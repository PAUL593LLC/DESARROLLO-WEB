from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from modelos.modelos import Usuario
from modelos.productos import Producto
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from Conexion.conexion import obtener_conexion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto_seguro'  # Necesario para formularios con CSRF

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Definir la clase de formulario
class NombreForm(FlaskForm):
    nombre = StringField('Ingresa tu nombre', validators=[DataRequired(), Length(min=2, max=20)])
    enviar = SubmitField('Enviar')


# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')


# Ruta para el formulario
@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    form = NombreForm()
    if form.validate_on_submit():
        session['nombre'] = form.nombre.data  # Guardar en sesión
        flash('Formulario enviado con éxito!', 'success')
        return redirect(url_for('resultado'))
    return render_template('formulario.html', form=form)


# Ruta para mostrar el resultado
@app.route('/resultado')
def resultado():
    nombre = session.get('nombre', None)  # Obtener de sesión

    if nombre is None:  # Evita errores si no se ha llenado el formulario
        flash('No hay datos en la sesión. Ingresa tu nombre en el formulario.', 'warning')
        return redirect(url_for('formulario'))

    return render_template('resultado.html', nombre=nombre)
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test_db')
def test_db():
    conexion = obtener_conexion()
    if conexion:
        conexion.close()
        return "Conexión exitosa a MySQL"
    else:
        return "Error en la conexión a MySQL"


# Ruta para obtener todos los usuarios de la base de datos
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Para obtener los resultados en formato de diccionario
        cursor.execute("SELECT * FROM usuarios")  # Corrección aquí
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return jsonify(usuarios)  # Retornar los datos en formato JSON
    else:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500


# Ruta para mostrar los usuarios en una tabla HTML
@app.route('/usuarios_formulario', methods=['GET'])
def usuarios_tabla():
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor(dictionary=True)  # Para obtener los resultados en formato de diccionario
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        conexion.close()
        return render_template('usuarios_formulario.html', usuarios=usuarios)
    else:
        return "Error en la conexión a la base de datos", 500


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Verificar si el usuario ya existe
        cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (email,))
        usuario_existente = cursor.fetchone()

        if usuario_existente:
            flash('Este correo ya está registrado.', 'warning')
            cursor.close()
            conexion.close()
            return redirect(url_for('registro'))

        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
                       (nombre, email, password_hash))
        conexion.commit()
        cursor.close()
        conexion.close()
        flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario = Usuario.obtener_por_email(email)

        if usuario and usuario.verificar_password(password):
            login_user(usuario)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email o contraseña incorrectos', 'danger')

    return render_template('login.html')


@app.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        if nombre and precio and stock:
            Producto.insertar(nombre, float(precio), int(stock))
            flash('Producto creado exitosamente.', 'success')
            return redirect(url_for('listar_productos'))
        else:
            flash('Todos los campos son obligatorios.', 'danger')
    return render_template('crear_producto.html')

@app.route('/productos')
def listar_productos():
    productos = Producto.obtener_todos()
    return render_template('productos.html', productos=productos)
@app.route('/editar/<int:id_producto>', methods=['GET', 'POST'])
def editar_producto(id_producto):
    producto = Producto.obtener_por_id(id_producto)
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        Producto.actualizar(id_producto, nombre, float(precio), int(stock))
        flash('Producto actualizado correctamente.')
        return redirect(url_for('listar_productos'))
    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<int:id_producto>', methods=['GET', 'POST'])
def eliminar_producto(id_producto):
    if request.method == 'POST':
        Producto.eliminar(id_producto)
        flash('Producto eliminado correctamente.')
        return redirect(url_for('listar_productos'))
    producto = Producto.obtener_por_id(id_producto)
    return render_template('eliminar_producto.html', producto=producto)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.obtener_por_id(user_id)


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
