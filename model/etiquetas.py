# Etiquetas

from google.appengine.ext import ndb
from model.squabs import Squab


class Etiqueta(ndb.Model):
    etiqueta = ndb.StringProperty(required=True)
    squab_key = ndb.KeyProperty(kind=Squab)