import json
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'chave-secreta-super-segura'

# Caminho do arquivo JSON
USUARIOS_JSON = 'usuarios.json'

# Função para carregar os usuários do arquivo JSON
def carregar_usuarios():
    try:
        with open(USUARIOS_JSON, 'r') as f:
            usuarios = json.load(f)
            print("Usuários carregados do JSON:", usuarios)  # Print para verificar os dados carregados
            return usuarios
    except FileNotFoundError:
        print("Arquivo não encontrado, retornando dicionário vazio.")  # Print se o arquivo não for encontrado
        return {}  # Se o arquivo não existir, retorna um dicionário vazio

# Função para salvar os usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(USUARIOS_JSON, 'w') as f:
        json.dump(usuarios, f, indent=4)
    print("Usuários salvos no arquivo:", usuarios)  # Print para verificar os dados salvos

# Carregar os usuários ao iniciar o app
usuarios_registrados = carregar_usuarios()
print("Usuários registrados na inicialização:", usuarios_registrados)  # Verificar o conteúdo inicial dos usuários

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/coleta')
def coleta():
    return render_template('coleta.html')

@app.route('/descarte')
def descarte():
    return render_template('descarte.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

# Cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        cidade = request.form['cidade']

        print(f"Cadastro recebido: nome={nome}, email={email}, cidade={cidade}")  # Print para verificar os dados recebidos

        if nome and email and senha and cidade:
            # Armazena os dados no arquivo JSON
            usuarios_registrados[email] = {
                'nome': nome,
                'email': email,
                'senha': senha,
                'cidade': cidade,
                'pontos': 0,
                'ultimoDescarte': '',
                'ultimoPontos': '',
                'historico': []
            }
            salvar_usuarios(usuarios_registrados)  # Salva os dados no arquivo JSON
            session['usuario_email'] = email  # salva só o email na sessão
            print(f"Usuário {email} cadastrado com sucesso. Sessão: {session}")  # Verificando sessão
            flash("Cadastro realizado com sucesso!")
            return redirect(url_for('conta'))
        else:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('cadastro'))

    return render_template('c.html')

# Login do usuário
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    print(f"Tentativa de login: email={email}, senha={senha}")  # Print para verificar os dados recebidos

    usuario = usuarios_registrados.get(email)
    print(f"Usuário encontrado: {usuario}")  # Verificar se o usuário foi encontrado

    if usuario and usuario['senha'] == senha:
        session['usuario_email'] = email  # salva o e-mail do usuário logado
        print(f"Usuário {email} logado. Sessão: {session}")  # Verificar se a sessão foi definida
        return redirect(url_for('conta'))
    else:
        flash('Credenciais inválidas. Tente novamente.')
        return redirect(url_for('cadastro'))

# Página da conta
@app.route('/conta')
def conta():
    email = session.get('usuario_email')
    print(f"Verificando sessão na página de conta: {email}")  # Verificar o valor da sessão

    if email and email in usuarios_registrados:
        usuario = usuarios_registrados[email]
        print(f"Usuário encontrado na conta: {usuario}")  # Verificar se o usuário foi encontrado
        return render_template('conta.html', usuario=usuario)

    flash('Você precisa estar logado para acessar sua conta.')
    return redirect(url_for('cadastro'))

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_email', None)
    flash("Você saiu da sua conta.")
    print("Usuário deslogado. Sessão após logout:", session)  # Verificando sessão após logout
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
