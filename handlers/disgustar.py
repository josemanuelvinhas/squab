# Disgustar

import time

import webapp2
from google.appengine.ext import ndb
from webapp2_extras.users import users


class DisgustarHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        if usr:
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

            sq = ndb.Key(urlsafe=id).get()
            sq_key = sq.key
            sq_key.delete()
            time.sleep(1)
            return self.redirect(ruta)
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/disgustar', DisgustarHandler)
], debug=True)
