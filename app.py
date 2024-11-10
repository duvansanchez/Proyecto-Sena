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

#TODO CONTRASEÑA ENCRIPTADA Y CONFIRMAR CONTRASEÑA
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
            
            if insert_usuario == True:
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
            
            if not actualizar_usuario:
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

# TODO PARA QUE CARGUEN LOS TIPOS DE CC
@app.route('/pacientes', methods=['GET','POST'])
@login_required
def pacientes():
    usuario_login = session.get('usuario')

    lista_de_campos = ['nombre', 'apellidos','nacimiento','tipo_identificacion', 'cedula', 'telefono', 'genero', 'nacionalidad','direccion','correo']
    recomendaciones = {}
    generos = dataQuery.generos()
    # TODO CARGAR MAS NACIONALIDADES
    nacionalidades = dataQuery.nacionalidades()
    recomendaciones.setdefault('generos',generos)
    recomendaciones.setdefault('nacionalidades',nacionalidades)

    data = {}
    

    if request.method == 'POST':
        accion = request.form.get('accion')

        for campo in request.form:
            data[campo] = request.form[campo]
        
        tipo_identificacion = data['tipo_identificacion']
        cedula_paciente = data['cedula']
        
        if accion == 'guardar':
            validar_paciente = dataQuery.validarPaciente(cedula_paciente)['data']

            if validar_paciente != '':
                flash('Ya existe un paciente con ese código.')
                return redirect(url_for('pacientes'))        
                    
            data_insert = [data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo']]
            insert_paciente = dataQuery.crearPaciente(data_insert)
           
            if insert_paciente == True:
                flash('Paciente creado correctamente')
                return redirect(url_for('pacientes'))
            else:
                flash('No se pudo realizar el insert')
                return redirect(url_for('pacientes')) 
            
        elif accion == 'buscar':
            parametros = [tipo_identificacion,cedula_paciente]
            buscar_paciente = dataQuery.busquedaPaciente(parametros)['result-busqueda']
            print(buscar_paciente)
            
            if buscar_paciente[0] == '':
                flash('No existe un paciente con ese tipo de documento y cedula')
                return redirect(url_for('pacientes'))
            else:
                data_busqueda = {
                    'nombre': buscar_paciente[0],
                    'apellidos': buscar_paciente[1],
                    'nacimiento': buscar_paciente[2],
                    'tipo_identificacion': buscar_paciente[3],
                    'cedula': buscar_paciente[4],
                    'telefono': buscar_paciente[5],
                    'nacionalidad': buscar_paciente[6],
                    'genero': buscar_paciente[7],
                    'direccion': buscar_paciente[8],
                    'correo': buscar_paciente[9]
                }
                return render_template('pacientes.html',  
                                    lista_de_campos=lista_de_campos, 
                                    usuario_login=usuario_login,
                                    recomendaciones=recomendaciones,
                                    data=data_busqueda
                                    )   
        elif accion == 'actualizar':
            data_original = json.loads(data['datosOriginales'])
            parametros = (data['nombre'], data['apellidos'], data['nacimiento'], data['tipo_identificacion'], data['cedula'], data['telefono'], data['genero'], data['nacionalidad'], data['direccion'], data['correo'], data_original['tipo_identificacion'], data_original['cedula'])

            
            actualizar_paciente = dataQuery.actualizarPaciente(parametros)
            
            if actualizar_paciente == False:
                flash('No se actualizaron los datos')
                return redirect(url_for('pacientes'))
            else:
                flash('Datos actualizados correctamente')
                return render_template('pacientes.html',  
                                    lista_de_campos=lista_de_campos, 
                                    usuario_login=usuario_login,
                                    recomendaciones=recomendaciones,
                                    data=data
                                    )
        else:
            print("No se reconoció la acción")
        
        
    return render_template('pacientes.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones, usuario_login=usuario_login, data=data)

@app.route('/medicos', methods=['GET','POST'])
@login_required
# TODO PARA QUE CARGUEN LOS TIPOS DE CC
def medicos():
    usuario_login = session.get('usuario')

    lista_de_campos = ['nombre', 'apellidos','nacimiento','tipo_identificacion', 'cedula', 'telefono', 'genero', 'nacionalidad','direccion','correo','especialidad','usuario']
    recomendaciones = {}
    generos = dataQuery.generos()
    especialidades = dataQuery.especialidades()
    # TODO CARGAR MAS NACIONALIDADES
    nacionalidades = dataQuery.nacionalidades()
    recomendaciones.setdefault('generos',generos)
    recomendaciones.setdefault('especialidades',especialidades)
    recomendaciones.setdefault('nacionalidades',nacionalidades)

    data = {}

    if request.method == 'POST':
        accion = request.form.get('accion')

        for campo in request.form:
            data[campo] = request.form[campo]
        
        medico = data['nombre']
        cedula_medico = data['cedula']
        medicoUser = data['usuario']

        if accion == 'guardar':
            consultar_medico = dataQuery.validarMedico(opcion=1,data=cedula_medico)['data']
            consultar_medico_user = dataQuery.validarMedico(opcion=2,data=medicoUser)['data']
            
            if consultar_medico != '':
                flash('Ya existe un medico con esa cedula')
                return redirect(url_for('medicos'))  

            if consultar_medico_user != '':
                flash('Ya existe un medico con ese usuario')
                return redirect(url_for('medicos'))
            
            data_insert = [data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo'],data['especialidad'],data['usuario']]
            insert_medico = dataQuery.crearMedico(data_insert)
            
            if insert_medico == True:
                flash('Medico creado correctamente')
                return redirect(url_for('medicos'))
            else:
                flash('No se pudo realizar el insert')
                return redirect(url_for('medicos')) 
              
        elif accion == 'buscar':
            parametros = [medico,cedula_medico]
            buscar_medico = dataQuery.busquedaMedico(parametros)['result-busqueda']
            
            if buscar_medico[0] == '':
                flash('No existe un medico con ese nombre o con esa cedula')
                return redirect(url_for('medicos'))
            else:
                data_busqueda = {
                    'nombre': buscar_medico[0],
                    'apellidos': buscar_medico[1],
                    'nacimiento': buscar_medico[2],
                    'tipo_identificacion': buscar_medico[3],
                    'cedula': buscar_medico[4],
                    'telefono': buscar_medico[5],
                    'genero': buscar_medico[6],
                    'nacionalidad': buscar_medico[7],
                    'direccion': buscar_medico[8],
                    'correo': buscar_medico[9],
                    'especialidad': buscar_medico[10],
                    'usuario': buscar_medico[11]
                }
                return render_template('medicos.html',  
                                    lista_de_campos=lista_de_campos, 
                                    usuario_login=usuario_login,
                                    recomendaciones=recomendaciones,
                                    data=data_busqueda
                                    )   
        elif accion == 'actualizar':     
            data_original = json.loads(data['datosOriginales'])
            parametros = (data['nombre'],data['apellidos'],data['nacimiento'],data['tipo_identificacion'],data['cedula'],data['telefono'],data['genero'],data['nacionalidad'],data['direccion'],data['correo'],data['especialidad'],data['usuario'],data_original['usuario'],data_original['cedula'])
            
            actualizar_medico = dataQuery.actualizarMedico(parametros)
            
            if actualizar_medico == False:
                flash('No se actualizaron los datos')
                return redirect(url_for('medicos'))
            else:
                flash('Datos actualizados correctamente')
                return render_template('medicos.html',  
                                    lista_de_campos=lista_de_campos, 
                                    usuario_login=usuario_login,
                                    recomendaciones=recomendaciones,
                                    data=data
                                    )
        else:
            print("No se reconoció la acción")
        
    return render_template('medicos.html', lista_de_campos=lista_de_campos, recomendaciones=recomendaciones, usuario_login=usuario_login, data=data)

# @app.route('/salas', methods=['GET','POST'])
# @login_required
# def salas():
    usuario_login = session.get('usuario')

    if request.method == 'POST':
        data = {}
        for campo in request.form:
            data[campo] = request.form[campo]

    #EDITAR
    lista_de_campos = ['sala-med','medicos']
    return render_template('salas.html',lista_de_campos=lista_de_campos)

# Ruta para renderizar la plantilla con las citas
@app.route('/citas', methods=['GET','POST'])
@login_required
def citas():
    usuario_login = session.get('usuario')
    citas = [{
                'id': '',
                'fecha': '',
                'hora_llegada': '',
                'codigo_paciente': '',
                'nombre_paciente': '',
                'medico': '',
                'nombre_medico': '',
                'sala': '',
                'especialidad':''
            }]
    
    if request.method == 'POST':
        data = {}
        
        for campo in request.form:
            data[campo] = request.form[campo]
            
        fecha_citas = data['fecha_citas']
        buscar_citas = dataQuery.busquedaCitas(fecha_citas)['result-busqueda']
        print(f"buscar_citas {buscar_citas[0]}")
        citas = []

        if buscar_citas[0][0] == '':
            return redirect(url_for('citas'))
        else:
            for cita in buscar_citas:
                paciente_cita= {
                    'fecha': cita[0],
                    'hora_llegada': cita[1],
                    'codigo_paciente': cita[2],
                    'nombre_paciente': cita[3],
                    'medico': cita[4],
                    'nombre_medico': cita[5],
                    'especialidad': cita[6]
                }
                citas.append(paciente_cita)
                    
        print(fecha_citas)
        return render_template('citas.html', usuario_login=usuario_login,fecha_citas=fecha_citas, citas=citas)   
    
    return render_template('citas.html', usuario_login=usuario_login,citas=citas, fecha_citas='')   
   
# Ruta para renderizar la plantilla con las citas
@app.route('/crearcitas', methods=['GET','POST'])
@login_required
def crearcitas():
    usuario_login = session.get('usuario')
    
    query_citas= db.select("SELECT me.cedula, CONCAT(me.nombre,' ',me.apellidos) nombre,me.especialidad, ho.dia, ho.inicio, ho.fin, ci.fecha, ci.hora_llegada FROM Medicos me INNER JOIN Horarios_Medicos ho ON ho.cedula = me.cedula INNER JOIN Citas ci on ci.medico = me.cedula")
    citas_medicos = dataQuery.estructurarMedicos(query_citas)
    
    query_especialidades = db.select("SELECT especialidad FROM Especialidades")
    especialidades = dataQuery.estructurarEspecialidades(query_especialidades)
    
    pacientes = [
    {
        "id": 1,
        "nombre": "Juan Carlos Pérez",
        "cedula": "123456789",
        "fecha_nacimiento": "1985-06-12",
        "telefono": "3123456789",
        "direccion": "Calle 12 #34-56",
        "email": "juan.perez@example.com"
    },
    {
        "id": 2,
        "nombre": "Ana María López",
        "cedula": "987654321",
        "fecha_nacimiento": "1990-09-23",
        "telefono": "3156789123",
        "direccion": "Carrera 45 #67-89",
        "email": "ana.lopez@example.com"
    },
    {
        "id": 3,
        "nombre": "Carlos Ramírez",
        "cedula": "456123789",
        "fecha_nacimiento": "1987-01-30",
        "telefono": "3101234567",
        "direccion": "Calle 45 #12-34",
        "email": "carlos.ramirez@example.com"
    }
    ]
        
    if request.method == 'POST':
        accion = request.form.get('accion')
        
        data = {}
        for campo in request.form:
            data[campo] = request.form[campo]
        
        if accion == "buscar_paciente":
            tipo_identificacion = 'CC' 
            cedula_paciente = data['cedula']
            parametros = [tipo_identificacion,cedula_paciente]
            
            buscar_paciente = dataQuery.busquedaPaciente(parametros)['result-busqueda']
            
            if buscar_paciente[0] == '':
                flash('No existe un paciente con esa cedula')
                return redirect(url_for('crearcitas'))
            else:
                cedula = buscar_paciente[4]
                nombre = buscar_paciente[0]
                apellidos = buscar_paciente[1]
                
                data_busqueda = f"{cedula} {nombre} {apellidos}"
                return render_template('crearcitas.html',usuario_login=usuario_login, pacientes=pacientes, especialidades=especialidades, medicos=citas_medicos,nombre_paciente=data_busqueda)  
             
        elif accion == "crear_cita":
            query = db.inserts['crear_cita']
            data = dataQuery.prepararDatosCitas(data)
            insert = db.insert(query,data)
            
            if insert is True:
                flash('Cita creada con exito')
                return redirect(url_for('crearcitas'))
            else:
                flash('No se pudo crear la cita medica')
                return redirect(url_for('crearcitas'))

    return render_template('crearcitas.html', usuario_login=usuario_login, pacientes=pacientes, especialidades=especialidades, medicos=citas_medicos)  

# Ruta para renderizar la plantilla con las citas
@app.route('/crearhorarios', methods=['GET','POST'])
@login_required
#FIXME NO ESTAN ELIMINANDO LOS HORARIOS
def crearhorarios():
    usuario_login = session.get('usuario')

    query_medicos = db.select("SELECT nombre,apellidos,cedula,especialidad FROM Medicos")
    medicos = []
    for index, (nombre, apellido, cedula, especialidad) in enumerate(query_medicos, start=1):
        medico = {
            "id": index,
            "nombre": nombre,
            "apellido": apellido,
            "cedula":cedula,
            "especialidad": especialidad
        }
        medicos.append(medico)
    
    query_especialidades = db.select("SELECT especialidad FROM Especialidades")
    especialidades = dataQuery.estructurarEspecialidades(query_especialidades)
    
    query_horarios_medicos = db.select("SELECT ho.dia,ho.inicio,ho.fin,m1.nombre,ho.cedula FROM Horarios_Medicos ho LEFT JOIN Medicos m1 ON m1.cedula = ho.cedula")
    horarios_medicos = ''
    if query_horarios_medicos[0][0] != '':
        horarios_medicos = dataQuery.estructurarHorarios(query_horarios_medicos)

    if request.method == 'POST':
        horarios = request.form.getlist('horarios[]')  
        print(f'Horarios encontrados {horarios}')
        
        horarios_decodificados = [json.loads(horario) for horario in horarios][0]
        print(f'Horarios decodificados {horarios_decodificados}')

        #Si el medico no tiene horarios decodificados entonces vaciar todos los horarios
        if horarios_decodificados == []:
            flash('El medico tiene que tener minimo un dia de horario creado')
            return redirect(url_for('crearhorarios'))   
        
        #TODO PROBAR CUANDO NO HAYA NINGUN HORARIO
        cont_elim = 0
        for horario in horarios_decodificados:
            nuevo_horario = [horario['dia'], horario['inicio'], horario['fin'], horario['medico'], horario['cedula']]
            
            cont_elim += 1
            if cont_elim <= 1:
                eliminar_horario = dataQuery.eliminarHorario([horario['cedula']])
            
            insert_horario = dataQuery.crearHorario(nuevo_horario)
            if not insert_horario:
                flash('No se pudo crear el horario')
                return redirect(url_for('crearhorarios'))   
           
            # if insert_horario:
            #     flash('Horario creado con exito')
            #     return redirect(url_for('crearhorarios'))   
            # else:
            #     flash('No se pudo crear el horario')
            #     return redirect(url_for('crearhorarios'))  

            # # Validar si ya tiene un horario creado
            # if validar_horario != '':
            #     print("ELIMINANDO HORARIO")
            #     eliminar_horario = dataQuery.eliminarHorario([horario['cedula'],horario['dia']])
            #     insert_horario = dataQuery.crearHorario(nuevo_horario)
            #     if insert_horario:
            #         flash('Horario creado con exito')
            #         return redirect(url_for('crearhorarios'))   
            #     else:
            #         flash('No se pudo crear el horario')
            #         return redirect(url_for('crearhorarios'))                                       

            # else:
            #     insert_horario = dataQuery.crearHorario(nuevo_horario)
            #     if insert_horario:
            #         flash('Horario creado con exito')
            #         return redirect(url_for('crearhorarios'))   
            #     else:
            #         flash('No se pudo crear el horario')
            #         return redirect(url_for('crearhorarios'))       
                 
        flash(f'Horarios medicos actualizados')
        return redirect(url_for('crearhorarios'))  
    
    return render_template('crearhorarios.html',usuario_login=usuario_login, medicos=medicos, especialidades=especialidades,horarios_medicos=horarios_medicos)  
if __name__ ==  '__main__': 
    app.run(host='localhost',port=5000,debug=True) 