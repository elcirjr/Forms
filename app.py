import os
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    como_soube = db.Column(db.String(120), nullable=False)

class Corretor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    imobiliaria = db.Column(db.String(80), nullable=False)

class Ponto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    horario = db.Column(db.Time, nullable=False)
    corretor_id = db.Column(db.Integer, db.ForeignKey('corretor.id'), nullable=False)
    corretor = db.relationship('Corretor', backref=db.backref('pontos', lazy=True))

db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cliente', methods=['GET', 'POST'])
def cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        como_soube = request.form['como_soube']
        novo_cliente = Cliente(nome=nome, telefone=telefone, email=email, como_soube=como_soube)
        db.session.add(novo_cliente)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cliente_form.html')

@app.route('/corretor', methods=['GET', 'POST'])
def corretor():
    if request.method == 'POST':
        cpf = request.form['cpf']
        nome = request.form['nome']
        imobiliaria = request.form['imobiliaria']
        if Corretor.query.filter_by(cpf=cpf).first():
            return "CPF já cadastrado!"
        novo_corretor = Corretor(cpf=cpf, nome=nome, imobiliaria=imobiliaria)
        db.session.add(novo_corretor)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('corretor_form.html')

@app.route('/ponto', methods=['GET', 'POST'])
def ponto():
    if request.method == 'POST':
        data = request.form['data']
        horario = request.form['horario']
        cpf = request.form['cpf']
        corretor = Corretor.query.filter_by(cpf=cpf).first()
        if not corretor:
            return "Corretor não encontrado!"
        novo_ponto = Ponto(data=data, horario=horario, corretor=corretor)
        db.session.add(novo_ponto)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('ponto_form.html')

if __name__ == '__main__':
    app.run(debug=True)
