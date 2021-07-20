from nbgrader.apps import NbGraderAPI
from traitlets.config import Config

# create a custom config object to specify options for nbgrader
config = Config()
config.CourseDirectory.course_id = "course_1"
config.CourseDirectory.root='NB_GRADER/course_1/'


'''
https://nbgrader.readthedocs.io/en/stable/configuration/config_options.html

CourseDirectory.autograded_directory Unicode
Defecto: 'autograded'
El nombre del directorio que contiene los envíos de tareas después 
de que se hayan calificado automáticamente.


CourseDirectory.feedback_directory Unicode
Defecto: 'feedback'
El nombre del directorio que contiene comentarios sobre la tarea después de que se 
haya completado la calificación.

CourseDirectory.release_directory Unicode
Defecto: 'release'
El nombre del directorio que contiene la versión de la tarea que se entregará a 
los estudiantes.

CourseDirectory.root Unicode
Defecto: ''
El directorio raíz de los archivos del curso (que incluye los directorios fuente , d
e publicación , enviados , autograbados , etc.). Por defecto, el directorio de trabajo actual.


CourseDirectory.release_directory Unicode
Defecto: 'release'
El nombre del directorio que contiene la versión de la tarea que se entregará a los estudiantes. 
Esto corresponde a la variable nbgrader_step en la opción de configuración directory_structure .


CourseDirectory.source_directory Unicode
Defecto: 'source'
El nombre del directorio que contiene la versión maestro / instructor de las asignaciones. 

CourseDirectory.submitted_directory Unicode
Defecto: 'submitted'
El nombre del directorio que contiene las tareas que los estudiantes han enviado para su calificación.
'''



#config.JupyterApp.config_fileUnicode='NB_GRADER/course_1/nbgrader_config.py'
#config.JupyterApp.config_file_nameUnicode='NB_GRADER/course_1/nbgrader_config.py'

# https://nbgrader.readthedocs.io/en/stable/api/high_level_api.html#nbgrader.apps.api.NbGraderAPI.get_released_assignments
api = NbGraderAPI(config=config)
all_assignments_names = api.get_source_assignments()


print(all_assignments_names)

asignacion_id='tarea_1'
estudiante_id='114283316418743255552'

# calificacion
resultado=api.autograde(assignment_id=asignacion_id, student_id=estudiante_id)
print("Resultado:",resultado)

print("*"*100)
if resultado['success'] is True:
    calif=api.get_submission(assignment_id=asignacion_id, student_id=estudiante_id)
    puntosObtenidos=calif['score']
    puntosTotales=calif['max_score']
    print(puntosObtenidos,'/',puntosTotales)
