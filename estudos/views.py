from flask import Blueprint, render_template,redirect,url_for, session
import sqlite3
from estudos import bcrypt
from .forms import LoginForm, CadastroForm
from flask import request, jsonify
views = Blueprint('views',__name__)


@views.route('/')
def index():
    return render_template('index.html')

def gerar_hash(senha):
    hash_senha = bcrypt.generate_password_hash(senha).decode('utf-8')
    return hash_senha

def verificar_senha(senha_digitada, senha_hash):
    return bcrypt.check_password_hash(senha_hash, senha_digitada)



@views.route('/login',methods =['POST', 'GET'])
def login():
    form = LoginForm()
    erro = None
    

    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data

        with sqlite3.connect('app/usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT senha, nome FROM usuarios WHERE email = ?', (email,))
            row = cursor.fetchone()

            if row and verificar_senha(senha, row[0]):
                session['usuario'] = row[1]
                session.permanent = True
                return redirect(url_for('views.dashboard'))
            else:
                erro = 'Email ou senha incorreto'
    return render_template('login.html', form = form, erro = erro)

@views.route('/cadastro', methods =['POST','GET'])
def cadastro():
    form = CadastroForm()
    erro = None

    if form.validate_on_submit:
        nome = form.nome.data
        email = form.nome.email
        senha = form.nome.senha
        senha_hash = gerar_hash(senha)

        with sqlite3.connect('app/usuarios.db') as conn:
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM usuarios WHERE email = ?', (email,))

            if cursor.fetchone():
                erro ='Email já cadastrado em nosso site'
                return render_template('cadastro.html', erro = erro, form = form)


            cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?,?,?)', (nome, email, senha_hash))

        return redirect(url_for('views.login'))
    return render_template('cadastro.html', form = form, erro = erro)

@views.route('/experimentos',methods =['POST','GET'])
def experimentos():
    return render_template('experimentos.html')


@views.route('/experimento-queda-livre',methods =['POST','GET'])
def experimento_queda_livre():
    return render_template('experimento-queda-livre.html')

@views.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"response": "Por favor, digite algo para começar."})

    # Aqui você pode colocar a integração com uma IA depois.
    resposta = f"Você disse: {message}"
    return jsonify({"response": resposta})