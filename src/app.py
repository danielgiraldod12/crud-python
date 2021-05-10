from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Configuracion de parametros de base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root@localhost/gogympy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Creamos los objetos globales del ORM y del Schema
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Clase User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cc = db.Column(db.String(15))
    idNum = db.Column(db.Integer)
    name = db.Column(db.String(30))
    email = db.Column(db.String(40))
    id_record_num = db.Column(db.Integer)
    id_training_program = db.Column(db.Integer)
    id_training_center = db.Column(db.Integer)
    password = db.Column(db.Integer)
    
    def __init__(self,cc,idNum,name,email,id_record_num,id_training_center,id_training_program,password):
        self.cc = cc
        self.idNum = idNum
        self.name = name
        self.email = email
        self.id_record_num = id_record_num
        self.id_training_center = id_training_center
        self.id_training_program = id_training_program
        self.password = password
    
db.create_all()

# Esquema User
class UserSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'cc',
            'idNum',
            'name',
            'email',
            'id_record_num',
            'id_training_center',
            'id_training_program',
            'password'
            )

user_schema = UserSchema()
users_schema = UserSchema(many=True)

# Clase asist
class Asist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    name = db.Column(db.String(30))
    record_num = db.Column(db.Integer)

    def __init__(self,id_user,name,record_num):
        self.id_user = id_user
        self.name = name
        self.record_num = record_num

db.create_all()

# Esquema Asist
class AsistSchema(ma.Schema):
    class Meta:
        fields = (
            'id',
            'id_user',
            'name',
            'record_num'
        )

asist_schema = AsistSchema()
asists_schema = AsistSchema(many=True)

# Ruta tabla asistencias
@app.route('/asists', methods=['GET'])
def asists():
    allAsists = Asist.query.all()
    result = users_schema.dump(allAsists)
    
    return render_template('asists.html', asists = allAsists)

# Rutas backend asistencias
@app.route('/asists/create/<id>')
def asist_create(id):
    user = User.query.get(id)
    id_user = user.id
    name = user.name
    if(user.id_record_num == 1):
        record_num = 2061250
    else:
        record_num = 2061277

    new_asist = Asist(id_user,name,record_num)
    db.session.add(new_asist)
    db.session.commit()

    return redirect(url_for('asists'))

@app.route('/asists/delete/<id>')
def asist_delete(id):
    asist = Asist.query.get(id)
    db.session.delete(asist)
    db.session.commit()

    return redirect(url_for('asists'))

# Rutas formularios y tablas usuarios
@app.route('/', methods=['GET'])
def home():
    allUsers = User.query.all()
    result = users_schema.dump(allUsers)

    return render_template('index.html', users = allUsers)

@app.route('/users/create')
def create_form():
    return render_template('create.html')

@app.route('/users/edit/<id>')
def edit_form(id):
    user = User.query.get(id)

    return render_template('edit.html', user = user)

# Rutas backend usuarios
@app.route('/users/store', methods=['POST'])
def create_user():
    cc = request.form['cc']
    idNum = request.form['idNum']
    name = request.form['name']
    email = request.form['email']
    id_record_num = request.form['id_record_num']
    id_training_center = request.form['id_training_center']
    id_training_program = request.form['id_training_program']
    password = request.form['password']

    new_user = User(cc,idNum,name,email,id_record_num,id_training_center,id_training_program,password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('home'))

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/users/update/<id>', methods=['POST'])
def edit_user(id):
    user = User.query.get(id)

    user.cc = request.form['cc']
    user.idNum = request.form['idNum']
    user.name = request.form['name']
    user.email = request.form['email']
    user.id_record_num = request.form['id_record_num']
    user.id_training_center = request.form['id_training_center']
    user.id_training_program = request.form['id_training_program']
    user.password = request.form['password']

    db.session.commit()
    return redirect(url_for('home'))

@app.route('/users/delete/<id>')
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('home'))

    
if __name__=="__main__":
    app.run(debug=True)