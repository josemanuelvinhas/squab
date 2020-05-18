# Likes

from google.appengine.ext import ndb
from model.squabs import Squab


class Likes(ndb.Model):
    email = ndb.StringProperty(required=True)
    squab_key = ndb.KeyProperty(kind=Squab)
    hora = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
