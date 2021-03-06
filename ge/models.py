# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models
from model_utils import Choices
from smart_selects.db_fields import ChainedForeignKey
from versatileimagefield.fields import VersatileImageField
from ajaximage.fields import AjaxImageField
from django.utils import timezone
from uuid import uuid4
import os
from  django.db import connection
#from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_long(value):
    if (value > -57 or value < -69):
        raise ValidationError(
            _(' Longitud incorrecta...'),
            params={'value': value},
        )


def validate_lat(value):
    if (value > -9 or value < -22):
        raise ValidationError(
            _('Latitud incorrecta...'),
            params={'value': value},
        )


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


class Continente (models.Model):
    nom_continente = models.CharField(max_length=100,
            verbose_name='Nombre del Continente')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_continente'

    def __unicode__(self):
        return self.nom_continente


class Pais(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nom_pais = models.CharField(max_length=100,
            help_text='Nombre del país',
            verbose_name='Nombre del país')
    nom_pais_inter = models.CharField(max_length=100,
            help_text='Nombre del país internacional')
    nom_pais_alias = models.CharField(max_length=100,
            help_text='Nombre corto del país')
    iso3166_2 = models.CharField(max_length=2,
            help_text='Código de 2 caracteres de acuerdo al ISO3166')
    iso3166_3 = models.CharField(max_length=3,
            help_text='Código de 3 caracteres de acuerdo al ISO3166')
    nacionalidad = models.CharField(max_length=50,
            help_text='Descripción genérica de la nacionalidad')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia del registro país')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia del registro país')
    actual = models.BooleanField(
            help_text='Especifica el estado activo o dado de baja lógica')
    descripcion = models.TextField(blank=True,
            help_text='Descripción del motivo de creación y/o actualización')
    estado =  models.BooleanField(
            help_text='True si el país participa en procesos electorales')
    continente = models.ForeignKey('Continente')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia del país (Capital)')
    geom = models.MultiPolygonField()
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia del país (Capital)')
    geohash_ref = models.CharField(max_length=8,
            help_text='Geohash del lugar de referencia del país (Capital)')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_pais'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_pais

    def nacionalidad_show(self):
        return self.nacionalidad


class Nivel_ut(models.Model):
    ut_descripcion = models.CharField(max_length=100,
            help_text='Descripción de la unidad territorial según país')
    pais = models.ForeignKey('Pais')
    jerarquia = models.PositiveSmallIntegerField(null=True,
            verbose_name = 'Jerarquía',
            help_text='Jerarquía de la Unidad Territorial de acuerdo al País')

    class Meta:
        db_table = 'g_nivel_ut'
        unique_together = ('id', 'jerarquia')

    def __unicode__(self):
        return self.ut_descripcion

class Ut_sup(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    nom_ut_sup = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. Superior')
    continente = models.ForeignKey(Continente)
    #pais = models.ForeignKey('Pais')
    pais = ChainedForeignKey(
        'Pais',
        chained_field="continente",
        chained_model_field="continente",
        show_all=False,
        auto_choose=True
    )
    cod_ine = models.CharField(max_length=2,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_ut_sup'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_ut_sup


class Ut_intermedia(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    nom_ut_intermedia = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. Intermedia')
    cod_ine = models.CharField(max_length=4,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')

    continente = models.ForeignKey(Continente)
    pais = ChainedForeignKey(
        'Pais',
        chained_field="continente",
        chained_model_field="continente",
        show_all=False,
        auto_choose=True
    )
    #ut_sup = models.ForeignKey('Ut_sup')
    ut_sup = ChainedForeignKey(
        'Ut_sup',
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True
    )
    ut_intermedia_id = models.IntegerField(
            help_text='Será utilizado para definir más niveles a futuro de ser necesario - recursivo')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_ut_intermedia'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_ut_intermedia

class Ut_basica(models.Model):
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    continente = models.ForeignKey(Continente)
    pais = ChainedForeignKey(
        'Pais',
        chained_field="continente",
        chained_model_field="continente",
        show_all=False,
        auto_choose=True
    )
    #ut_sup = models.ForeignKey('Ut_sup')
    ut_sup = ChainedForeignKey(
        'Ut_sup',
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True
    )
    ut_intermedia = ChainedForeignKey(
        'Ut_intermedia',
        chained_field="ut_sup",
        chained_model_field="ut_sup",
        show_all=False,
        auto_choose=True
    )
    nom_ut_basica = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. Básica')
    cod_ine = models.CharField(max_length=6,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    #ut_intermedia = models.ForeignKey('Ut_intermedia')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_ut_basica'
        unique_together = ('id_origen', 'version')

    def __unicode__(self):
        return self.nom_ut_basica


class Localidad(models.Model):
    continente = models.ForeignKey(Continente)
    pais = ChainedForeignKey(
        'Pais',
        chained_field="continente",
        chained_model_field="continente",
        show_all=False,
        auto_choose=True
    )
    ut_sup = ChainedForeignKey(
        'Ut_sup',
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True
    )
    ut_intermedia = ChainedForeignKey(
        'Ut_intermedia',
        chained_field="ut_sup",
        chained_model_field="ut_sup",
        show_all=False,
        auto_choose=True
    )
    ut_basica = ChainedForeignKey(
        'Ut_basica',
        chained_field="ut_intermedia",
        chained_model_field="ut_intermedia",
        show_all=False,
        auto_choose=True
    )
    nom_localidad = models.CharField(max_length=80,
            verbose_name = 'Nombre Ud.Terr. - equivalente a localidad en Bolivia')
    id_origen = models.IntegerField()
    version = models.PositiveSmallIntegerField()
    nivel_ut = models.ForeignKey('Nivel_ut')
    cod_ine = models.CharField(max_length=15,
            help_text='Código del INE si corresponde a Bolivia',
            verbose_name = 'Código INE')
    cod_ine_shp = models.CharField(max_length=15,
            help_text='Código del INE de fuente shapefile',
            verbose_name = 'Código INE - shapefile')
    periodo_ini = models.DateField(
            help_text='Periodo inicial de vigencia de la unidad territorial')
    periodo_fin = models.DateField(
            help_text='Periodo final de vigencia de la unidad territorial')
    actual = models.BooleanField(
            help_text='Indica si la unidad territorial esta vigente')
    censo = models.IntegerField(
            help_text='Año del Censo realizado por el INE')
    poblacion = models.IntegerField(
            help_text='Número de Población según el censo')
    viviendas = models.IntegerField(
            help_text='Número de viviendas según el censo')
    doc_legal = models.CharField(max_length=100,
            help_text='Indica si la unidad territorial esta vigente')
    #ut_basica = models.ForeignKey('Ut_basica')
    fecha_ingreso = models.DateField(
            help_text='Fecha de ingreso al sistema')
    latitud = models.FloatField(
            help_text='Latitud de la Localidad')
    longitud = models.FloatField(
            help_text='Longitud de la localidad')
    geohash = models.CharField(max_length=7,
            help_text='Geohash de la ubicación de la Localidad')
    geom = models.PointField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_localidad'
        unique_together = ('id_origen', 'version')
        verbose_name = '-Localidad-'
        verbose_name_plural = 'Localidades'

    def __unicode__(self):
        return self.nom_localidad


class Localidad_fuente(models.Model):
    localidad = models.ForeignKey('Localidad')
    nom_localidad = models.CharField(max_length=80)
    censo = models.IntegerField()
    poblacion = models.IntegerField()
    viviendas = models.IntegerField()
    geom = models.PointField(null=True)
    objects = models.GeoManager()

    class Meta:
        db_table = 'g_localidad_fuente'

    def __unicode__(self):
        return self.nom_localidad

## ge
class Asiento(models.Model):
    ESTADOS = Choices(
        (1, 'ACTIVO', ('ACTIVO')),
        (2, 'REHABILITADO', ('REHABILITADO')),
        (3, 'TRASLADADO', ('TRASLADADO')),
        (4, 'SUSPENDIDO', ('SUSPENDIDO')),
        (5, 'SUPRIMIDO', ('SUPRIMIDO')))
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    continente = models.ForeignKey(Continente)
    pais = ChainedForeignKey(
        'Pais',
        chained_field="continente",
        chained_model_field="continente",
        show_all=False,
        auto_choose=True
    )
    ut_sup = ChainedForeignKey(
        'Ut_sup',
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True
    )
    ut_intermedia = ChainedForeignKey(
        'Ut_intermedia',
        chained_field="ut_sup",
        chained_model_field="ut_sup",
        show_all=False,
        auto_choose=True
    )
    ut_basica = ChainedForeignKey(
        'Ut_basica',
        chained_field="ut_intermedia",
        chained_model_field="ut_intermedia",
        show_all=False,
        auto_choose=True
    )
    localidad = ChainedForeignKey(
        'Localidad',
        chained_field="ut_basica",
        chained_model_field="ut_basica",
        show_all=False,
        auto_choose=True
    )
    nom_asiento = models.CharField(max_length=100,
                                  verbose_name='Nombre Asiento Electoral',
                                  help_text='Ingrese nombre del Asiento Electoral'
                                  )
    #ut_basica = models.ForeignKey('Ut_basica')
    #localidad = models.ForeignKey('Localidad')
    doc_actualizacion = models.CharField(max_length=50,
                                     verbose_name='Doc. de Actualización RSP',
                                     help_text='Resolución de sala plena, (creacion/suspensión/supresión/..etc), Inf. u otro'
                                     )
    fecha_doc_actualizacion = models.DateField(
                                     verbose_name='Fecha resolución',
                                     help_text='Fecha resolución de sala plena'
                                     )
    descripcion_ubicacion = models.TextField(blank=True,
                                    verbose_name='Descripción ubicación',
                                    help_text='Descripción de la ubicación del asiento electoral'
                                            )
    estado = models.PositiveSmallIntegerField(choices=ESTADOS, default=ESTADOS.ACTIVO,
                                    verbose_name='Estado',
                                    help_text='Estado del asiento electoral'
                                             )
    proceso_activo = models.BooleanField(
                                    verbose_name='Activo en Proceso Electoral',
                                    help_text='Marcar si se encuentra activo en Proceso Electoral'
                                        )
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA,
                                    verbose_name='Etapa',
                                    help_text='Describe la etapa en la que se encuentra la solicitud'
                                            )
    #fecha_ingreso = models.DateTimeField(auto_now=True)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    obs = models.CharField(max_length=100)
    #fecha_act = models.DateTimeField(auto_now_add=True)
    #fecha_act = models.AutoDateTimeField(default=timezone.now)
    fecha_act = models.DateTimeField(auto_now=True)
    existe_orc = models.NullBooleanField(blank=True,
                                    verbose_name='Existe O.R.C.',
                                    help_text='Marque si en la localidad existe Oficialía de Registro Civil'
                                    )
    numero_orc = models.BigIntegerField(blank=True, null=True,
                                       verbose_name = 'Número de O.R.C.',
                                       help_text = 'Número de O.R.C.'
                                       )
    latitud = models.FloatField(validators=[validate_lat],
                                    help_text='Latitud/Longitud de la ubicación de la plaza principal u otra ubicación de interés en caso de que no cuente con plaza '
                                )
    longitud = models.FloatField(validators=[validate_long])
    geohash = models.CharField(max_length=8)
    geom = models.PointField(null=True, blank=True)
    objects = models.GeoManager()
    # GeoDjango-specific: a geometry field (MultiMultiPolygonField), and
    # overriding the default manager with a GeoManager instance.

    # Returns the string representation of the model.


    def __unicode__(self):              # __unicode__ on Python 2
        return self.nom_asiento

    def ubicacion(self):
        return '%s - %s - %s - %s' % (self.ut_basica, self.ut_basica.ut_intermedia.nom_ut_intermedia, self.ut_basica.ut_intermedia.ut_sup.nom_ut_sup, self.ut_basica.ut_intermedia.ut_sup.pais.nom_pais_alias)

'''
    def save(self, *args, **kwargs):
        self.fecha_act = datetime.now() #.replace(tzinfo=get_current_timezone())
        super(Asiento, self).save(*args, **kwargs)
'''

class Ruta(models.Model):
    asiento = models.ForeignKey('Asiento')
    nro_ruta = models.IntegerField()
    nro_tramo = models.IntegerField()
    inicio = models.CharField(max_length=80)
    fin = models.CharField(max_length=80)
    tipo = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=100)
    distancia_km = models.FloatField()
    tiempo_hrs = models.IntegerField()
    tiempo_min = models.IntegerField()
    costo = models.FloatField()
    obs = models.CharField(max_length=100)
    fecha_act = models.DateTimeField(auto_now_add=True)
    geom = models.LineStringField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return str(self.nro_ruta)

class Asiento_jurisdiccion(models.Model):
    asiento = models.ForeignKey('Asiento')
    localidad = models.ForeignKey('Localidad')
    accesibilidad = models.CharField(max_length=100)
    distancia_km = models.FloatField()
    geohash = models.CharField(max_length=8)
    latitud = models.FloatField()
    longitud = models.FloatField()
    obs = models.CharField(max_length=200)
    fecha_act = models.DateTimeField()
    geom = models.PointField(null=True)
    objects = models.GeoManager()


def path_and_rename(instance, filename):
    upload_to = 'img'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

'''
class path_and_renamec(instance):
    def __call__(self):
        upload_to = 'img'
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)
'''

# https://djangosnippets.org/snippets/2731/
def prefetch_id(instance):
    """ Fetch the next value in a django id autofield postgresql sequence """
    cursor = connection.cursor()
    cursor.execute(
        "SELECT nextval('{0}_{1}_id_seq'::regclass)".format(
            instance._meta.app_label.lower(),
            instance._meta.object_name.lower(),
        )
    )
    row = cursor.fetchone()
    cursor.close()
    return int(row[0])

# https://stackoverflow.com/questions/5135556/dynamic-file-path-in-django
def get_asiento_img_path(instance, filename):
    id = instance.id
    if id == None:
        id = max(map(lambda a:a.id, Asiento_img.objects.all())) + 1
    return os.path.join('img', str(id), filename)

def get_asiento_img_path2(instance, filename):
    id = instance.id
    if id == None:
        #id = max(map(lambda a:a.id, Asiento_img.objects.all())) + 1
        id = prefetch_id(instance) + 1
    return os.path.join('img', str(id), filename)


def get_asiento_img_path3(instance, filename):
    upload_to = 'img'
    ext = filename.split('.')[-1]
    id = instance.id
    if id == None:
        id = prefetch_id(instance) + 1
        filename = '{}_{}.{}'.format(id, instance.vista, ext)
    else:
        #filename = '{}.{}'.format(instance.pk, ext)
        filename = '{}_{}.{}'.format(instance.pk, instance.vista, ext)
    #return os.path.join('img', str(id), filename)
    return os.path.join(upload_to, filename)


class Asiento_img(models.Model):
    VISTAS = Choices(
        (1, 'PANORAMICA', ('PANORAMICA')),
        (2, 'VISTA1', ('VISTA1')),
        (3, 'VISTA2', ('VISTA2')),
        (4, 'VISTA3', ('VISTA3')))
    asiento = models.ForeignKey('Asiento')
    vista = models.PositiveSmallIntegerField(choices=VISTAS)
    #img = models.ImageField(upload_to="img", null=True, blank=True)
    #ok img = VersatileImageField('Image', upload_to="img", null=True, blank=True)
    #ok img = VersatileImageField('Image', upload_to=path_and_rename, null=True, blank=True)
    #ok img = AjaxImageField(upload_to='img', max_height=768, max_width=1024, crop=True)
    img = VersatileImageField(upload_to=get_asiento_img_path3)

    #def image_tag(self):
     #   return mark_safe('<img src="/img/%s" width="150" height="150" />' % (self.image))

    '''
    def save(self, *args, **kwargs):
        if not self.id: #and img:
            #self.id = prefetch_id(instance)
            self.id = prefetch_id

        super(Asiento_img, self).save(*args, **kwargs)
    '''

    class Meta:
        unique_together = ('asiento', 'vista')


class Tipo_circun(models.Model):
    tipo_circun = models.CharField(max_length=40)

    def __unicode__(self):
        return self.tipo_circun

class Circun(models.Model):
    circun = models.PositiveSmallIntegerField()
    nom_circunscripcion = models.CharField(max_length=100)
    tipo_circun = models.ForeignKey('Tipo_circun')
    asientos = models.ManyToManyField('Asiento', through='asiento_circun')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.nom_circunscripcion
    #class Admin:
    #    pass


class Asiento_circun(models.Model):
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    circun = models.ForeignKey(Circun, on_delete=models.CASCADE)


class Distrito(models.Model):
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    asientos = models.ManyToManyField('Asiento', through='asiento_distrito')
    distrito = models.CharField(max_length=100)
    nro_distrito = models.CharField(max_length=10)
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField()
    obs = models.CharField(max_length=150)
    fecha_act = models.DateTimeField()
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.distrito


class Asiento_distrito(models.Model):
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE)


class Zona(models.Model):
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    zona = models.CharField(max_length=100)
    distrito = models.ForeignKey('Distrito')
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField()
    obs = models.CharField(max_length=120)
    fecha_act = models.DateTimeField()
    lat_ref = models.FloatField(
            help_text='Latitud del lugar de referencia')
    long_ref = models.FloatField(
            help_text='Longitud del lugar de referencia')
    geohash_ref = models.CharField(max_length=7,
            help_text='Geohash del lugar de referencia')
    geom = models.MultiPolygonField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.zona


class Recinto(models.Model):
    ESTADOS = Choices(
        (1, 'ACTIVO', ('ACTIVO')),
        (2, 'REHABILITADO', ('REHABILITADO')),
        (3, 'TRASLADADO', ('TRASLADADO')),
        (4, 'SUSPENDIDO', ('SUSPENDIDO')),
        (5, 'SUPRIMIDO', ('SUPRIMIDO')))
    ETAPAS = Choices(
        (1, 'PROPUESTA', ('PROPUESTA')),
        (2, 'REVISION', ('REVISION')),
        (3, 'APROBADO', ('APROBADO')))
    TIPOS = Choices(
        (1, 'UNIDAD_EDUCATIVA', ('Unidad Educativa')),
        (2, 'SEDE', ('Sede/Casa comunal/Casa de gobierno/Salón de comunidad')),
        (3, 'IGLESIA', ('Iglesia/Seminario')),
        (4, 'CÁRCEL', ('Cárcel')),
        (5, 'UNIVERSIDAD', ('Universidad/Normal')),
        (6, 'PLAZA', ('Plaza')),
        (7, 'CENTRO_SALUD', ('Centro de Salud')),
        (8, 'COMPLEJO', ('Complejo/Campo deportivo')),
        (100, 'OTROS', ('Otros')),

    )
    continente = models.ForeignKey(Continente)
    pais = ChainedForeignKey(
        'Pais',
        chained_field="continente",
        chained_model_field="continente",
        show_all=False,
        auto_choose=True
    )
    ut_sup = ChainedForeignKey(
        'Ut_sup',
        chained_field="pais",
        chained_model_field="pais",
        show_all=False,
        auto_choose=True
    )
    ut_intermedia = ChainedForeignKey(
        'Ut_intermedia',
        chained_field="ut_sup",
        chained_model_field="ut_sup",
        show_all=False,
        auto_choose=True
    )
    ut_basica = ChainedForeignKey(
        'Ut_basica',
        chained_field="ut_intermedia",
        chained_model_field="ut_intermedia",
        show_all=False,
        auto_choose=True
    )
    asiento = ChainedForeignKey(
        'Asiento',
        chained_field="ut_basica",
        chained_model_field="ut_basica",
        show_all=False,
        auto_choose=True
    )
    tipo = models.PositiveSmallIntegerField(
        choices=TIPOS, default=TIPOS.UNIDAD_EDUCATIVA)
    zona = models.ForeignKey('Zona')
    nom_recinto = models.CharField(max_length=100,
                                  verbose_name= 'Nombre de Recinto',
                                  help_text= 'Nombre del Recinto Electoral'
                                  )
    doc_actualizacion = models.CharField(max_length=50,
                                        verbose_name='Doc. de Actualización',
                                        help_text='Resolución de sala plena, (creación/suspensión/supresión/...etc)')
    fecha_doc_actualizacion = models.DateField(
                                        verbose_name='Fecha Doc. de Actualización',
                                        help_text='Fecha Doc. de Actualización (RSP, Inf, etc.)'
    )
    max_mesas = models.PositiveSmallIntegerField()
    nro_pisos = models.PositiveIntegerField()
    nro_aulas = models.PositiveSmallIntegerField()
    direccion = models.CharField(max_length=150)
    estado = models.PositiveSmallIntegerField(
        choices=ESTADOS, default=ESTADOS.ACTIVO)
    tipo_circun = models.ForeignKey('Tipo_circun')
    rue = models.PositiveIntegerField()
    etapa = models.PositiveSmallIntegerField(choices=ETAPAS, default=ETAPAS.PROPUESTA)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_act = models.DateTimeField(auto_now_add=True)
    obs = models.CharField(max_length=120)
    latitud = models.FloatField()
    longitud = models.FloatField()
    geohash = models.CharField(max_length=9)
    geom = models.PointField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.nom_recinto

    def ubicacion(self):
        return '%s - %s - %s - %s - %s' % (self.direccion, self.ut_basica, self.ut_basica.ut_intermedia.nom_ut_intermedia, self.ut_basica.ut_intermedia.ut_sup.nom_ut_sup, self.ut_basica.ut_intermedia.ut_sup.pais.nom_pais_alias)


class Recinto_img(models.Model):
    VISTAS = Choices(
        (1, 'FRONTAL', ('FRONTAL')),
        (2, 'INTERIOR', ('INTERIOR')),
        (3, 'LATERAL_IZQ', ('LATERAL_IZQ')),
        (4, 'LATERAL_DER', ('LATERAL_DER')))
    recinto = models.ForeignKey('Recinto')
    vista = models.PositiveSmallIntegerField(choices=VISTAS)
    img = models.ImageField(upload_to="img", null=True, blank=True)

    class Meta:
        unique_together = ('recinto', 'vista')


class Categoria(models.Model):
    nom_categoria = models.CharField(max_length=100)

    def __unicode__(self):
        return self.nom_categoria

class Subcategoria(models.Model):
    categoria = models.ForeignKey(Categoria)
    nom_subcategoria = models.CharField(max_length=100)
    obs = models.CharField(max_length=220)

    def __unicode__(self):
        return self.nom_subcategoria


class Recinto_detalle(models.Model):
    recinto = models.ForeignKey('Recinto')
    subcategoria = models.ForeignKey('Subcategoria')
    descripcion = models.CharField(max_length=100)


class Asiento_detalle(models.Model):
    asiento = models.ForeignKey('Asiento')
    categoria = models.ForeignKey(Categoria)
    subcategoria = ChainedForeignKey(
        'Subcategoria',
        chained_field="categoria",
        chained_model_field="categoria",
        show_all=False,
        auto_choose=True
    )
    descripcion = models.CharField(max_length=100)
    def __unicode__(self):
        return self.descripcion
