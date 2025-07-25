from flask import Flask, jsonify, render_template, request, url_for, flash, redirect
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Riosgamesas31@"
app.config['MYSQL_DB'] = "dbflasks"
app.secret_key = "supersecretkey"

mysql = MySQL(app)

# Ruta de inicio
@app.route('/')
def home():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums WHERE State = 1')
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

@app.route('/editar/<int:id>')
def editar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums WHERE id=%s', (id,))
        album = cursor.fetchone()
        return render_template('formUpdate.html', album=album)
    except Exception as e:
        print('Error al obtener contacto:', e)
        return redirect(url_for('home'))
    finally:
        cursor.close()

@app.route('/actualizarAlbum/<int:id>', methods=['POST'])
def actualizarAlbum(id):
    datos = request.form
    titulo = datos.get('txtTitulo', '').strip()
    artista = datos.get('txtArtista', '').strip()
    año = datos.get('txtAnio', '').strip()
    edad = datos.get('txtEdad', '').strip()
    errores = {}

    if not titulo:
        errores['txtTitulo'] = 'El nombre es obligatorio'
    if not artista:
        errores['txtArtista'] = 'El correo es obligatorio'
    if not año:
        errores['txtAnio'] = 'Numero de teléfono obligatorio'
    if not edad:
        errores['txtEdad'] = 'Edad del contacto obligatorio'
    elif not edad.isdigit() or int(edad) < 1 or int(edad) > 105:
        errores['txtEdad'] = 'Solo se permiten edades entre 1 y 105'


    if errores:
        return render_template('formUpdate.html', album=(id, titulo, artista, año, edad), errores=errores)

    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Albums SET Titulo=%s, Artista=%s, Año=%s, Edad=%s WHERE id=%s', (titulo, artista, año, edad, id))
        mysql.connection.commit()
        flash('Contacto actualizado con éxito')
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al actualizar: ' + str(e))
    finally:
        cursor.close()

    return redirect(url_for('home'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums WHERE id = %s', (id,))
        album = cursor.fetchone()
        return render_template('confirmDel.html', album=album)
    except Exception as e:
        flash('Error al obtener contacto: ' + str(e))
        return redirect(url_for('home'))
    finally:
        cursor.close()

@app.route('/eliminarConfirmado/<int:id>', methods=['POST'])
def eliminarConfirmado(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Albums SET State = 0 WHERE id = %s', (id,))
        mysql.connection.commit()
        flash('Contacto eliminado con éxito')
    except Exception as e:
        mysql.connection.rollback()
        flash('Error al eliminar: ' + str(e))
    finally:
        cursor.close()
    return redirect(url_for('home'))


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
    edad = request.form.get('txtEdad', '').strip()

    # Validación de campos vacíos y formato de año
    if not titulo:
        errores['txtTitulo'] = 'Nombre obligatorio'
    if not artista:
        errores['txtArtista'] = 'Correo obligatorio'
    if not año:
        errores['txtAnio'] = 'Numero de teléfono obligatorio'
    if not edad:
        errores['txtEdad'] = 'Edad del contacto obligatorio'
    elif not edad.isdigit() or int(edad) < 1 or int(edad) > 105:
        errores['txtEdad'] = 'Solo se permiten edades entre 1 y 105'

    if not errores:
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO Albums (Titulo, Artista, Año, Edad) VALUES (%s, %s, %s, %s)', (titulo, artista, año, edad))
            mysql.connection.commit()
            flash('Contacto guardado con éxito')
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
