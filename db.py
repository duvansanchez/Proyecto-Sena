import pyodbc

class DataBase:
    def __init__(self):
        self.inserts = {
            "dataUsuarios":"EXECUTE dbo.dataUsuarios @usuario=?, @cedula=?,@telefono=?,@correo=?,@contraseña=?",
            "dataPacientes":"EXECUTE dbo.dataPacientes @nombre = ?, @apellidos = ?, @nacimiento = ?, @tipo_identificacion = ?, @cedula = ?, @telefono = ?, @genero = ?, @nacionalidad = ?, @direccion = ?, @correo = ?",
            "dataMedicos":"EXECUTE dbo.dataMedicos @nombre=?,@apellidos=?,@nacimiento=?,@tipo_identificacion=?,@cedula=?,@telefono=?,@genero=?,@nacionalidad=?,@direccion=?,@correo=?,@especialidad=?,@usuario=?"
        }

        self.updates = {
            "result-status":"EXECUTE dbo.[updateBtts] @date_match=?,@name_main=?,@name_second=?,@possesion_m=?,@possesion_s=?,@shots_m=?,@shots_s=?,@xg_m=?,@xg_s=?,@result_ht=?,@result=?,@success=?"
        }
        
        self.validadores = {
            "validarPaciente":"SELECT TOP 1 cedula FROM pacientes where cedula = ?",
            "validarUsuario":"SELECT TOP 1 usuario FROM usuarios where usuario = ?",
            "validarUsuarioId":"SELECT TOP 1 cedula FROM usuarios where cedula = ?",
            "validarMedico":"SELECT TOP 1 cedula FROM medicos where cedula = ?",
            "validarMedicoUser":"SELECT TOP 1 usuario FROM medicos where usuario = ?",
            "validarLogin":"SELECT TOP 1 usuario FROM usuarios where usuario = ? and contraseña = ?"
        }
   
        self.consultas = {
            "especialidades":"SELECT especialidad FROM especialidades",
            "nacionalidades":"SELECT nacionalidad FROM nacionalidades",
            "generos":"SELECT genero FROM generos",
            "doctors":"SELECT * FROM medicos",
            "busqueda_usuario":"SELECT * FROM usuarios WHERE usuario = ? or cedula = ?",
            "busqueda_medico":"SELECT * FROM medicos WHERE nombre = ? or cedula = ?",
            "busqueda_paciente":"SELECT * FROM pacientes WHERE tipo_identificacion = ? and cedula = ?",
            "busqueda_citas":"SELECT c1.fecha,c1.hora_llegada,c1.codigo_paciente,c1.nombre_paciente,c1.medico,c1.nombre_medico,c1.salas,m1.especialidad FROM citas c1 INNER JOIN medicos m1 on c1.medico = m1.cedula WHERE c1.fecha = ?"
        }
        self.actualizar = {
            "actualizar_usuario": "UPDATE [dbo].[Usuarios] SET [usuario] = ?, [cedula] = ?, [telefono] = ?, [correo] = ?, [contraseña] = ? WHERE usuario = ? and cedula = ?",
            
            "actualizar_medico":"UPDATE [dbo].[Medicos] SET [nombre] = ?, [apellidos] = ?, [nacimiento] = ?, [tipo_identificacion] = ?, [cedula] = ?, [telefono] = ?, [genero] = ?, [nacionalidad] = ?, [direccion] = ?, [correo] = ?, [especialidad] = ?, [usuario] = ? WHERE usuario = ? and cedula = ?",
            
            "actualizar_paciente":"UPDATE [dbo].[Pacientes] SET [nombre] = ?, [apellidos] = ?, [nacimiento] = ?, [tipo_identificacion] = ?, [cedula] = ?, [telefono] = ?, [genero] = ?, [nacionalidad] = ?, [direccion] = ?, [correo] = ? WHERE tipo_identificacion = ? and cedula = ?"


        }
   
    def conexiondb(self):
        # Crear variables de entorno
        server = 'DESKTOP-T71IG1E' 
        database = 'PROYECTO SENA'
        username = 'sa'
        password = 'Infotec123'

        # Crea la cadena de conexión
        try:
            conexion_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            conexion = pyodbc.connect(conexion_string)
            cursor = conexion.cursor()
            
            return cursor,conexion
        
        except Exception as e:
            print(f"Error en la conexión: {e}")

    def insert(self,insert,values):
        cursor, conexion = self.conexiondb()

        try:
            obtener = cursor.execute(insert,values)

            # Confirma los cambios en la base de datos    
            conexion.commit()


            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()
            return True  

        except Exception as e:
            cursor.close()
            conexion.close()
            return True  

    def update(self, update, values):
        cursor, conexion = self.conexiondb()

        try:
            cursor.execute(update, values)
            conexion.commit()
            return True  
        except Exception as e:
            return False  
        finally:
            cursor.close()
            conexion.close()

    def select(self, query, values=()):
        cursor, conexion = self.conexiondb()

        try:
            cursor.execute(query, values)

            resultados = cursor.fetchall()  
            
            if len(resultados) == 0:
                return [['']]
            else:
                return resultados
        except Exception as e:
            print(f"Error al consultar datos: {e}")

        finally:
            # Cerrar el cursor y la conexión siempre, independientemente de si hubo un error
            cursor.close()
            conexion.close()

