import pandas as pd
import time


# Importando o arquivo csv
df = pd.read_csv("comentarios.csv", encoding='UTF-8')

start = time.time()
# Criando uma nova coluna "lixo"
df["new"] = None

# Separando os conteúdos
for index, row in df.iterrows():
    comentarios = row['Comentários']
    # Substituindo os caracteres especiais
    comentarios = str(comentarios)

    comentarios = comentarios.replace('[a-zA-ZÀ-Úà-ú ]', '')
    # Verificando se é somente caracteres alfabéticos
    if comentarios.isalpha():
        df.at[index, 'Comentários'] = comentarios
    else:
        df.at[index, 'new'] = comentarios
        df.at[index, 'Comentários'] = None


df.drop(columns=["Comentários"], inplace=True)

df.dropna(thresh=None, inplace=True)


# Exibindo o resultado
print(df)

end = time.time()
exec_time = end - start
print(f"Tempo de execução: {exec_time:.2f}s ")