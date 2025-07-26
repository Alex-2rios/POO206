from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.albumModel import * 

albumsBP = Blueprint('albums', __name__)

# Ruta de inicio
@albumsBP.route('/')
def home():
    try:
        consultaTodos = getAll()
        return render_template('formulario.html', errores={}, albums=consultaTodos)
    except Exception as e:
        print('Error al consultar la base de datos:', e)
        return render_template('formulario.html', errores={}, albums=[])


# Ruta álbum detalles
@albumsBP.route('/detalle/<int:id>')
def detalle(id):
    try:
        consultaId = getById(id)
        return render_template('consulta.html', Albums=consultaId)
    except Exception as e:
        print('Error al consultar por id:', e)
        return redirect(url_for('albums.home'))


# Ruta para insertar un nuevo álbum
@albumsBP.route('/guardarAlbum', methods=['POST'])
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
        errores['txtAnio'] = 'En año solo ingresar un año válido'

    if not errores:
        try:
            insertAlbum(titulo, artista, año)
            flash('Álbum guardado con éxito')
            return redirect(url_for('albums.home'))
        except Exception as e:
            flash('Error al guardar: ' + str(e))
            return redirect(url_for('albums.home'))

    return render_template('formulario.html', errores=errores)


# Ruta para editar un álbum
@albumsBP.route('/editar/<int:id>', methods=['GET'])
def editar(id):
    try:
        album = getById(id)  # Obtener el álbum por ID
        if not album:
            flash('Álbum no encontrado')
            return redirect(url_for('albums.home'))
        return render_template('formUpdate.html', album=album)
    except Exception as e:
        print('Error al obtener álbum:', e)
        flash('Error al obtener el álbum para edición')
        return redirect(url_for('albums.home'))


# Ruta para actualizar un álbum
@albumsBP.route('/actualizarAlbum/<int:id>', methods=['POST'])
def actualizarAlbum(id):
    datos = request.form
    titulo = datos.get('txtTitulo', '').strip()
    artista = datos.get('txtArtista', '').strip()
    año = datos.get('txtAnio', '').strip()
    errores = {}

    if not titulo:
        errores['txtTitulo'] = 'El título es obligatorio'
    if not artista:
        errores['txtArtista'] = 'El artista es obligatorio'
    if not año:
        errores['txtAnio'] = 'El año es obligatorio'
    elif not año.isdigit() or int(año) < 1800 or int(año) > 2030:
        errores['txtAnio'] = 'Ingrese un año válido'

    if errores:
        return render_template('formUpdate.html', album=(id, titulo, artista, año), errores=errores)

    try:
        updateAlbum(id, titulo, artista, año)
        flash('Álbum actualizado correctamente')
    except Exception as e:
        flash('Error al actualizar: ' + str(e))

    return redirect(url_for('albums.home'))


# Ruta para eliminar un álbum (soft delete)
@albumsBP.route('/eliminar/<int:id>', methods=['GET'])
def eliminar(id):
    try:
        album = getById(id)  # Obtener el álbum por ID
        if not album:
            flash('Álbum no encontrado')
            return redirect(url_for('albums.home'))
        return render_template('confirmDel.html', album=album)
    except Exception as e:
        flash('Error al cargar álbum: ' + str(e))
        return redirect(url_for('albums.home'))


# Ruta para confirmar la eliminación del álbum (soft delete)
@albumsBP.route('/eliminarConfirmado/<int:id>', methods=['POST'])
def eliminarConfirmado(id):
    try:
        softDeleteAlbum(id)  # Función para realizar el soft delete (marcar el álbum como eliminado)
        flash('Álbum eliminado correctamente de la base de datos')
    except Exception as e:
        flash('Error al eliminar: ' + str(e))
    return redirect(url_for('albums.home'))
