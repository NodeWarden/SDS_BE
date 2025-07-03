import re
import json
from pathlib import Path


DATA_FOLDER = Path("./data/processed")
file_list = list(DATA_FOLDER.glob("*.txt"))
out_dir = Path("./outputs")
out_dir.mkdir(parents=True, exist_ok=True)

dict_list = []

for file_path in file_list:
    with open(file_path, "r", encoding="utf-8") as f:
        testo = f.read()
        doc_sections = {}
        
        pattern_titoli = re.compile(r"^[#\s]*sezione\s*\d", re.MULTILINE | re.IGNORECASE)
        pattern_h = re.compile(r"\bH\d{3}[A-Z]?\b")
        h_in_sect2 = False
        
        match_titoli = list(pattern_titoli.finditer(testo))
        
        for i, match in enumerate(match_titoli):
            
            titolo = match.group().strip()
            start = match.end()
            end = match_titoli[i+1].start() if i+1 < len(match_titoli) else len(testo)
            
            doc_sections[titolo] = testo[start:end].strip()

        for titolo, testo_sezione in doc_sections.items():
            h_found = set()
            if h_in_sect2 == False:
                for match in pattern_h.finditer(testo_sezione):
                    if (titolo.lower().strip().endswith("sezione 2")): h_in_sect2 = True
                    if match.group() not in h_found:
                        h_found.add(match.group())
                        print(f"File: {file_path}, sezione: {titolo}, frase H: {match.group()}")
                        dict_list.append({'file_name' : str(file_path), 'sezione' : titolo, 'frase_H' : match.group()})
                    
with open(out_dir/"ready2csv.json","w", encoding="utf-8") as j:
    json.dump(dict_list, j, indent=4)

## se dict_list(sezione) < 3 ==> json = filename, col=H, val
## se dict_list(sezione) >= 3 => json = filename, col=L, val
##