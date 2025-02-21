from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():  # put application's code here
    return 'BIENVENIDOS NUEVAMENTE AMIGOS'

# NUEVA RUTA
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f"Hola, {nombre}!"


if __name__ == '__main__':
    app.run()
