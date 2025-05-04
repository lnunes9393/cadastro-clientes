from flask import Flask, render_template, request, redirect
import sqlite3
import pandas as pd
import os

app = Flask(__name__)

def get_data(query):
    conn = sqlite3.connect("clientes.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

@app.route("/")
def home():
    return "Hello World"

@app.route("/dashboard")
def dashboard():
    df_fat = get_data("SELECT * FROM faturamento_mensal")
    df_gastos = get_data("SELECT * FROM gastos_indiretos")
    return render_template("dashboard.html", faturamento=df_fat.to_dict(orient='records'), gastos=df_gastos.to_dict(orient='records'))

@app.route("/relatorio")
def relatorio():
    df = get_data("SELECT * FROM controle_vendas")
    return render_template("relatorio.html", vendas=df.to_dict(orient='records'))

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        data = request.form["data"]
        cliente = request.form["cliente"]
        quantidade = request.form["quantidade"]
        conn = sqlite3.connect("clientes.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO controle_vendas (data, cliente, quantidade) VALUES (?, ?, ?)", (data, cliente, quantidade))
        conn.commit()
        conn.close()
        return redirect("/relatorio")
    return render_template("cadastrar.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)