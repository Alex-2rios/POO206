from flask import Flask, jsonify
from flask_mysqldb import MySQL
import MySQLdb
from config import Config  

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)

    # Rutas de manejo de errores y pruebas de conexión
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

    # Registrar el Blueprint
    from controllers.albumController import albumsBP
    app.register_blueprint(albumsBP)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=3000, debug=True)
