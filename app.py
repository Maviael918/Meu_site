from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
from config import Config
from models import db, Cliente
import os

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.secret_key = 'sua_chave_secreta'  # Chave secreta para gerenciar sessões
db.init_app(app)

# Rota para a página principal de cadastro
@app.route('/')
def serve_front_end():
    return render_template('index.html')

# Rota para processar o login do usuário
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Dados recebidos para login:", data)  # Log para verificar dados recebidos
    cliente = Cliente.query.filter_by(email=data['email'], senha=data['senha']).first()
    if cliente:
        session['cliente_id'] = cliente.id  # Armazena o ID do cliente na sessão
        print(f"Login bem-sucedido! Cliente ID: {cliente.id}")  # Log para verificar a sessão
        return jsonify({"message": "Login bem-sucedido!"}), 200
    else:
        print("Email ou senha inválidos!")  # Log para login inválido
        return jsonify({"message": "Email ou senha inválidos!"}), 401

# Rota para processar o cadastro de um novo cliente
@app.route('/cadastro', methods=['POST'])
def cadastrar_cliente():
    data = request.get_json()
    print("Dados recebidos para cadastro:", data)  # Log para verificar dados recebidos
    novo_cliente = Cliente(nome=data['nome'], email=data['email'], senha=data['senha'])
    db.session.add(novo_cliente)  # Adiciona o novo cliente ao banco de dados
    db.session.commit()  # Salva as mudanças no banco de dados
    print("Cliente cadastrado com sucesso!")  # Log para cadastro de cliente
    return jsonify({"message": "Cliente cadastrado com sucesso!"}), 201

# Rota para listar todos os clientes cadastrados
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()  # Obtém todos os clientes do banco de dados
    resultado = [{"id": cliente.id, "nome": cliente.nome, "email": cliente.email} for cliente in clientes]
    return jsonify(resultado), 200

# Rota para servir a página de vídeo somente se o cliente estiver logado
@app.route('/video')
def serve_video_page():
    if 'cliente_id' in session:
        print(f"Exibindo vídeo para Cliente ID: {session['cliente_id']}")  # Log para sessão ativa
        return render_template('video.html')
    else:
        print("Sessão não encontrada! Redirecionando para a página principal.")  # Log para sessão inativa
        return redirect(url_for('serve_front_end'))

# Inicialização do banco de dados e execução do servidor Flask
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas do banco de dados
    
    # Rodando o servidor Flask com o host configurado para 0.0.0.0 para permitir o acesso externo
    app.run(host='0.0.0.0', port=5000, debug=True)  # Inicia o servidor Flask no modo de depuração
