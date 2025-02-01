import requests

clientes = [
    {"nome": "João Silva", "email": "joao.silva@example.com", "senha": "senha123"},
    {"nome": "Maria Souza", "email": "maria.souza@example.com", "senha": "senha456"},
    # Adicione mais clientes aqui
]

url = "http://localhost:5000/cadastro"

for cliente in clientes:
    response = requests.post(url, json=cliente)
    print(response.json())
