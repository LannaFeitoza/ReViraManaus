from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'chave-secreta-super-segura'

# Simula um banco de dados em memória
usuarios_registrados = {}

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

        if nome and email and senha and cidade:
            # Armazena os dados na "base de dados" em memória
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
            session['usuario_email'] = email  # salva só o email na sessão
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

    usuario = usuarios_registrados.get(email)

    if usuario and usuario['senha'] == senha:
        session['usuario_email'] = email  # salva o e-mail do usuário logado
        return redirect(url_for('conta'))
    else:
        flash('Credenciais inválidas. Tente novamente.')
        return redirect(url_for('cadastro'))

# Página da conta
@app.route('/conta')
def conta():
    email = session.get('usuario_email')
    if email and email in usuarios_registrados:
        usuario = usuarios_registrados[email]
        return render_template('conta.html', usuario=usuario)
    flash('Você precisa estar logado para acessar sua conta.')
    return redirect(url_for('cadastro'))

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_email', None)
    flash("Você saiu da sua conta.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
