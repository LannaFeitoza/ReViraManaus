from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/cadastro')
def cadastro():
    return render_template('c.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
