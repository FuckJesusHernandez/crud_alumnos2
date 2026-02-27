import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

# crear instancia
app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modelo de la base de datos
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'

    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return {
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre,
        }


# ======================
# VISTAS HTML
# ======================

# Ruta raiz
@app.route('/estudiantes', methods=['GET'])
def index():
    estudiantes = Estudiante.query.all()
    return render_template('index.html', estudiantes=estudiantes)


# Crear estudiante (FORM)
@app.route('/estudiantes/new', methods=['GET', 'POST'])
def create_estudiante():
    if request.method == 'POST':

        nvo_estudiante = Estudiante(
            no_control=request.form['no_control'],
            nombre=request.form['nombre'],
            ap_paterno=request.form['ap_paterno'],
            ap_materno=request.form['ap_materno'],
            semestre=int(request.form['semestre'])
        )

        db.session.add(nvo_estudiante)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('create_estudiante.html')


# Actualizar estudiante (FORM)
@app.route('/estudiantes/update/<string:no_control>', methods=['GET', 'POST'])
def update_estudiante_view(no_control):

    estudiante = db.session.get(Estudiante, no_control)

    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.ap_paterno = request.form['ap_paterno']
        estudiante.ap_materno = request.form['ap_materno']
        estudiante.semestre = int(request.form['semestre'])

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_estudiante.html', estudiante=estudiante)


# Eliminar estudiante
@app.route('/estudiantes/delete/<string:no_control>')
def delete_estudiante(no_control):

    estudiante = db.session.get(Estudiante, no_control)

    if estudiante:
        db.session.delete(estudiante)
        db.session.commit()

    return redirect(url_for('index'))


# ======================
# API REST (JSON)
# ======================

# Insertar estudiante (API)
@app.route('/estudiantes', methods=['POST'])
def insert_estudiante():

    data = request.get_json()

    if not data:
        return jsonify({'msg': 'JSON inválido'}), 400

    nuevo_estudiante = Estudiante(
        no_control=data['no_control'],
        nombre=data['nombre'],
        ap_paterno=data['ap_paterno'],
        ap_materno=data['ap_materno'],
        semestre=data['semestre']
    )

    db.session.add(nuevo_estudiante)
    db.session.commit()

    return jsonify({'msj': 'Estudiante agregado correctamente'})


# Actualizar estudiante (API)
@app.route('/estudiantes/<string:no_control>', methods=['PUT'])
def update_estudiante_api(no_control):

    estudiante = db.session.get(Estudiante, no_control)

    if estudiante is None:
        return jsonify({'msg': 'Estudiante no encontrado'}), 404

    data = request.get_json()

    if "nombre" in data:
        estudiante.nombre = data['nombre']
    if "ap_paterno" in data:
        estudiante.ap_paterno = data['ap_paterno']
    if "ap_materno" in data:
        estudiante.ap_materno = data['ap_materno']
    if "semestre" in data:
        estudiante.semestre = data['semestre']

    db.session.commit()

    return jsonify({'msg': 'Estudiante actualizado correctamente'})


# ======================
# RUN
# ======================
if __name__ == '__main__':
    app.run(debug=True)