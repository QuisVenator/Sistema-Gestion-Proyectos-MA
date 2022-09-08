# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from . import views

app_name = "webApp"
urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/activar/<int:id>', views.activarUsuario, name='usuarios'),
    path('proyecto/',views.proyectos, name='proyectos'),
    path('CrearProyecto/',views.CrearProyecto, name='CrearProyecto'),
    path('CrearProyecto/guardar',views.crearProyectoGuardar, name='crearProyectoGuardar'),
    path('proyecto/roles',views.rolesProyecto, name='rolesProyecto'),
    path('proyecto/<int:id>',views.verProyecto, name='verProyecto'),
    path('test/',views.request_page , name='test'),
]
