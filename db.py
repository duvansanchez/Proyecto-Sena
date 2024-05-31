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
            "validarMedicoUser":"SELECT TOP 1 usuario FROM medicos where usuario = ?" 
        }
   
        self.consultas = {
            "especialidades":"SELECT especialidad FROM especialidades",
            "nacionalidades":"SELECT nacionalidad FROM nacionalidades",
            "generos":"SELECT genero from generos"
        }
    def conexiondb(self):
        # Crear variables de entorno
        server = 'DESKTOP-AK1M9SS' 
        database = 'PROYECTO SENA'
        username = 'sa'
        password = 'Infotec123'

        # Crea la cadena de conexión
        try:
            conexion_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"
            conexion = pyodbc.connect(conexion_string)
            cursor = conexion.cursor()
            
            print(f"Exito en la conexión")
            
            return cursor,conexion
        except Exception as e:
            print(f"Error en la conexión: {e}")

    def insert(self,insert,values):
        cursor, conexion = self.conexiondb()

        try:
            obtener = cursor.execute(insert,values)

            # Confirma los cambios en la base de datos    
            conexion.commit()

            print("Procedimiento almacenado ejecutado exitosamente.")

            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()

        except Exception as e:
            print(f"Error en la conexión: {e}")
            cursor.close()
            conexion.close()

    def update(self,update,values):
        cursor, conexion = self.conexiondb()

        try:
            obtener = cursor.execute(update,values)

            # Confirma los cambios en la base de datos
            conexion.commit()

            print("Procedimiento almacenado ejecutado exitosamente.")

            # Cierra el cursor y la conexión
            cursor.close()
            conexion.close()

        except Exception as e:
            print(f"Error en la conexión: {e}")
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
                print("Consulta hecha correctamente")
                print(resultados)
                return resultados
        except Exception as e:
            print(f"Error en la conexión: {e}")

        finally:
            # Cerrar el cursor y la conexión siempre, independientemente de si hubo un error
            cursor.close()
            conexion.close()

