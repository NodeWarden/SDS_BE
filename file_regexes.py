import re
import json
from pathlib import Path

GUIDE_FOLDER = Path("./guidelines/processed")
DATA_FOLDER = Path("./data/processed")

guide_list = list(GUIDE_FOLDER.glob("*.txt"))
file_list = list(DATA_FOLDER.glob("*.txt"))

out_dir = Path("./outputs")
out_dir.mkdir(parents=True, exist_ok=True)

dict_list = []
dict_dang = []
associazioni = {}
#estrazione associazioni H, M e tipo M(INA/CUT)
for guide_file in guide_list:
    with open(guide_file, "r", encoding="utf-8") as g:
        testo = g.read()
        # doc_rows = {}
        for riga in testo.splitlines():
            pattern_M = re.search(r"\|\s*(\d+)", riga)
            pattern_H = re.search(r"\bH\d{3}[A-Z]?\b", riga)
            if pattern_H and pattern_M:
                if pattern_H.group() not in associazioni:
                    associazioni[pattern_H.group()] = []
                associazioni[pattern_H.group()].append((pattern_M.group(1), str(guide_file)))
                dict_dang.append({
                    'pericolosita' : str(guide_file), 
                    'indice_M' : pattern_M.group(1), 
                    'indice_H' : pattern_H.group()
                    })
#fine estrazione associazioni

# dict_list.append(associazioni)
print(associazioni)


#estrazione e salvataggio json con codici h da file chunkati.
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
                        dict_list.append({'file_name' : str(file_path), 'sezione' : titolo, 'frase_H' : match.group(), 'pericolo_M' : associazioni[pattern_H.group()]})
                        # if match.group() in dict_dang.values():
                        #     for M in dict_dang.items():
                                
#fine estrazione frasi h da pdf




## se dict_list(sezione) < 3 ==> json = filename, col=H, val
## se dict_list(sezione) >= 3 => json = filename, col=L, val


with open(out_dir/"ready2csv2.json","w", encoding="utf-8") as j:
    json.dump(dict_list, j, indent=4)