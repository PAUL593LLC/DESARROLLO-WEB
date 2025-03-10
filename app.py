from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET KEY'] = 'mi_secreto_seguro' #necesario para formularios con CSRF

# Definir la clase de formulario

class Formulario(FlaskForm):
 nombre = StringField('Nombre',
validators=[DataRequired()])
 enviar = SubmitField('Enviar')


app = Flask(__name__)

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Página "Acerca de"
@app.route('/about')
def about():
    return render_template('about.html')

# Ruta dinámica con nombre de usuario
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return render_template('usuario.html', nombre=nombre)

# Ruta con formulario para ingresar nombre
@app.route('/usuario/formulario', methods=['GET', 'POST'])
def usuario_form():
    if request.method == 'POST':
        nombre = request.form['nombre']
        return render_template('usuario.html', nombre=nombre)
    return render_template('formulario.html')

if __name__ == '__main__':
    app.run(debug=True)
