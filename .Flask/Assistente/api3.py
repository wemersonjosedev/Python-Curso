import requests
import json

URL = "http://localhost:5000/cursos"

response = requests.get(url=URL)

cursos = json.loads(response.text)

cursos = cursos['results']

for curso in cursos:
    nome = curso['nome']
    descricao = curso['descricao']
    data = curso['data_publicacao']
    texto = f'Curso {nome} tem descrição {descricao} e foi criado em {data}'
    print(texto)