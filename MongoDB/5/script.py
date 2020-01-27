## O dataset de jogadores NBA vinha mal formatado, faltava uma virgula no final de cada linha
# Este script corrige isso

# O dataset foi buscado a https://data.mendeley.com/datasets/ct8f9skv97/1

f = open("nbagames.json", "r")
out = open("nba.json", "w")
line = f.readline()

while line:
    res = line + ',\n'
    out.write(res)
    line = f.readline()

