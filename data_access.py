from collections import defaultdict
from db import DataBase

class DataAccess:
    def __init__(self):
        self.db = DataBase()
        
# Validadores
    def validarPaciente(self,data):
        query = self.db.validadores['validarPaciente']
        resultado = self.db.select(query,data)[0][0]
        
        row = {}
        row['data'] = resultado
        return row  
   
    def validarUsuario(self,opcion,data):
        #Validar si existe ya un usuario con ese user
        if opcion == 1:
            query = self.db.validadores['validarUsuario']
            resultado = self.db.select(query,data)[0][0]
            
            row = {}
            row['data'] = resultado
            return row
        
        #Validar si existe ya un usuario con esa cedula
        if opcion == 2:
            query = self.db.validadores['validarUsuarioId']
            resultado = self.db.select(query,data)[0][0]
            
            row = {}
            row['data'] = resultado
            return row

    def validarMedico(self,opcion,data):
        #Validar si existe ya un medico con esa cedula
        if opcion == 1:
            query = self.db.validadores['validarMedico']
            resultado = self.db.select(query,data)[0][0]
            
            row = {}
            row['data'] = resultado
            return row
        
        #Validar si existe ya un medico con ese usuario
        if opcion == 2:
            query = self.db.validadores['validarMedicoUser']
            resultado = self.db.select(query,data)[0][0]

            row = {}
            row['data'] = resultado
            return row

    def validarLogin(self,data):
        query = self.db.validadores['validarLogin']
        resultado = self.db.select(query,data)[0][0]

        if len(resultado) > 0:
            return True
        else:
            return False
    
    def validarHorarios(self,data):
        query = self.db.validadores['validarHorario']
        resultado = self.db.select(query,data)[0]

        row = {}
        row['data'] = resultado
        return row
    
# Cargar informacion por defecto
    def especialidades(self):
        query = self.db.consultas['especialidades']
        especialidades = self.db.select(query)
        return especialidades
    
    def nacionalidades(self):
        query = self.db.consultas['nacionalidades']
        nacionalidades = self.db.select(query)
        return nacionalidades
    
    def generos(self):
        query =  self.db.consultas['generos']
        generos = self.db.select(query)
        return generos
    
    def tipocc(self):
        query =  self.db.consultas['tipocc']
        generos = self.db.select(query)
        return generos
    
    def doctors(self):
        query = self.db.consultas['doctors']
        doctors = self.db.select(query)
        return doctors

# Busquedas
    def busquedaUsuario(self,data):
        query = self.db.consultas['busqueda_usuario']
        usuario = self.db.select(query,data)[0]
        
        row = {}
        row['result-busqueda'] = usuario
        return row
    
    def busquedaMedico(self,data):
        query = self.db.consultas['busqueda_medico']
        medico = self.db.select(query,data)[0]
        
        row = {}
        row['result-busqueda'] = medico
        return row
    
    def busquedaPaciente(self,data):
        query = self.db.consultas['busqueda_paciente']
        paciente = self.db.select(query,data)[0]
        
        row = {}
        row['result-busqueda'] = paciente
        return row
    
    def busquedaCitas(self,data):
        query = self.db.consultas['busqueda_citas']
        citas = self.db.select(query,data)
        
        row = {}
        row['result-busqueda'] = citas
        return row
    

    
# Actualizaciones
    def actualizarUsuario(self,data):
        update = self.db.actualizar['actualizar_usuario']
        usuario = self.db.update(update,data)
        
        return usuario
    
    def actualizarMedico(self,data):
        update = self.db.actualizar['actualizar_medico']
        medico = self.db.update(update,data)
        
        return medico
    
    def actualizarPaciente(self,data):
        update = self.db.actualizar['actualizar_paciente']
        paciente = self.db.update(update,data)
        
        return paciente

# Insertaciones
    def crearUsuario(self, data):
        query_insert = self.db.inserts['dataUsuarios']
        insert = self.db.insert(query_insert,data)
        
        return insert
    
    def crearMedico(self, data):
        query_insert = self.db.inserts['dataMedicos']
        insert = self.db.insert(query_insert,data)
        
        return insert
    
    def crearPaciente(self, data):
        query_insert = self.db.inserts['dataPacientes']
        insert = self.db.insert(query_insert,data)
        
        return insert
   
    def crearHorario(self, data):
        query_insert = self.db.inserts['crear_horario']
        insert = self.db.insert(query_insert,data)
        
        return insert

# Limpieza de datos
    def estructurarMedicos(self,resultado_query):
        # Diccionario para agrupar médicos por cédula
        medicos_dict = defaultdict(lambda: {
            "nombre": "",
            "especialidad": "",
            "horarios": [],
            "citas": []
        })

        for fila in resultado_query:
            # Verificar si la fila tiene 8 o 7 valores
            if len(fila) == 8:
                cedula, nombre_medico, especialidad, dia, inicio, fin, fecha, hora_llegada = fila
            elif len(fila) == 7:
                cedula, nombre_medico, especialidad, dia, inicio, fin, fecha = fila
                hora_llegada = None
            else:
                raise ValueError("La fila no tiene el número correcto de columnas.")
            
            # Si este médico ya existe en el diccionario, solo agregamos horarios y citas
            if not medicos_dict[cedula]["nombre"]:
                medicos_dict[cedula]["nombre"] = nombre_medico
                medicos_dict[cedula]["especialidad"] = especialidad

            # Agregar horario si no está duplicado
            horario = {"dia": dia, "inicio": inicio, "fin": fin}
            if horario not in medicos_dict[cedula]["horarios"]:
                medicos_dict[cedula]["horarios"].append(horario)

            # Agregar cita si no está duplicada
            if fecha and hora_llegada:
                cita = {"fecha": str(fecha), "hora": str(hora_llegada)}
                if cita not in medicos_dict[cedula]["citas"]:
                    medicos_dict[cedula]["citas"].append(cita)

        # Convertir el diccionario en una lista de médicos con la estructura deseada y orden de claves
        medicos_estructurados = []
        for cedula, datos in medicos_dict.items():
            medico_ordenado = {
                "id": cedula,  # Primer campo
                "nombre": datos["nombre"],  # Segundo campo
                "especialidad": datos["especialidad"],  # Tercer campo
                "horarios": datos["horarios"],  # Cuarto campo
                "citas": datos["citas"]  # Quinto campo
            }
            medicos_estructurados.append(medico_ordenado)

        return medicos_estructurados
    
    def estructurarEspecialidades(self,query_especialidades):
        especialidades = []
        for especialidad in query_especialidades: 
            especialidades.append(especialidad[0])
        return especialidades

    def estructurarHorarios(self,horarios):
        horariosDoctores = []
        for dia, inicio, fin, nombre, cedula in horarios:
            horario = {
                'cedula': cedula,
                'dia': dia,
                'inicio': inicio,
                'fin': fin,
                'medico': nombre
            }
            horariosDoctores.append(horario)
        return horariosDoctores
    
    def prepararDatosCitas(self,data):
        codigo_paciente, nombre_paciente = data['nombre_paciente'].split(' ', 1)
        medico_id, nombre_medico = data['nombre_medico'].split(' - ', 1)
        data = {
            'fecha': data['fecha_cita'],
            'hora_llegada': data['hora_cita'],
            'codigo_paciente': codigo_paciente,
            'nombre_paciente': nombre_paciente,
            'medico': medico_id.strip(),  
            'nombre_medico': nombre_medico.strip()  
        }
        valores = (
            data['fecha'],
            data['hora_llegada'],
            data['codigo_paciente'],
            data['nombre_paciente'],
            data['medico'],
            data['nombre_medico']
        )
        return valores

# Eliminar datos
    def eliminarHorario(self,data):
        query_delete = self.db.deletes['deleteHorarios']
        delete = self.db.delete(query_delete,data)
        
        return delete
