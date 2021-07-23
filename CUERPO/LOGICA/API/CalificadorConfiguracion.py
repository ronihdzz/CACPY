import os


class CalificadorConfiguracion:
    def __init__(self,curso_nombre=None,curso_api_id=None,programTopic_nombre=None,
                 programTopic_id=None,retroTopic_nombre=None,retroTopic_id=None,
                 clase_nombreNbGrader=None):

        self.curso_api_id = curso_api_id
        self.curso_nombre=curso_nombre

        self.programTopic_id=programTopic_id
        self.programTopic_nombre=programTopic_nombre

        self.retroTopic_nombre=retroTopic_nombre
        self.retroTopic_id=retroTopic_id

        self.clase_nombreNbGrader=clase_nombreNbGrader


    def get_id_nombre_cursoClassroom(self):
        return self.curso_api_id,self.curso_nombre

    def get_id_nombre_topicClassroom(self):
        return self.programTopic_id,self.programTopic_nombre

    def get_nombre_cursoNbGrader(self):
        return self.clase_nombreNbGrader




    def reiniciarValores(self):
        self.curso_nombre = None
        self.curso_api_id = None
        self.programTopic_nombre = None
        self.programTopic_id=None
        self.retroTopic_nombre = None
        self.retroTopic_id = None
        self.clase_nombreNbGrader=None

    def cargarDatosCurso(self,id,nombre):
        self.reiniciarValores()
        self.curso_api_id = id
        self.curso_nombre=nombre

    def cargarDatosTopic(self,programaTopic_id,programaTopic_nombre):
        self.programTopic_id=programaTopic_id
        self.programTopic_nombre=programaTopic_nombre


    def datosListosApartadoTareas(self):
        if self.curso_api_id!=None and self.programTopic_id!=None and self.clase_nombreNbGrader!=None:
            return True
        else:
            return False

    def set_clase_nombreNbGrader(self,nuevoValor):
        self.clase_nombreNbGrader=nuevoValor


    def respaldarDatos(self,nombreArchivo):
        seDebeRespaldar= (self.curso_api_id!=None and self.programTopic_id!=None)
        archivoDatosExiste=os.path.isfile(nombreArchivo)

        datosRespaldar=(
            self.curso_api_id,
            self.programTopic_id
        )

        if seDebeRespaldar:
            with open(nombreArchivo,'w') as archivo:
                archivo.write(  '\n'.join( datosRespaldar )   )

        elif archivoDatosExiste:
            os.remove(nombreArchivo)

