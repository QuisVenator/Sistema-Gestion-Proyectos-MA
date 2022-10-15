


from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from usuario.utils import validarPermisos,getUsuarioSesion,getIdScrumRol,getProyectsByUsuarioID,getProyectsByID,getRolByProyectId,getColaboratorsByProyect,getTipoUsbyProyectId,getTipoUsbyNotProyectId,getRolByID
from usuario.models import Usuario,Cliente,Proyecto,MiembroEquipo,Permiso,Rol,ProyectoRol,TipoUserStory,PrioridadTUs,UserStory,FaseTUS,Fase
from django.template import loader
from django.db.models import Q

# Create your views here.
def login(request):
    """
    Metodo de redireccion del login para poder ingresar mediante sso
    """
    return render(request,'accounts/login.html')

@login_required(login_url="/login/")
def index(request):
    """
    Luego de loguease se lleva a la vista principal la cual tiene
    distintas opciones dependiendo el rol que tenga 
    """
    data = request.user
    usuario = Usuario.objects.filter(email = data.email)
    es_usuario_nuevo = False
    print(data.username)
    if not usuario:
        es_usuario_nuevo = True
        nuevo_usuario = Usuario(
            nombre = data.first_name,
            apellido = data.last_name,
            email = data.email,
            nombre_usuario = data.username
        )
        nuevo_usuario.save()
        userSession = nuevo_usuario
    else:
        userSession = usuario[0]
    request.session['userSesion'] = "userSession"
    proyectos = getProyectsByUsuarioID(userSession.id)
    total_proyectos = Proyecto.objects.count()
    total_usuarios = Usuario.objects.count()
    context = {
        'segment': 'index',
        'userSession':userSession,
        'proyectos':proyectos,
        'total_proyectos':total_proyectos,
        'total_usuarios':total_usuarios
        }
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



def usuarios(request):
    """
    Se lista los usuarios actuales del sistema, este metodo se utiliza en el usuario admin
    """
    userSession = getUsuarioSesion(request.user.email)
    usuarios = Usuario.objects.all()
    rolUsuario = Rol.objects.get(id=userSession.df_rol.id)
    permisosProyecto = ['act_Usuario','dct_Usuario']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context = { 'usuarios':usuarios,
                'segment': 'usuarios',
                'userSession':userSession,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos}
    html_template = loader.get_template('home/usuarios.html')
    return HttpResponse(html_template.render(context, request))
@login_required(login_url="/login/")
def proyectos(request):
    """
    Se lista los proyectos actuales del sistema, este metodo se utiliza en el usuario admin
    """
    userSession = getUsuarioSesion(request.user.email)
    rolUsuario = Rol.objects.get(id=userSession.df_rol.id)
    proyectos = Proyecto.objects.all()
    permisosProyecto = ['crt_Proyecto','asg_Proyecto']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context = { 'userSession':userSession,
                'proyectos':proyectos,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos}
    html_template = loader.get_template('home/proyectos.html')
    return HttpResponse(html_template.render(context, request))

def GestionProyecto(request):
    usuarios = Usuario.objects.all()
    userSession = getUsuarioSesion(request.user.email)
    context = {'usuarios':usuarios,'segment': 'GestionProyecto','userSession':userSession}
    html_template = loader.get_template('home/GestionProyecto.html')
    return HttpResponse(html_template.render(context, request))

def GestionProyectoAgregar(request):
    print(request.POST['nombreProyecto'])
    variables = request.POST
    if request.method == 'POST':
        cliente = Cliente(
           nombre_cliente = variables['nombreCliente'] ,
           apellido_cliente =variables['apellidoCliente'] ,
           email_cliente = variables['emailCliente'],
           telefono_cliente = variables['telefonoCliente'],
           empresa_cliente = variables['empresaCliente']
        )
        cliente.save()
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        miembro.miembro_rol.add(getIdScrumRol())
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables['scrumMaster']))
        proyecto = Proyecto(
           nombre_proyecto = variables['nombreProyecto'],
           cliente_proyecto = cliente,
           fecha_ini_proyecto = variables['fechaInicio'],
           fecha_fin_proyecto = variables['fechaFin'],
           descripcion_proyecto = variables['descripcion'],
           sprint_dias = variables['sprintDias']
        )
        proyecto.save()
        proyecto.miembro_proyecto.add(miembro)
    return redirect('/')
@login_required(login_url="/login/")
def CrearProyecto(request):
    """
    Redirige a la vista de creacion de proyectos, consiste en un formulario
    """
    usuarios = Usuario.objects.all()
    userSession = getUsuarioSesion(request.user.email)
    rolUsuario = Rol.objects.get(id=userSession.df_rol.id)
    print(rolUsuario.permiso.all())
    context = { 'usuarios':usuarios,
                'segment': 'crearProyecto',
                'userSession':userSession,
                'rolUsuario':rolUsuario
                }
    html_template = loader.get_template('home/CrearProyecto.html')
    return HttpResponse(html_template.render(context, request))

def activarUsuario(request,id):
    """
    Cuando un usuario nuevo se loguea en el sistema queda en estado pendiente hasta que el admin le de acceso
    """
    usuario = Usuario.objects.get(id=id)
    usuario.activo = True
    usuario.save()
    return redirect('/')

def crearProyectoGuardar(request):
    """
    Metodo en el se crea el proyecto, realizando todos los inserts requeridos
    """
    print(request.POST['nombreProyecto'])
    variables = request.POST
    if request.method == 'POST':
        cliente = Cliente(
           nombre_cliente = variables['nombreCliente'] ,
           apellido_cliente =variables['apellidoCliente'] ,
           email_cliente = variables['emailCliente'],
           telefono_cliente = variables['telefonoCliente'],
           empresa_cliente = variables['empresaCliente']
        )
        cliente.save()
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        miembro.miembro_rol.add(getIdScrumRol())
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables['scrumMaster']))
        proyecto = Proyecto(
           nombre_proyecto = variables['nombreProyecto'],
           cliente_proyecto = cliente,
           fecha_ini_proyecto = variables['fechaInicio'],
           fecha_fin_proyecto = variables['fechaFin'],
           descripcion_proyecto = variables['descripcion'],
           sprint_dias = variables['sprintDias']
        )
        proyecto.save()
        proyecto.miembro_proyecto.add(miembro)
    return redirect('/')
@login_required(login_url="/login/")
def verProyecto(request,id):
    """
    Cuando un usuario ingresa a un proyecto en el cual fue asignado se visualizan 
    todos los datos de la misma 
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    permisosProyecto = ['dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'verProyecto',
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/vistaProyectos.html')
    return HttpResponse(html_template.render(context,request))
@login_required(login_url="/login/")
def rolesProyecto(request,id):
    """
    Se lista todos los roles especificos de cada proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    rolesProyecto = getRolByProyectId(id)
    permisos = Permiso.objects.all()
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(request.session['userSesion'])
    permisosProyecto = ['crt_rol','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'rolesProyecto',
                'permisos':permisos,
                'rolesProyecto':rolesProyecto,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/rolesProyecto.html')
    return HttpResponse(html_template.render(context,request))
@login_required(login_url="/login/")
def rolesProyectoCrear(request,id):
    """
    Se lista todos los roles especificos de cada proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    rolesProyecto = getRolByProyectId(id)
    permisos = Permiso.objects.all()
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(request.session['userSesion'])
    permisosProyecto = ['crt_rol','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'rolesProyecto',
                'permisos':permisos,
                'rolesProyecto':rolesProyecto,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos
                }
    html_template = loader.get_template('home/rolesProyectoCrear.html')
    return HttpResponse(html_template.render(context,request))

def rolesProyectoEditar(request,idProyecto,idRol):
    """
    Se lista todos los roles especificos de cada proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    permisos = Permiso.objects.all()
    proyecto = getProyectsByID(idProyecto,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    rolEditar = Rol.objects.get(id=idRol)

    for i in rolEditar.permiso.all():
       permisos = permisos.filter(~Q(id=i.id))
    print(request.session['userSesion'])
    permisosProyecto = ['crt_rol','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context= {  'userSession':userSession,
                'proyecto':proyecto,
                'segment': 'rolesProyecto',
                'permisos':permisos,
                'rolUsuario':rolUsuario,
                'validacionPermisos':validacionPermisos,
                'rolEditar':rolEditar
                }
    html_template = loader.get_template('home/rolesProyectoEditar.html')
    return HttpResponse(html_template.render(context,request))
    

def crearRolProyecto(request,id):
    """Se crea un nuevo rol con todos los permisos asociados"""
    variables = request.POST
    if request.method == 'POST':
        rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
        rol.save()
        for permiso in variables.getlist('permisos',False):
            print(permiso)
            rol.permiso.add(Permiso.objects.get(id=permiso))
        proyecto_rol = ProyectoRol(
            descripcion_proyecto_rol=''
        )
        proyecto_rol.save()
        proyecto_rol.rol.add(rol)
        proyecto_rol.proyecto.add(Proyecto.objects.get(id=id))
    return redirect(f'/proyecto/roles/{id}')


def editarRolProyecto(request,id):
    variables = request.POST
    if request.method == 'POST':
        idRol = variables.get('idRol',False)
        Rol.objects.filter(id=idRol).update(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )

    return redirect(f'/proyecto/roles/{id}')


def eliminarRolProyecto(request,id):
    """Se elimina el rol asociado al id"""
    variables = request.POST
    record = Rol.objects.filter(id = variables.get('idRol',False))
    record.delete()

    """validarEliminacion = getRolByID(id)
    print(validarEliminacion)
    if(validarEliminacion==None):
        print("no es")
    else:
        rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
        rol.delete()
    
    rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
    rol.delete()
    if request.method == 'POST':
        rol = Rol(
            descripcion_rol = variables.get('descripcion',False),
            nombre_rol = variables.get('nombre_rol',False),
        )
        rol.delete()
        for permiso in variables.getlist('permisos',False):
            print(permiso)
            rol.permiso.remove(Permiso.objects.get(id=permiso))
        proyecto_rol = ProyectoRol(
            descripcion_proyecto_rol=''
        )
        rol.objects.filter(id=id).delete()
        proyecto_rol.objects.filter(id=id).delete()
        #$proyecto_rol.delete()
        proyecto_rol.rol.remove(rol)
        proyecto_rol.proyecto.remove(Proyecto.objects.get(id=id))"""
    return redirect(f'/proyecto/roles/1')


def colaboradoresProyecto(request,id):
    """
    Se lista todos colaboradores del proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(rolUsuario.permiso.all())
    rolesProyecto = getRolByProyectId(id)
    colaboradores = getColaboratorsByProyect(id)
    usuarios = Usuario.objects.filter(~Q(id=userSession.id)).filter(~Q(df_rol=1))
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context={
        'colaboradores':colaboradores,
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'usuarios':usuarios,
        'validacionPermisos':validacionPermisos
        }
    html_template = loader.get_template('home/colaboradoresProyecto.html')
    return HttpResponse(html_template.render(context,request))
@login_required(login_url="/login/")

def colaboradoresProyectoCrear(request,id):
    """
    Se lista todos colaboradores del proyecto
    """
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    print(rolUsuario.permiso.all())
    rolesProyecto = getRolByProyectId(id)
    colaboradores = getColaboratorsByProyect(id)
    usuarios = Usuario.objects.filter(~Q(id=userSession.id)).filter(~Q(df_rol=1))
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context={
        'colaboradores':colaboradores,
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'usuarios':usuarios,
        'validacionPermisos':validacionPermisos
        }
    html_template = loader.get_template('home/colaboradoresProyectoCrear.html')
    return HttpResponse(html_template.render(context,request))

def colaboradoresProyectoEditar(request,idProyecto,idColaborador):
    print(f"ID PROYECTO = {idProyecto}")
    print(f"ID COLABORADOR = {idColaborador}")
    userSession = getUsuarioSesion(request.user.email)
    print(f"GET PROYECTS = {getProyectsByID(id,userSession.id)}")
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    rolesProyecto = getRolByProyectId(id)
    colaboradores = getColaboratorsByProyect(idProyecto)
    usuarios = Usuario.objects.filter(~Q(id=userSession.id)).filter(~Q(df_rol=1))
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context={
        'colaboradores':colaboradores,
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'usuarios':usuarios,
       'validacionPermisos':validacionPermisos
        }
    html_template = loader.get_template('home/colaboradoresProyectoEditar.html')
    return HttpResponse(html_template.render(context,request))


def asignarColaboradorProyecto(request,id):
    """Se almacena el nuevo rol con el colaborador al proyecto"""
    variables = request.POST
    if request.method == 'POST':
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        miembro.miembro_rol.add(Rol.objects.get(id=variables.get('rol',False)))
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables.get('usuario',False)))
        proyecto = Proyecto.objects.get(id=id)
        proyecto.miembro_proyecto.add(miembro)
    return redirect(f'/proyecto/colaboradores/{id}')

def eliminarColaboradorProyecto(request,id):


    variables = request.POST
    print(variables.get('idColaborador',False))
    record = MiembroEquipo.objects.filter(id = variables.get('idColaborador',False))
    record.delete()
    return redirect(f'/proyecto/1')

def editarColaboradorProyecto(request,idProyecto):
    """Se eliminan los colaboradores de un proyecto especifico"""
    print(f"ID PROYECTO 2= {idProyecto}")
    variables = request.POST
    if request.method == 'POST':
        miembro = MiembroEquipo(
           descripcion = ''
        )
        miembro.save()
        miembro.miembro_rol.add(Rol.objects.get(id=variables.get('rol',False)))
        miembro.miembro_usuario.add(Usuario.objects.get(id=variables.get('usuario',False)))
        proyecto = Proyecto.objects.get(id=idProyecto)
        proyecto.miembro_proyecto.add(miembro)
    return redirect(f'/proyecto/{idProyecto}')

def tipoUs(request,id):
    """Se listan todos los tipos de US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    tipoUs = getTipoUsbyProyectId(id)
    todostipoUs = getTipoUsbyNotProyectId(id)
    prioridad = PrioridadTUs.objects.all()
    rolesProyecto = getRolByProyectId(id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','imp_TipoUs','ctr_TipoUs']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'prueba':rolesProyecto,
        'tipoUs':tipoUs,
        'prioridades':prioridad,
        'todostipoUs':todostipoUs
        }
    html_template = loader.get_template('home/tipoUS.html')
    return HttpResponse(html_template.render(context,request))
def tipoUsCrear(request,id):
    """Se listan todos los tipos de US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    tipoUs = TipoUserStory.objects.filter(proyecto_tipo_us = id)
    prioridad = PrioridadTUs.objects.all()
    print(tipoUs)
    rolesProyecto = getRolByProyectId(id)
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','ctr_TipoUs']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'prueba':rolesProyecto,
        'tipoUs':tipoUs,
        'prioridades':prioridad
        }
    html_template = loader.get_template('home/tipoUSCrear.html')
    return HttpResponse(html_template.render(context,request))


def crearTUSProyecto(request,id):
    """Se almacena en base de datos el nuevo tipo de US"""
    variables = request.POST
    if request.method == 'POST':
        tipoUs = TipoUserStory(
            proyecto_tipo_us = Proyecto.objects.get(id=id),
            nombre_tipo_us = variables.get('nombre',False),
            descripcion_tipo_us= variables.get('descripcion',False),
            prioridad_tipo_us= PrioridadTUs.objects.get(id=variables.get('prioridad',False)),
        )
        tipoUs.save()
        fases = Fase.objects.all()
        for fase in fases:
            faseTus = FaseTUS(
                tipo_us_faseTUS=tipoUs,
                fase_faseTUS=fase
            )
            faseTus.save()
    return redirect(f'/proyecto/tipoUS/{id}')

def verProductBacklog(request,id):
    """Se visualiza todos los US"""
    userSession = getUsuarioSesion(request.user.email)
    proyecto = getProyectsByID(id,userSession.id)[0]
    rolUsuario = Rol.objects.get(id=proyecto.id_rol)
    rolesProyecto = getRolByProyectId(id)
    tipoUs = TipoUserStory.objects.filter(proyecto_tipo_us = id)
    print()
    permisosProyecto = ['agr_Colaborador','dsp_Colaborador','dsp_Roles','dsp_TipoUs','dsp_ProductBack','imp_TipoUs','ctr_TipoUs']
    validacionPermisos = validarPermisos(permisosProyecto,rolUsuario)
    userStorys = UserStory.objects.filter(proyecto_us = id)
    context={
        'rolesProyecto':rolesProyecto,
        'userSession':userSession,
        'proyecto':proyecto,
        'rolUsuario':rolUsuario,
        'validacionPermisos':validacionPermisos,
        'tipoUs':tipoUs,
        'prueba':rolesProyecto,
        'userStorys':userStorys
        }
    html_template = loader.get_template('home/productBacklog.html')
    return HttpResponse(html_template.render(context,request))

def crearUs(request,id):
    """Se agregan los nuevos Us"""
    variables = request.POST
    if request.method == 'POST':
        userStory = UserStory(
            proyecto_us = Proyecto.objects.get(id=id),
            nombre_us = variables.get('nombre',False),
            descripcion_us= variables.get('descripcion',False),
            tiempoEstimado_us = variables.get('tiempo',False),
            tipo_us= TipoUserStory.objects.get(id=variables.get('tipoUs',False))
        )
        userStory.save()
    return redirect(f'/proyecto/{id}')

def importarTusDeProyecto(request,id):
    """Se importan los tipos de US """
    variables = request.POST
    if request.method == 'POST':
        tipoUsSelect = TipoUserStory.objects.get(id=variables.get('idTipoUs',False))
        tipoUs = TipoUserStory(
            proyecto_tipo_us = Proyecto.objects.get(id=id),
            nombre_tipo_us = tipoUsSelect.nombre_tipo_us,
            descripcion_tipo_us= tipoUsSelect.descripcion_tipo_us,
            prioridad_tipo_us= tipoUsSelect.prioridad_tipo_us,
        )
        tipoUs.save()
        fases = Fase.objects.all()
        for fase in fases:
            faseTus = FaseTUS(
                tipo_us_faseTUS=tipoUs,
                fase_faseTUS=fase
            )
            faseTus.save()
    return redirect(f'/proyecto/{id}')