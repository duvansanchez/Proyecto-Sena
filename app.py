import sys
from flask import Flask, render_template, request, make_response, flash, redirect, url_for
from cryptography.fernet import Fernet
from db import DataBase
from config import Config
from data_access import DataAccess
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config.from_object(Config)
db = DataBase()
dataQuery = DataAccess()

class User(UserMixin): #Heredando y añadiendo automáticamente todos los métodos y propiedades necesarios que Flask-Login requiere para gestionar la autenticación y las sesiones de usuario
    def __init__(self, id):
        self.id = id
        
# especialidades = db.select(db.consultas['especialidades'])

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = {}

        for campo in request.form:
            data[campo] = request.form[campo]
            
        clave = Fernet.generate_key()
        fernet = Fernet(clave)
        
        usuario =  request.form['usuario']
        contraseña = request.form['contraseña'].encode()

        # Encriptar la contraseña
        encrypted_password = fernet.encrypt(contraseña)
        print(f"Contraseña encriptada: {encrypted_password}")
        print(f"Clave de encriptación: {clave}")
                
        decrypted_password = fernet.decrypt(encrypted_password)
        print(f"Contraseña desencriptada: {decrypted_password.decode()}")
    return render_template('login.html')

@app.route('/usuario', methods=['GET','POST'])
def usuario():
    lista_de_campos = ['usuario', 'cedula', 'telefono', 'correo', 'contraseña', 'confirmar_contraseña']
    
    if request.method == 'POST':
        data = {}

        for campo in request.form:
            data[campo] = request.form[campo]
        
        usuario = data['usuario']
        usuarioid = data['cedula']
        data_usuario = list(dataQuery.validarUsuario(1,usuario))[0][0]
        data_usuarioid = list(dataQuery.validarUsuario(2,usuarioid))[0][0]
        
        if len(data_usuario) != 0:
            flash('Ya existe un usuario con ese user')
            return redirect(url_for('usuario'))  
        
        if len(data_usuarioid) != 0:
            flash('Ya existe un usuario con esa cedula')
            return redirect(url_for('usuario'))  
        

        
        insert = db.inserts['dataUsuarios']
        data_insert = [data['usuario'],data['cedula'],data['telefono'],data['correo'],data['contraseña']]
        db.insert(insert,data_insert)
        
        nombre = request.form.get('nombre')
        print(f"Nombre recibido: {nombre}")
    
    return render_template('usuario.html', lista_de_campos=lista_de_campos)

@app.route('/pacientes', methods=['GET','POST'])
def pacientes():
    lista_de_campos = ['nombre', 'apellidos','nacimiento','tipo_identificacion', 'cedula', 'telefono', 'genero', 'nacionalidad','direccion','correo']
    recomendaciones = {}
    generos = dataQuery.generos()
    nacionalidades = dataQuery.nacionalidades()
    recomendaciones.setdefault('generos',generos)
    recomendaciones.setdefault('nacionalidades',nacionalidades)


    if request.method == 'POST':
        data = {}

        for campo in request.form:
            data[campo] = request.form[campo]
        
        #Validar si ya existe el paciente
        paciente = data['cedula']
        data_paciente = list(dataQuery.validarPaciente(paciente))[0][0]
        
        if len(data_paciente) != 0:
            flash('Ya existe un paciente con ese código.')
            return redirect(url_for('pacientes'))        
                
        #Insertar paciente
        insert = db.inserts['dataPacientes']
        data_insert = [data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo']]
        db.insert(insert,data_insert)
        
    return render_template('pacientes.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones)

@app.route('/medicos', methods=['GET','POST'])
def medicos():
    lista_de_campos = ['nombre', 'apellidos','nacimiento','tipo_identificacion', 'cedula', 'telefono', 'genero', 'nacionalidad','direccion','correo','especialidad','usuario']
    recomendaciones = {}
    generos = dataQuery.generos()
    especialidades = dataQuery.especialidades()
    nacionalidades = dataQuery.nacionalidades()
    recomendaciones.setdefault('generos',generos)
    recomendaciones.setdefault('especialidades',especialidades)
    recomendaciones.setdefault('nacionalidades',nacionalidades)

    if request.method == 'POST':
        data = {}

        for campo in request.form:
            data[campo] = request.form[campo]

        medico = data['cedula']
        medicoUser = data['usuario']
        data_medico = list(dataQuery.validarMedico(opcion=1,data=medico))[0][0]
        data_medicoUser = list(dataQuery.validarMedico(opcion=2,data=medicoUser))[0][0]
        
        
        if len(data_medico) != 0:
            flash('Ya existe un medico con esa cedula')
            return redirect(url_for('medicos'))  

        if len(data_medicoUser) != 0:
            flash('Ya existe un medico con ese usuario')
            return redirect(url_for('medicos'))  
        
        insert = db.inserts['dataMedicos']
        data_insert = [data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo'],data['especialidad'],data['usuario']]
        db.insert(insert,data_insert)
        
    return render_template('medicos.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones)




if __name__ ==  '__main__': 
    app.run(host='localhost',port=5000,debug=True) 
    
