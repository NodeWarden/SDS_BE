def conta_ricorrenze(file_path, lettera):
    ricorrenze = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parole = line.split()
            for parola in parole:
                if parola.startswith(lettera):
                    ricorrenze[parola] = ricorrenze.get(parola, 0) + 1
    return ricorrenze

# Esempio di utilizzo
file_path = 'frasi_di_pericolo.txt'  # Sostituisci con il percorso del tuo file
lettera = 'E'           # Sostituisci con la lettera che vuoi cercare

ricorrenze = conta_ricorrenze(file_path, lettera)
print(ricorrenze)
