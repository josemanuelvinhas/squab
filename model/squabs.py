# Squabs

from google.appengine.ext import ndb


class Squab(ndb.Model):
    email = ndb.StringProperty(required=True, indexed=True)
    login = ndb.StringProperty(required=True)
    texto = ndb.StringProperty(required=True)
    hora = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
