# Eliminar

import time

import webapp2
from google.appengine.ext import ndb
from webapp2_extras.users import users

from model.etiquetas import Etiqueta


class EliminarHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        if usr:
            id = self.request.get("id", "")
            ruta = self.request.get("ruta", "Desconodido")

            if ruta not in ["/perfil", "/portada", "/buscar"]:
                ruta = "/portada"
            if ruta == "/buscar":
                ruta += "?user=" + self.request.get("user", "")
                megusta = self.request.get("megusta", "off")
                if megusta == "on":
                    ruta += "&megusta=" + self.request.get("megusta", "off")
                for et in self.request.GET.getall("etiqueta"):
                    ruta += "&etiqueta=" + et

            sq = ndb.Key(urlsafe=id).get()
            if sq.email == usr.email():
                sq_key = sq.key
                etiquetas = Etiqueta().query(Etiqueta.squab_key == sq_key)
                for et in etiquetas:
                    et.key.delete()
                sq_key.delete()
            time.sleep(1)

            return self.redirect(ruta)
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/eliminar', EliminarHandler)
], debug=True)
