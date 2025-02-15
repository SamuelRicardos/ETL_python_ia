import pandas as pd
from openai import OpenAI

try:
    df = pd.read_csv('content/sunglases_sales.csv')
except FileNotFoundError:
    print("O arquivo CSV não foi encontrado no caminho especificado.")
    df = pd.DataFrame()

client = OpenAI()

def ask_gpt(prompt):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Você é um Engenheiro de Dados especializado em ETL."},
            {"role": "user","content": prompt}
        ]
    )
    response = completion.choices[0].message.content
    return response

pergunta = input('Faça sua pergunta: \n')

prompt_exemplo = f'Tenho um DF chamado "df" e as colunas são: {df.dtypes}. Segue uma amostra dos dados: {df.head(6)}. Quero que você me diga apenas o código, nada mais que o código, para a pergunta: {pergunta}'

codigos_recebidos = ask_gpt(prompt_exemplo)

codigos_tratados = codigos_recebidos.split('\n')
codigos_tratados = codigos_tratados[1:-1]

for codigo in codigos_tratados:
    print('Executando código:', codigo)
    try:
        exec(codigo)
    except Exception as e:
        print(f"Erro ao executar o código: {e}")

ultimo_codigo = codigos_tratados[-1].split(' = ')[0]
try:
    resultado = eval(ultimo_codigo)
    print("Resultado final:", resultado)
except Exception as e:
    print(f"Erro ao avaliar o código: {e}")