import sys

if len(sys.argv) != 2:
    print(f"Uso: python3 {sys.argv[0]} mensajeCifrado")
    sys.exit(1)

print("No funciono bien... :(")
mensaje_cifrado = sys.argv[1]

alfabeto = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
frecuencias = {letra: 0 for letra in alfabeto}
total_letras = 0

for caracter in mensaje_cifrado.upper():
    if caracter in alfabeto:
        frecuencias[caracter] += 1
        total_letras += 1



print("Letra | Frec.")

for posicion, letra in enumerate(alfabeto):
    if total_letras > 0:
        frecuencia = frecuencias[letra] / total_letras
    else:
        frecuencia = 0

    print(f"-> {letra} : {frecuencia:.2f}", end="  ")

    if posicion % 3 == 2:
        print()

frecExperimentales = "EAOLSNDRUITCPMYQBHGFVJÑZXKW"
sortedFrecs = sorted(frecuencias,key=frecuencias.get,reverse=True)
diccionario = {}

for i,l in enumerate(sortedFrecs):
    diccionario[l] = frecExperimentales[i]

mensaje_descifrado = ""
for c in mensaje_cifrado.upper():
    if(c in alfabeto):
        mensaje_descifrado += diccionario[c]
    
    else:
        mensaje_descifrado += " "


print(mensaje_descifrado)