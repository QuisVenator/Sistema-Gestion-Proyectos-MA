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
    path('proyecto/roles/<int:id>',views.rolesProyecto, name='rolesProyecto'),
    path('proyecto/roles/guardar/<int:id>',views.crearRolProyecto, name='crearRolProyecto'),
    path('proyecto/<int:id>',views.verProyecto, name='verProyecto'),
    path('proyecto/colaboradores/<int:id>',views.colaboradoresProyecto, name='colaboradoresProyecto'),
    path('proyecto/colaboradores/guardar/<int:id>',views.asignarColaboradorProyecto, name='asignarColaboradorProyecto')
]