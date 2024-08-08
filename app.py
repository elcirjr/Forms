from flask import Flask, request, render_template, redirect, url_for
from openpyxl import Workbook, load_workbook
import os

app = Flask(__name__)

# Nomes dos arquivos de planilha
FILE_NAME_ATENDIMENTO = 'atendimento_respostas.xlsx'
FILE_NAME_CLIENTE = 'cliente_respostas.xlsx'
FILE_NAME_CORRETOR = 'corretor_respostas.xlsx'
FILE_NAME_PONTO = 'ponto_respostas.xlsx'

def init_excel_file(file_name, headers):
    if not os.path.exists(file_name):
        wb = Workbook()
        ws = wb.active
        ws.append(headers)
        wb.save(file_name)

def check_duplicate(file_name, cpf):
    if os.path.exists(file_name):
        wb = load_workbook(file_name)
        ws = wb.active
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] == cpf:
                return True
    return False

@app.route('/')
def index(index):
    if index not in ['vendedor1', 'vendedor2']:
        abort(404)  # Retorna erro 404 se o vendedor não for válido
    return render_template('menu.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/atendimento')
def atendimento():
    return render_template('atendimento.html')

@app.route('/submit_atendimento_form', methods=['POST'])
def submit_atendimento_form():
    atendido = request.form['atendido']
    
    if not os.path.exists(FILE_NAME_ATENDIMENTO):
        init_excel_file(FILE_NAME_ATENDIMENTO, ['Atendido'])
    
    wb = load_workbook(FILE_NAME_ATENDIMENTO)
    ws = wb.active
    ws.append([atendido])
    wb.save(FILE_NAME_ATENDIMENTO)
    
    if atendido == 'Sim':
        return redirect(url_for('cliente_form'))
    else:
        return redirect(url_for('menu'))

@app.route('/cliente_form')
def cliente_form():
    return render_template('cliente_form.html')

@app.route('/submit_cliente_form', methods=['POST'])
def submit_cliente_form():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    data_visita = request.form['data_visita']
    como_soube = request.form['como_soube']
    
    if not os.path.exists(FILE_NAME_CLIENTE):
        init_excel_file(FILE_NAME_CLIENTE, ['Nome', 'Telefone', 'E-mail', 'Data da Visita', 'Como Soube'])
    
    wb = load_workbook(FILE_NAME_CLIENTE)
    ws = wb.active
    ws.append([nome, telefone, email, data_visita, como_soube])
    wb.save(FILE_NAME_CLIENTE)
    
    return redirect(url_for('menu'))

@app.route('/corretor_form')
def corretor_form():
    return render_template('corretor_form.html')

@app.route('/submit_corretor_form', methods=['POST'])
def submit_corretor_form():
    cpf = request.form['cpf']
    nome = request.form['nome']
    imobiliaria = request.form['imobiliaria']
    
    if check_duplicate(FILE_NAME_CORRETOR, cpf):
        return "Erro: CPF já cadastrado."
    
    if not os.path.exists(FILE_NAME_CORRETOR):
        init_excel_file(FILE_NAME_CORRETOR, ['CPF', 'Nome', 'Imobiliária'])
    
    wb = load_workbook(FILE_NAME_CORRETOR)
    ws = wb.active
    ws.append([cpf, nome, imobiliaria])
    wb.save(FILE_NAME_CORRETOR)
    
    return redirect(url_for('menu'))

@app.route('/ponto_form')
def ponto_form():
    return render_template('ponto_form.html')

@app.route('/submit_ponto_form', methods=['POST'])
def submit_ponto_form():
    cpf = request.form['cpf']
    data = request.form['data']
    horario_entrada = request.form['horario_entrada']
    horario_saida = request.form['horario_saida']
    
    # Verifica se o CPF existe na planilha de corretores
    if not check_duplicate(FILE_NAME_CORRETOR, cpf):
        return "Erro: CPF não cadastrado."
    
    if not os.path.exists(FILE_NAME_PONTO):
        init_excel_file(FILE_NAME_PONTO, ['CPF', 'Data', 'Horário de Entrada', 'Horário de Saída'])
    
    wb = load_workbook(FILE_NAME_PONTO)
    ws = wb.active
    ws.append([cpf, data, horario_entrada, horario_saida])
    wb.save(FILE_NAME_PONTO)
    
    return redirect(url_for('menu'))

if __name__ == '__main__':
    init_excel_file(FILE_NAME_ATENDIMENTO, ['Atendido', 'Data'])
    init_excel_file(FILE_NAME_CLIENTE, ['Nome', 'Telefone', 'E-mail', 'Data da Visita', 'Como Soube'])
    init_excel_file(FILE_NAME_CORRETOR, ['CPF', 'Nome', 'Imobiliária'])
    init_excel_file(FILE_NAME_PONTO, ['CPF', 'Data', 'Horário de Entrada', 'Horário de Saída'])
    app.run(debug=True)
