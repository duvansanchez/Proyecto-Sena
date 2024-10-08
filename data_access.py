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
    
# Actualizaciones
    def actualizarUsuario(self,data):
        update = self.db.actualizar['actualizar_usuario']
        usuario = self.db.update(update,data)
        
        return 'Data actualizada correctamente'

# Insertaciones
    def crearUsuario(self, data):
        query_insert = self.db.inserts['dataUsuarios']
        insert = self.db.insert(query_insert,data)
        
        return insert


