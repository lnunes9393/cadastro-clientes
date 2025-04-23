
from flask import Flask, render_template, request
import sqlite3
import os
import pandas as pd

app = Flask(__name__)
DB_PATH = 'database/clientes.db'

def criar_tabelas():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.executescript("""
CREATE TABLE IF NOT EXISTS vendas_sacolas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor_unitario REAL,
    quantidade INTEGER,
    valor_total REAL
);
CREATE TABLE IF NOT EXISTS gastos_indiretos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    mes TEXT,
    valor_total REAL
);
CREATE TABLE IF NOT EXISTS faturamento_mensal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mes TEXT,
    vendas REAL,
    sacolas REAL,
    gastos_indiretos REAL,
    lucro_liquido REAL,
    valor_liquido_por_sacola REAL
);
        """)

@app.route("/")
def home():
    return "Sistema de Cadastro de Alface"

@app.route("/relatorio")
def relatorio():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM faturamento_mensal")
    dados = cur.fetchall()
    con.close()
    return render_template("relatorio.html", dados=dados)

from flask import jsonify
@app.route("/dashboard")
def dashboard():
    con = sqlite3.connect(DB_PATH)
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
    os.makedirs("database", exist_ok=True)
    criar_tabelas()
    app.run(host="0.0.0.0", port=10000)
