# Generated by Django 4.1 on 2022-09-24 23:03

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prioridad_tipo_us', models.IntegerField(blank=True, null=True)),
                ('nombre_tipo_us', models.CharField(max_length=50)),
                ('descripcion_tipo_us', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Tipo User Story',
                'verbose_name_plural': 'Tipos de User Story',
                'ordering': ['nombre_tipo_us'],
            },
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_us', models.CharField(max_length=50)),
                ('descripcion_us', models.CharField(max_length=50)),
                ('duracion_us', models.IntegerField(blank=True, null=True)),
                ('fechaIni_us', models.DateField(default=datetime.date.today)),
                ('tipo_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.tipouserstory')),
            ],
            options={
                'verbose_name': 'User Story',
                'verbose_name_plural': 'User Stories',
                'ordering': ['nombre_us'],
            },
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sp', models.CharField(max_length=50)),
                ('fechaIni_sp', models.DateField(default=datetime.date.today)),
                ('fechaFIn_sp', models.DateField()),
                ('duracion_sp', models.IntegerField()),
                ('userStory_sp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuario.userstory')),
            ],
            options={
                'verbose_name': 'Sprint',
                'verbose_name_plural': 'Sprints',
                'ordering': ['nombre_sp'],
            },
        ),
    ]