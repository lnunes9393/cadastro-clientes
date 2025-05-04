from flask import Flask, render_template
import sqlite3
import pandas as pd

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

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  # Render define automaticamente
    app.run(host="0.0.0.0", port=port)
