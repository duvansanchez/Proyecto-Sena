import sys
import json
from flask import Flask, render_template, request, session, flash, redirect, url_for, send_from_directory
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

# @app.route('/static/js/<path:filename>')
# def serve_js(filename):
#     return send_from_directory('static/js', filename, mimetype='application/javascript')

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
        
        validar_usuario = list(dataQuery.validarLogin(data=data_validate))[0][0]

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
    
    lista_de_campos = ['usuario', 'cedula', 'telefono', 'correo', 'contraseña', 'confirmar_contraseña']
    
    if request.method == 'POST':
        data = {}
        
        accion = request.form.get('accion')

        for campo in request.form:
            data[campo] = request.form[campo]
            
        usuario = data['usuario']
        cedula_usuario = data['cedula']

        if accion == 'guardar':
            data_usuario = dataQuery.validarUsuario(opcion=1,data=usuario)['data']
            data_usuarioid = dataQuery.validarUsuario(opcion=2,data=cedula_usuario)['data']
            
            if len(data_usuario) != 0:
                flash('Ya existe un usuario con ese user')
                return redirect(url_for('usuario'))  
            
            if len(data_usuarioid) != 0:
                flash('Ya existe un usuario con esa cedula')
                return redirect(url_for('usuario'))  
            
            
            data_insert = [data['usuario'],data['cedula'],data['telefono'],data['correo'],data['contraseña']]
            insert_usuario = dataQuery.crearUsuario(data_insert)
            
            if insert_usuario == 'Insert hecho correctamente':
                flash('Usuario creado correctamente')
                return redirect(url_for('usuario'))
            else:
                flash('No se pudo realizar el insert')
                return redirect(url_for('usuario'))
                
       
        elif accion == 'buscar':
            parametros = [usuario,cedula_usuario]
            buscar_usuario = dataQuery.busquedaUsuario(parametros)['result-busqueda']
            
            if buscar_usuario[0] == '':
                flash('No existe un usuario con ese user o con esa cedula')
                return redirect(url_for('usuario'))
            else:
                return render_template('usuario.html',  
                                    lista_de_campos=lista_de_campos, 
                                    usuario_login=usuario_login,
                                    usuario=buscar_usuario[0],
                                    cedula=buscar_usuario[1],
                                    telefono=buscar_usuario[2],
                                    correo=buscar_usuario[3],
                                    contraseña=buscar_usuario[4]
                                    )   
        
        elif accion == 'actualizar':
            data_original = json.loads(data['datosOriginales'])
            parametros = (data['usuario'], data['cedula'], data['telefono'], data['correo'], data['contraseña'], data_original['usuario'], data_original['cedula'])
            
            actualizar_usuario = dataQuery.actualizarUsuario(parametros)
            
            if len(actualizar_usuario) == 0:
                flash('No se actualizaron los datos')
                return redirect(url_for('usuario'))
            else:
                flash('Datos actualizados correctamente')
                return render_template('usuario.html',  
                                    lista_de_campos=lista_de_campos, 
                                    usuario_login=usuario_login,
                                    usuario=data['usuario'],
                                    cedula=data['cedula'],
                                    telefono=data['telefono'],
                                    correo=data['correo'],
                                    contraseña=data['contraseña']
                                    )
        else:
            print("No se reconoció la acción")
        
    
    return render_template('usuario.html', lista_de_campos=lista_de_campos, usuario_login=usuario_login,usuario='',cedula='',telefono='',correo='',contraseña='')

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
    doctors = dataQuery.doctors()
    print(doctors)
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

        consultar_medico = dataQuery.validarMedico(opcion=1,data=medico)['data']
        consultar_medico_user = dataQuery.validarMedico(opcion=2,data=medicoUser)['data']
        print(f'"{len(consultar_medico)}"')
        print(f'"{len(consultar_medico_user)}"')
        
        if consultar_medico != '':
            flash('Ya existe un medico con esa cedula')
            return redirect(url_for('medicos'))  

        if consultar_medico_user != '':
            flash('Ya existe un medico con ese usuario')
            return redirect(url_for('medicos'))  
        
        insert = db.inserts['dataMedicos']
        data_insert = [data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo'],data['especialidad'],data['usuario']]
        db.insert(insert,data_insert)
        
    return render_template('medicos.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones, usuario_login=usuario_login)

@app.route('/salas', methods=['GET','POST'])
@login_required
def salas():
    usuario_login = session.get('usuario')

    if request.method == 'POST':
        data = {}
        for campo in request.form:
            data[campo] = request.form[campo]

    #EDITAR
    lista_de_campos = ['sala-med','medicos']
    return render_template('salas.html',lista_de_campos=lista_de_campos)

@app.route('/buscador', methods=['GET','POST'])
@login_required
def buscador():
    usuario_login = session.get('usuario')

    if request.method == 'POST':
        data = {}
        for campo in request.form:
            data[campo] = request.form[campo]

    #EDITAR
    lista_de_campos = ['sala-med','medicos']
    
    return render_template('buscador.html',lista_de_campos=lista_de_campos)

if __name__ ==  '__main__': 
    app.run(host='localhost',port=5000,debug=True) 