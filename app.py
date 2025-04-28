from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from models.estabelecimento_model import Estabelecimento
from services import estabelecimento_service as service

app = Flask(__name__)
app.secret_key = 'segredo_seguro_para_flash'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastrar-form', methods=['GET', 'POST'])
def cadastrar_form():
    if request.method == 'POST':
        nome = request.form['nome']
        lat = float(request.form['latitude'])
        lon = float(request.form['longitude'])

        est = Estabelecimento(nome, lat, lon)
        sucesso, msg = service.cadastrar_estabelecimento(est)
        if sucesso:
            flash(msg, 'success')
            return redirect(url_for('listar_todos_web'))
        else:
            flash(msg, 'error')
            return redirect(url_for('cadastrar_form'))
    return render_template('cadastrar.html')

@app.route('/relatorio-5km-form', methods=['GET', 'POST'])
def relatorio_5km_form():
    if request.method == 'POST':
        nome = request.form['nome']
        resultado, erro = service.relatorio_5km_por_nome(nome)
        if erro:
            flash(erro, 'error')
        return render_template('relatorio_5km.html', nome=nome, resultado=resultado)
    return render_template('relatorio_5km.html')

@app.route('/relatorio-mais-proximo-form', methods=['GET', 'POST'])
def relatorio_mais_proximo_form():
    if request.method == 'POST':
        try:
            lat = float(request.form['latitude'])
            lon = float(request.form['longitude'])
            resultado, erro = service.mais_proximo_de_ponto(lat, lon)
            if erro:
                flash(erro, 'error')
            return render_template('relatorio_mais_proximo.html', resultado=resultado)
        except:
            flash("Latitude e longitude inválidas", 'error')
            return redirect(url_for('relatorio_mais_proximo_form'))
    return render_template('relatorio_mais_proximo.html')

@app.route('/relatorio-10km')
def relatorio_10km_web():
    resultado = service.relatorio_10km()
    return render_template('relatorio_10km.html', resultado=resultado)

@app.route('/listar-todos')
def listar_todos_web():
    estabelecimentos = service.listar_estabelecimentos()
    return render_template('listar_todos.html', estabelecimentos=estabelecimentos)

@app.route('/editar/<nome>', methods=['GET', 'POST'])
def editar_estabelecimento(nome):
    est = service.buscar_por_nome(nome)
    if not est:
        flash(f"Estabelecimento '{nome}' não encontrado.", 'error')
        return redirect(url_for('listar_todos_web'))

    if request.method == 'POST':
        novo_nome = request.form['nome']
        nova_lat = float(request.form['latitude'])
        nova_lon = float(request.form['longitude'])
        sucesso, msg = service.editar_estabelecimento(nome, Estabelecimento(novo_nome, nova_lat, nova_lon))

        if sucesso:
            flash(msg, 'success')
        else:
            flash(msg, 'error')
        return redirect(url_for('listar_todos_web'))

    return render_template('editar.html', estabelecimento=est)

@app.route('/excluir/<nome>')
def excluir_estabelecimento(nome):
    sucesso, msg = service.excluir_estabelecimento(nome)
    flash(msg, 'success' if sucesso else 'error')
    return redirect(url_for('listar_todos_web'))

@app.route('/mapa')
def mapa():
    estabelecimentos = service.listar_estabelecimentos()
    return render_template('mapa.html', estabelecimentos=estabelecimentos)

if __name__ == '__main__':
    app.run(debug=True)
