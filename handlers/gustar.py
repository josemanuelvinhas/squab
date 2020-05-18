# Gustar

import time

import webapp2
from google.appengine.ext import ndb
from webapp2_extras.users import users

from model.likes import Likes


class GustarHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        if usr:
            email = usr.email()
            id = self.request.get("id", "")
            ruta = self.request.get("ruta", "Desconodido")
            if ruta not in ["/portada", "/buscar"]:
                ruta = "/portada"
            if ruta == "/buscar":
                ruta += "?user=" + self.request.get("user", "")
                megusta = self.request.get("megusta", "off")
                if megusta == "on":
                    ruta += "&megusta=" + self.request.get("megusta", "off")
                for et in self.request.GET.getall("etiqueta"):
                    ruta += "&etiqueta=" + et

            sq = ndb.Key(urlsafe=id)
            lista_likes = Likes.query(ndb.AND(Likes.email == email,
                                              Likes.squab_key == sq
                                              ))
            if len(lista_likes.fetch()) == 0:
                lk = Likes(email=email,
                           squab_key=sq
                           )
                lk.put()
            time.sleep(1)
            return self.redirect(ruta)
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/gustar', GustarHandler)
], debug=True)
