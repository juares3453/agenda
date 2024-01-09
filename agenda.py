import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Arquivo JSON para armazenar a agenda
AGENDA_FILE = 'agenda.json'

# Função para carregar a agenda a partir do arquivo JSON
def carregar_agenda():
    try:
        with open(AGENDA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Função para salvar a agenda no arquivo JSON
def salvar_agenda(agenda):
    with open(AGENDA_FILE, 'w') as file:
        json.dump(agenda, file, indent=4)

# Carrega a agenda ao iniciar o aplicativo
agenda_telefonica = carregar_agenda()

@app.route('/')
def index():
    return render_template('index.html', agenda=agenda_telefonica)

@app.route('/adicionar_contato', methods=['POST'])
def adicionar_contato():
    nome = request.form['nome']
    ramal = request.form['ramal']
    setor = request.form['setor']

    contato = {'setor': setor, 'ramal': ramal}
    agenda_telefonica[nome] = contato
    salvar_agenda(agenda_telefonica)

    return redirect(url_for('index'))


@app.route('/remover_contato/<nome>', methods=['POST'])
def remover_contato(nome):
    if nome in agenda_telefonica:
        del agenda_telefonica[nome]
        salvar_agenda(agenda_telefonica)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
