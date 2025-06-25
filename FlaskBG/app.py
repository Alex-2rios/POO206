from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Riosgamesas31@"
app.config['MYSQL_DB'] = "dbflask"
app.secret_key = "supersecretkey"

mysql = MySQL(app)

# Ruta de inicio
@app.route('/')
def home():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums')
        consultaTodos = cursor.fetchall()
        return render_template('formulario.html', errores={}, albums=consultaTodos)
    except Exception as e:
        print('Error al consultar la base de datos:', e)
        return render_template('formulario.html', errores={}, albums=[])
    finally:
        cursor.close()
        
@app.route('/detalle/<int:id>')
def detalle(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums WHERE id=%s', (id,))
        consultaId = cursor.fetchone()
        return render_template('consulta.html', Albums=consultaId)
    except Exception as e:
        print('Error al consultar por id:' +e)
        return redirect(url_for('home'))
    finally:
        cursor.close()

# Ruta de consulta
@app.route('/consulta')
def consulta():
    return render_template('consulta.html')

# Ruta para el insert
@app.route('/guardarAlbum', methods=['POST'])
def guardar():
    errores = {}

    # Obtener los datos a insertar
    titulo = request.form.get('txtTitulo', '').strip()
    artista = request.form.get('txtArtista', '').strip()
    año = request.form.get('txtAnio', '').strip()

    # Validación de campos vacíos y formato de año
    if not titulo:
        errores['txtTitulo'] = 'Nombre del album obligatorio'
    if not artista:
        errores['txtArtista'] = 'Nombre del artista obligatorio'
    if not año:
        errores['txtAnio'] = 'Año del album obligatorio'
    elif not año.isdigit() or int(año) < 1800 or int(año) > 2030:
        errores['txtAnio'] = 'En año solo ingresar un año valido'

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO Albums (Titulo, Artista, Año) VALUES (%s, %s, %s)', (titulo, artista, año))
            mysql.connection.commit()
            flash('Album guardado con éxito')
            return redirect(url_for('home'))
        except Exception as e:
            mysql.connection.rollback()  # Deshacer cambios en caso de error
            flash('Error al guardar: ' + str(e))
            return redirect(url_for('home'))
        finally:
            cursor.close()

    return render_template('formulario.html', errores=errores)

# Ruta con manejo de errores
@app.errorhandler(404)
def paginaNoE(e):
    return 'Cuidado: Error de capa 8 !!!'

@app.errorhandler(405)
def metodoNoValido(e):
    return 'Cuidado: Método no permitido !!!'

# Ruta para probar la conexión a MySQL
@app.route('/DBCheck')
def DB_check():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        return jsonify({'status': 'ok', 'message': 'Conectado con éxito'}), 200
    except MySQLdb.MySQLError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
