import sys
from flask import Flask, render_template, request, session, flash, redirect, url_for
from cryptography.fernet import Fernet
from db import DataBase
from config import Config
from data_access import DataAccess
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db = DataBase()
dataQuery = DataAccess()

# DECORADORES
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# END POINTS
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
        data_validate = [usuario,contraseña]
        
        validar_usuario = list(dataQuery.validarLogin(data_validate))[0][0]

        if len(validar_usuario) == 0:
            print('Credenciales incorrectas')
            flash('Credenciales incorrectas')
            return redirect(url_for('login'))  
        else:
            session['usuario'] = usuario  # Almacena el nombre de usuario en la sesión
            return redirect(url_for('usuario'))

    return render_template('login.html')

@app.route('/usuario', methods=['GET','POST'])
@login_required
def usuario():
    usuario_login = session.get('usuario')

    # NUEVO
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
        
        nombre = request.form.get('usuario')
        print(f"Nombre recibido: {nombre}")
    
    return render_template('usuario.html', lista_de_campos=lista_de_campos, usuario_login=usuario_login)

@app.route('/pacientes', methods=['GET','POST'])
@login_required
def pacientes():
    usuario_login = session.get('usuario')

    # NUEVO
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
        
    return render_template('pacientes.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones, usuario_login=usuario_login)

@app.route('/medicos', methods=['GET','POST'])
@login_required
def medicos():
    usuario_login = session.get('usuario')

    # NUEVO
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
        consultar_medico = list(dataQuery.validarMedico(opcion=1,data=medico))[0][0]
        consultar_medico_user = list(dataQuery.validarMedico(opcion=2,data=medicoUser))[0][0]
        
        if len(consultar_medico) != 0:
            flash('Ya existe un medico con esa cedula')
            return redirect(url_for('medicos'))  

        if len(consultar_medico_user) != 0:
            flash('Ya existe un medico con ese usuario')
            return redirect(url_for('medicos'))  
        
        insert = db.inserts['dataMedicos']
        data_insert = [data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo'],data['especialidad'],data['usuario']]
        db.insert(insert,data_insert)
        
    return render_template('medicos.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones, usuario_login=usuario_login)


if __name__ ==  '__main__': 
    app.run(host='localhost',port=5000,debug=True) 
    
