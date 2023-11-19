#app.py

from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Configurações do banco de dados PostgreSQL
db_params = {
    'dbname': 'estoque',
    'user': 'postgres',
    'password': '1234',
    'host': 'localhost',
    'port': '5432'
}



@app.route('/')
def index():
    return render_template('index.html')

#Rota para adicionar ao estoque
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Recebendo os dados do formulário
        nome = request.form['nome']
        cod_barras = int(request.form['cod_barras'])
        lote = int(request.form['lote'])
        fabricante = request.form['fabricante']
        dt_fabricacao =  datetime.strptime(request.form['data_fabricação'], '%Y-%m-%d').date()
        dt_vencimento =  datetime.strptime(request.form['data_validade'], '%Y-%m-%d').date()
        preco = float(request.form['preco'])
        quantidade = int(request.form['quantidade'])
        obs = request.form['obs']

        add_item_estq(nome=nome, cod_barras=cod_barras, lote=lote, fabricante=fabricante, dt_fabricacao=dt_fabricacao, dt_vencimento=dt_vencimento, preco=preco, quantidade=quantidade, obs=obs)
        return render_template('add.html')
    return render_template('add.html')

# Rota para exibir o estoque
@app.route('/consult', methods=['GET', 'POST'])
def consult():
    data = get_est()


    return render_template('consult.html', data=data)


@app.route('/modify_quantity/<int:product_id>', methods=['POST'])
def modify_quantity(product_id):
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    quantidade_diminuir = int(request.form['quantidade_diminuir'])

    # Obtém os dados do produto
    cursor.execute("SELECT * FROM produtos WHERE id = %s", (product_id,))
    product_data = cursor.fetchone()

    current_quantity = product_data[8]  # Índice 8 para a coluna 'quantidade'

    if current_quantity == 0 or quantidade_diminuir >= current_quantity:
        cursor.execute("DELETE FROM produtos WHERE id = %s", (product_id,))
    else:
        new_quantity = current_quantity - quantidade_diminuir
        cursor.execute("UPDATE produtos SET quantidade = %s WHERE id = %s", (new_quantity, product_id))

    # Adiciona ao histórico de vendas
    produto_id = product_data[0]  # Índice 0 para a coluna 'id' na tabela 'produtos'
    data_venda = datetime.now().date()  # Data atual
    quantidade_vendida = quantidade_diminuir
    preco_unitario = product_data[7]  # Índice 7 para a coluna 'preco'
    valor_total = preco_unitario * quantidade_vendida

    # Insere os dados na tabela de vendas_historico
    cursor.execute("INSERT INTO vendas_historico (produto_id, data_venda, quantidade, preco_unitario, valor_total) VALUES (%s, %s, %s, %s, %s)",
                    (produto_id, data_venda, quantidade_vendida, preco_unitario, valor_total))

    conn.commit()
    conn.close()
    
    return redirect(url_for('consult'))


@app.route('/historic')
def historic():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vendas_historico")
    historico = cursor.fetchall()

    conn.close()

    return render_template('historic.html', historico=historico)



#Função para adicionar itens ao inventario
def add_item_estq(nome, cod_barras, lote, fabricante, dt_fabricacao, dt_vencimento, preco, quantidade, obs):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute(f"INSERT INTO produtos (nome, cod_barras, lote, fabricante, dt_fabricacao, dt_validade, preco, quantidade, obs) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (nome, cod_barras, lote, fabricante, dt_fabricacao, dt_vencimento, preco, quantidade, obs))
        conn.commit()
        cursor.close()
        conn.close()


    except Exception as e:
        print(e)


def get_est():

    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    data = cursor.fetchall()
    conn.close()
    return data

if __name__ == '__main__':
    app.run(debug=True)