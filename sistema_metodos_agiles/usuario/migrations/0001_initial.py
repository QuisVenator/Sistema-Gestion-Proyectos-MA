# Generated by Django 4.1 on 2022-09-07 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('apellido_cliente', models.CharField(max_length=100)),
                ('email_cliente', models.CharField(max_length=100)),
                ('telefono_cliente', models.CharField(max_length=100)),
                ('empresa_cliente', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nombre_cliente'],
            },
        ),
        migrations.CreateModel(
            name='MiembroEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Miembro',
                'verbose_name_plural': 'Miembros',
            },
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Permiso',
                'verbose_name_plural': 'Permisos',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100)),
                ('permiso', models.ManyToManyField(to='usuario.permiso')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('nombre_usuario', models.CharField(max_length=100)),
                ('activo', models.BooleanField(default=False)),
                ('df_rol', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='usuario.rol')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'ordering': ['nombre_usuario'],
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_proyecto', models.CharField(max_length=100)),
                ('fecha_ini_proyecto', models.DateField(null=True)),
                ('fecha_fin_proyecto', models.DateField(null=True)),
                ('descripcion_proyecto', models.CharField(default='', max_length=100)),
                ('estado_proyecto', models.CharField(default='1', max_length=1)),
                ('sprint_dias', models.IntegerField(default=0)),
                ('cliente_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.cliente')),
                ('miembro_proyecto', models.ManyToManyField(to='usuario.miembroequipo')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
                'ordering': ['nombre_proyecto'],
            },
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='miembro_rol',
            field=models.ManyToManyField(to='usuario.rol'),
        ),
        migrations.AddField(
            model_name='miembroequipo',
            name='miembro_usuario',
            field=models.ManyToManyField(to='usuario.usuario'),
        ),
    ]
