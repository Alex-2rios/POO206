from app import mysql

# Método para obtener albums activos
def getAll():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums WHERE State = 1')  # Filtra solo los albums activos
        consultaTodos = cursor.fetchall()
        cursor.close()
        return consultaTodos
    except Exception as e:
        mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
        raise Exception(f"Error al obtener todos los álbumes: {str(e)}")

# Método para obtener un album por ID
def getById(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM Albums WHERE id=%s', (id,))
        consultaId = cursor.fetchone()
        cursor.close()    
        return consultaId
    except Exception as e:
        mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
        raise Exception(f"Error al obtener el álbum con ID {id}: {str(e)}")

# Método para insertar un album
def insertAlbum(titulo, artista, año):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO Albums (Titulo, Artista, Año) VALUES (%s, %s, %s)', (titulo, artista, año))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
        raise Exception(f"Error al insertar el álbum: {str(e)}")

# Método para actualizar un album
def updateAlbum(id, titulo, artista, año):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Albums SET Titulo=%s, Artista=%s, Año=%s WHERE id=%s', (titulo, artista, año, id))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
        raise Exception(f"Error al actualizar el álbum con ID {id}: {str(e)}")

# Método para eliminar (soft delete) un album
def softDeleteAlbum(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE Albums SET State = 0 WHERE id = %s', (id,))
        mysql.connection.commit()
        cursor.close()
    except Exception as e:
        mysql.connection.rollback()  # Deshacer cualquier cambio en caso de error
        raise Exception(f"Error al eliminar el álbum con ID {id}: {str(e)}")
