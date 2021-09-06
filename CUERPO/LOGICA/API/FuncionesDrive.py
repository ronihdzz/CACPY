


def getId_carpeta(nombre,idCarpetaAlmacena,intermediarioAPI_drive):
    '''
    Accede a la carpeta cuyo id es igual al valor que almacenara el parametro
    'idCarpetaAlmacena', una vez accedido a la carpeta prosigue a buscar una
    carpeta con el nombre del valor que almacenara el parametro 'nombre'.Una
    vez hecho lo anterior pueden ocurrir dos cosas:
        A) Si no encuentra la carpeta la creara y posteriormente retornara
        su ID
        B) Si si encuentra la carpeta unicamente obtendra su ID y posteriormente
        la retornara

    Parámetros:
        nombre (str): Nombre de la carpeta de la cual se desea obtener su ID
        idCarpetaAlmacena (str) : Id de la carpeta que almacena la carpeta
        de la cual queremos obtener su ID
        intermediarioApi_drive : El objeto que nos permitira hacer consultas
        y recivir respuestas por parte de la API

    Returns:
        Retornara un diccionario con los siguientes datos en caso de NO existir ningun error:
            {
                'exito':True
                'resultado': {
                                'name':
                                'id':
                                'webContentLink':
                                'webViewLink':
                            }
            }
        Retornara un diccionario con los siguientes datos en caso de SI existir algun error:
            {
                'exito':False
                'resultado': 'Explicacion del error presentado'
            }
    '''

    errorPresentado={
        'explicacion':'',
        'exception': ''
    }

    resultado={
        'exito':False,
        'resultado':''
    }

    page_token=None


    try:
        # Lo que se busca es una CARPETA, la carpeta que se busca NO SE ENCUENTRA en la papelera de reciclaje
        # la carpeta que se busca se encuentra dentro de la carpeta  cuyo id es igual a un id especifico
        query = "trashed=False and mimeType='application/vnd.google-apps.folder' and name='{}'   and  '{}' in parents".format(
            nombre, idCarpetaAlmacena)

        listaResultados = []
        while True:
            response = intermediarioAPI_drive.files().list(
                q=query,
                spaces='drive',
                #fields='nextPageToken, files(id, name)',  webContentLink,webViewLink
                fields='nextPageToken,files(id,name,webContentLink,webViewLink)',
                pageToken=page_token).execute()

            for file in response.get('files', []):
                # Process change
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                listaResultados.append(
                    [
                        file.get('name'),
                        file.get('id'),
                        file.get('webContentLink'),
                        file.get('webViewLink')
                    ]
                )



            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        if listaResultados != []:
            # Si solo existe una carpeta con dicho nombre y especificaciones se obtiene su ID
            if len(listaResultados) == 1:
                resultado['resultado']={
                    'name': listaResultados[0][0],
                    'id':listaResultados[0][1],
                    'webContentLink':listaResultados[0][2],
                    'webViewLink':listaResultados[0][3]
                }
                resultado['exito']=True

            # Si existe mas de una carpeta con dicho nombre y especificaciones entonces hay un error
            else:
                errorPresentado['explicacion'] = f'Se encontro mas de una carpeta con el nombre de: {nombre} ' \
                                                 f'dentro de la carpeta con id: {idCarpetaAlmacena} es importante ' \
                                                 f'atenderlo por que esto puede causar problemas futuros'
                errorPresentado['exception'] = 'Ninguna'

        # Si no existe la carpeta buscada entonces se va a crear
        else:
            try:
                file_metadata = {
                    'name': nombre,
                    'parents': [idCarpetaAlmacena],
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                file = intermediarioAPI_drive.files().create(
                    body=file_metadata,
                    fields='id,name,webContentLink,webViewLink'
                    #fields='id'
                    #fields='files(id,name,webContentLink,webViewLink)'
                ).execute()

                resultado['exito']=True
                resultado['resultado']={
                    'name': file.get('name'),
                    'id':file.get('id'),
                    'webContentLink':file.get('webContentLink'),
                    'webViewLink':file.get('webViewLink')
                }

            except Exception as e:
                errorPresentado['explicacion'] = f'Ocurrio un error al crear la carpeta con el nombre: {nombre} en la carpeta ' \
                                     f'con id: {idCarpetaAlmacena} '
                errorPresentado['exception'] = e


    except Exception as e:
        errorPresentado['explicacion']=f'Ocurrio un error al buscar la carpeta con el nombre: {nombre} en la carpeta ' \
                                       f'con id: {idCarpetaAlmacena} '
        errorPresentado['exception']=e


    if resultado['exito'] is False:

        resultado['resultado']=f"Error explicado:{errorPresentado['explicacion']} " \
                               f"Exception:{errorPresentado['exception']}"


    return resultado







