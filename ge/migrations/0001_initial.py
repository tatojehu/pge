# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 19:09
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_asiento', models.CharField(max_length=100)),
                ('resol_creacion', models.CharField(max_length=50)),
                ('fecha_creacion', models.DateTimeField()),
                ('descripcion_ubicacion', models.CharField(max_length=254)),
                ('estado', models.PositiveSmallIntegerField(choices=[(1, 'ACTIVO'), (2, 'REHABILITADO'), (3, 'TRASLADADO'), (4, 'SUSPENDIDO'), (5, 'SUPRIMIDO')], default=1)),
                ('proceso_activo', models.BooleanField()),
                ('etapa', models.PositiveSmallIntegerField(choices=[(1, 'PROPUESTA'), (2, 'REVISION'), (3, 'APROBADO')], default=1)),
                ('fecha_ingreso', models.DateTimeField()),
                ('obs', models.CharField(max_length=100)),
                ('fecha_act', models.DateTimeField()),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('geohash', models.CharField(max_length=8)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Asiento_circun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Asiento_distrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Asiento_img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vista', models.PositiveSmallIntegerField(choices=[(1, 'PANORAMICA'), (2, 'VISTA1'), (3, 'VISTA2'), (4, 'VISTA3')])),
                ('img', models.ImageField(blank=True, null=True, upload_to='img')),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Asiento_jurisdiccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accesibilidad', models.CharField(max_length=100)),
                ('distancia_km', models.FloatField()),
                ('geohash', models.CharField(max_length=8)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('obs', models.CharField(max_length=100)),
                ('fecha_act', models.DateTimeField()),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_categoria', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Circun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('circun', models.PositiveSmallIntegerField()),
                ('nom_circunscripcion', models.CharField(max_length=100)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('asientos', models.ManyToManyField(through='ge.Asiento_circun', to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Continente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_continente', models.CharField(max_length=100, verbose_name='Nombre del Continente')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'db_table': 'g_continente',
            },
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distrito', models.CharField(max_length=100)),
                ('etapa', models.PositiveSmallIntegerField(choices=[(1, 'PROPUESTA'), (2, 'REVISION'), (3, 'APROBADO')], default=1)),
                ('fecha_ingreso', models.DateTimeField()),
                ('obs', models.CharField(max_length=150)),
                ('fecha_act', models.DateTimeField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('asientos', models.ManyToManyField(through='ge.Asiento_distrito', to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_origen', models.IntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('nom_localidad', models.CharField(max_length=80, verbose_name='Nombre Ud.Terr. - equivalente a localidad en Bolivia')),
                ('cod_ine', models.CharField(help_text='C\xf3digo del INE si corresponde a Bolivia', max_length=6, verbose_name='C\xf3digo INE')),
                ('cod_ine_shp', models.CharField(help_text='C\xf3digo del INE de fuente shapefile', max_length=15, verbose_name='C\xf3digo INE - shapefile')),
                ('periodo_ini', models.DateField(help_text='Periodo inicial de vigencia de la unidad territorial')),
                ('periodo_fin', models.DateField(help_text='Periodo final de vigencia de la unidad territorial')),
                ('actual', models.BooleanField(help_text='Indica si la unidad territorial esta vigente')),
                ('censo', models.IntegerField(help_text='A\xf1o del Censo realizado por el INE')),
                ('poblacion', models.IntegerField(help_text='N\xfamero de Poblaci\xf3n seg\xfan el censo')),
                ('viviendas', models.IntegerField(help_text='N\xfamero de viviendas seg\xfan el censo')),
                ('doc_legal', models.CharField(help_text='Indica si la unidad territorial esta vigente', max_length=100)),
                ('fecha_ingreso', models.DateField(help_text='Fecha de ingreso al sistema')),
                ('latitud', models.FloatField(help_text='Latitud de la Localidad')),
                ('longitud', models.FloatField(help_text='Longitud de la localidad')),
                ('geohash', models.CharField(help_text='Geohash de la ubicaci\xf3n de la Localidad', max_length=7)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'db_table': 'g_localidad',
            },
        ),
        migrations.CreateModel(
            name='Nivel_ut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ut_descripcion', models.CharField(help_text='Descripci\xf3n de la unidad territorial seg\xfan pa\xeds', max_length=100)),
            ],
            options={
                'db_table': 'g_nivel_ut',
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_origen', models.IntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('nom_pais', models.CharField(help_text='Nombre del pa\xeds', max_length=100, verbose_name='Nombre del pa\xeds')),
                ('nom_pais_inter', models.CharField(help_text='Nombre del pa\xeds internacional', max_length=100)),
                ('nom_pais_alias', models.CharField(help_text='Nombre corto del pa\xeds', max_length=100)),
                ('iso3166_2', models.CharField(help_text='C\xf3digo de 2 caracteres de acuerdo al ISO3166', max_length=2)),
                ('iso3166_3', models.CharField(help_text='C\xf3digo de 3 caracteres de acuerdo al ISO3166', max_length=3)),
                ('nacionalidad', models.CharField(help_text='Descripci\xf3n gen\xe9rica de la nacionalidad', max_length=50)),
                ('periodo_ini', models.DateField(help_text='Periodo inicial de vigencia del registro pa\xeds')),
                ('periodo_fin', models.DateField(help_text='Periodo final de vigencia del registro pa\xeds')),
                ('actual', models.BooleanField(help_text='Especifica el estado activo o dado de baja l\xf3gica')),
                ('descripcion', models.TextField(blank=True, help_text='Descripci\xf3n del motivo de creaci\xf3n y/o actualizaci\xf3n')),
                ('estado', models.BooleanField(help_text='True si el pa\xeds participa en procesos electorales')),
                ('fecha_ingreso', models.DateField(help_text='Fecha de ingreso al sistema')),
                ('lat_ref', models.FloatField(help_text='Latitud del lugar de referencia del pa\xeds (Capital)')),
                ('long_ref', models.FloatField(help_text='Longitud del lugar de referencia del pa\xeds (Capital)')),
                ('geohash_ref', models.CharField(help_text='Geohash del lugar de referencia del pa\xeds (Capital)', max_length=8)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('continente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Continente')),
            ],
            options={
                'db_table': 'g_pais',
            },
        ),
        migrations.CreateModel(
            name='Recinto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveSmallIntegerField()),
                ('nom_recinto', models.CharField(max_length=100)),
                ('max_mesas', models.PositiveSmallIntegerField()),
                ('cantidad_pisos', models.PositiveIntegerField()),
                ('direccion', models.CharField(max_length=150)),
                ('estado', models.PositiveSmallIntegerField(choices=[(1, 'ACTIVO'), (2, 'REHABILITADO'), (3, 'TRASLADADO'), (4, 'SUSPENDIDO'), (5, 'SUPRIMIDO')], default=1)),
                ('rue', models.PositiveIntegerField()),
                ('etapa', models.PositiveSmallIntegerField(choices=[(1, 'PROPUESTA'), (2, 'REVISION'), (3, 'APROBADO')], default=1)),
                ('fecha_ingreso', models.DateTimeField()),
                ('fecha_act', models.DateTimeField()),
                ('obs', models.CharField(max_length=120)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('geohash', models.CharField(max_length=9)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Recinto_img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vista', models.PositiveSmallIntegerField(choices=[(1, 'FRONTAL'), (2, 'INTERIOR'), (3, 'LATERAL_IZQ'), (4, 'LATERAL_DER')])),
                ('img', models.ImageField(blank=True, null=True, upload_to='img')),
                ('recinto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Recinto')),
            ],
        ),
        migrations.CreateModel(
            name='Ruta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nro_ruta', models.IntegerField()),
                ('nro_tramo', models.IntegerField()),
                ('inicio', models.CharField(max_length=80)),
                ('fin', models.CharField(max_length=80)),
                ('tipo', models.CharField(max_length=80)),
                ('descripcion', models.CharField(max_length=100)),
                ('distancia_km', models.FloatField()),
                ('tiempo_hrs', models.IntegerField()),
                ('tiempo_min', models.IntegerField()),
                ('costo', models.FloatField()),
                ('obs', models.CharField(max_length=100)),
                ('fecha_act', models.DateTimeField()),
                ('geom', django.contrib.gis.db.models.fields.LineStringField(srid=4326)),
                ('asiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Asiento')),
            ],
        ),
        migrations.CreateModel(
            name='Subcategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_subcategoria', models.CharField(max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo_circun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_circun', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Ut_basica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_origen', models.IntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('nom_ut_basica', models.CharField(max_length=80, verbose_name='Nombre Ud.Terr. B\xe1sica')),
                ('cod_ine', models.CharField(help_text='C\xf3digo del INE si corresponde a Bolivia', max_length=6, verbose_name='C\xf3digo INE')),
                ('periodo_ini', models.DateField(help_text='Periodo inicial de vigencia de la unidad territorial')),
                ('periodo_fin', models.DateField(help_text='Periodo final de vigencia de la unidad territorial')),
                ('actual', models.BooleanField(help_text='Indica si la unidad territorial esta vigente')),
                ('doc_legal', models.CharField(help_text='Indica si la unidad territorial esta vigente', max_length=100)),
                ('fecha_ingreso', models.DateField(help_text='Fecha de ingreso al sistema')),
                ('lat_ref', models.FloatField(help_text='Latitud del lugar de referencia')),
                ('long_ref', models.FloatField(help_text='Longitud del lugar de referencia')),
                ('geohash_ref', models.CharField(help_text='Geohash del lugar de referencia', max_length=7)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('nivel_ut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Nivel_ut')),
            ],
            options={
                'db_table': 'g_ut_basica',
            },
        ),
        migrations.CreateModel(
            name='Ut_intermedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_origen', models.IntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('nom_ut_intermedia', models.CharField(max_length=80, verbose_name='Nombre Ud.Terr. Intermedia')),
                ('cod_ine', models.CharField(help_text='C\xf3digo del INE si corresponde a Bolivia', max_length=4, verbose_name='C\xf3digo INE')),
                ('periodo_ini', models.DateField(help_text='Periodo inicial de vigencia de la unidad territorial')),
                ('periodo_fin', models.DateField(help_text='Periodo final de vigencia de la unidad territorial')),
                ('actual', models.BooleanField(help_text='Indica si la unidad territorial esta vigente')),
                ('doc_legal', models.CharField(help_text='Indica si la unidad territorial esta vigente', max_length=100)),
                ('ut_intermedia_id', models.IntegerField(help_text='Ser\xe1 utilizado para definir m\xe1s niveles a futuro de ser necesario - recursivo')),
                ('fecha_ingreso', models.DateField(help_text='Fecha de ingreso al sistema')),
                ('lat_ref', models.FloatField(help_text='Latitud del lugar de referencia')),
                ('long_ref', models.FloatField(help_text='Longitud del lugar de referencia')),
                ('geohash_ref', models.CharField(help_text='Geohash del lugar de referencia', max_length=7)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('nivel_ut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Nivel_ut')),
            ],
            options={
                'db_table': 'g_ut_intermedia',
            },
        ),
        migrations.CreateModel(
            name='Ut_sup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_origen', models.IntegerField()),
                ('version', models.PositiveSmallIntegerField()),
                ('nom_ut_sup', models.CharField(max_length=80, verbose_name='Nombre Ud.Terr. Superior')),
                ('cod_ine', models.CharField(help_text='C\xf3digo del INE si corresponde a Bolivia', max_length=2, verbose_name='C\xf3digo INE')),
                ('periodo_ini', models.DateField(help_text='Periodo inicial de vigencia de la unidad territorial')),
                ('periodo_fin', models.DateField(help_text='Periodo final de vigencia de la unidad territorial')),
                ('actual', models.BooleanField(help_text='Indica si la unidad territorial esta vigente')),
                ('doc_legal', models.CharField(help_text='Indica si la unidad territorial esta vigente', max_length=100)),
                ('fecha_ingreso', models.DateField(help_text='Fecha de ingreso al sistema')),
                ('lat_ref', models.FloatField(help_text='Latitud del lugar de referencia')),
                ('long_ref', models.FloatField(help_text='Longitud del lugar de referencia')),
                ('geohash_ref', models.CharField(help_text='Geohash del lugar de referencia', max_length=7)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('nivel_ut', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Nivel_ut')),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Pais')),
            ],
            options={
                'db_table': 'g_ut_sup',
            },
        ),
        migrations.CreateModel(
            name='Zona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zona', models.CharField(max_length=100)),
                ('etapa', models.PositiveSmallIntegerField(choices=[(1, 'PROPUESTA'), (2, 'REVISION'), (3, 'APROBADO')], default=1)),
                ('fecha_ingreso', models.DateTimeField()),
                ('obs', models.CharField(max_length=120)),
                ('fecha_act', models.DateTimeField()),
                ('lat_ref', models.FloatField(help_text='Latitud del lugar de referencia')),
                ('long_ref', models.FloatField(help_text='Longitud del lugar de referencia')),
                ('geohash_ref', models.CharField(help_text='Geohash del lugar de referencia', max_length=7)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('distrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Distrito')),
            ],
        ),
        migrations.AddField(
            model_name='ut_intermedia',
            name='ut_sup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Ut_sup'),
        ),
        migrations.AddField(
            model_name='ut_basica',
            name='ut_intermedia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Ut_intermedia'),
        ),
        migrations.AddField(
            model_name='recinto',
            name='tipo_circun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Tipo_circun'),
        ),
        migrations.AddField(
            model_name='recinto',
            name='zona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Zona'),
        ),
        migrations.AddField(
            model_name='nivel_ut',
            name='pais',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Pais'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='nivel_ut',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Nivel_ut'),
        ),
        migrations.AddField(
            model_name='localidad',
            name='ut_basica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Ut_basica'),
        ),
        migrations.AddField(
            model_name='circun',
            name='tipo_circun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Tipo_circun'),
        ),
        migrations.AddField(
            model_name='asiento_jurisdiccion',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Localidad'),
        ),
        migrations.AddField(
            model_name='asiento_distrito',
            name='distrito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Distrito'),
        ),
        migrations.AddField(
            model_name='asiento_circun',
            name='circun',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Circun'),
        ),
        migrations.AddField(
            model_name='asiento',
            name='localidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Localidad'),
        ),
        migrations.AddField(
            model_name='asiento',
            name='ut_basica',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ge.Ut_basica'),
        ),
        migrations.AlterUniqueTogether(
            name='ut_sup',
            unique_together=set([('id_origen', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='ut_intermedia',
            unique_together=set([('id_origen', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='ut_basica',
            unique_together=set([('id_origen', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='recinto_img',
            unique_together=set([('recinto', 'vista')]),
        ),
        migrations.AlterUniqueTogether(
            name='pais',
            unique_together=set([('id_origen', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='localidad',
            unique_together=set([('id_origen', 'version')]),
        ),
        migrations.AlterUniqueTogether(
            name='asiento_img',
            unique_together=set([('asiento', 'vista')]),
        ),
    ]
