from db import DataBase
class DataAccess:
    def __init__(self):
        self.db = DataBase()
        
#Validadores
    def validarPaciente(self,paciente):
        query = self.db.validadores['validarPaciente']
        resultados = self.db.select(query,paciente)
        return resultados
    
    def validarUsuario(self,opcion,data):
        #Validar si existe ya un usuario con ese user
        if opcion == 1:
            query = self.db.validadores['validarUsuario']
            resultados = self.db.select(query,data)
            return resultados
        
        #Validar si existe ya un usuario con esa cedula
        if opcion == 2:
            query = self.db.validadores['validarUsuarioId']
            resultados = self.db.select(query,data)
            return resultados

    def validarMedico(self,opcion,data):
        #Validar si existe ya un medico con esa cedula
        if opcion == 1:
            query = self.db.validadores['validarMedico']
            resultados = self.db.select(query,data)
            return resultados
        
        #Validar si existe ya un medico con ese usuario
        if opcion == 2:
            query = self.db.validadores['validarMedicoUser']
            resultados = self.db.select(query,data)
            return resultados

#Cargar Informacion
    def especialidades(self):
        especialidades = self.db.select(self.db.consultas['especialidades'])
        return especialidades
    
    def nacionalidades(self):
        nacionalidades = self.db.select(self.db.consultas['nacionalidades'])
        return nacionalidades
    
    def generos(self):
        generos = self.db.select(self.db.consultas['generos'])
        return generos