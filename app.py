
from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)
DB_URL = os.environ.get("DATABASE_URL")

def get_conn():
    return psycopg2.connect(DB_URL)

@app.route("/")
def home():
    return "Sistema de Cadastro de Alface com PostgreSQL"

@app.route("/relatorio")
def relatorio():
    con = get_conn()
    cur = con.cursor()
    cur.execute("SELECT * FROM faturamento_mensal")
    dados = cur.fetchall()
    con.close()
    return render_template("relatorio.html", dados=dados)

@app.route("/dashboard")
def dashboard():
    con = get_conn()
    cur = con.cursor()
    cur.execute("SELECT mes, vendas, sacolas, lucro_liquido, valor_liquido_por_sacola FROM faturamento_mensal ORDER BY mes")
    rows = cur.fetchall()
    con.close()

    meses = [r[0] for r in rows]
    vendas = [r[1] for r in rows]
    sacolas = [r[2] for r in rows]
    lucros = [r[3] for r in rows]
    precos = [r[4] for r in rows]

    vendas_totais = sum(v for v in vendas if v)
    sacolas_totais = sum(s for s in sacolas if s)
    lucro_total = sum(l for l in lucros if l)

    return render_template("dashboard.html",
        meses=meses,
        lucros=lucros,
        precos=precos,
        vendas_totais=vendas_totais,
        sacolas_totais=sacolas_totais,
        lucro_total=lucro_total
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
