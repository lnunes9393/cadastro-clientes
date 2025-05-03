from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello World'

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))  # Render define essa variável automaticamente
    app.run(host='0.0.0.0', port=port)
