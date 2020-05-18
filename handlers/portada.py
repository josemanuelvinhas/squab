# Portada

import webapp2
from webapp2_extras import jinja2
from webapp2_extras.users import users

from model.etiquetas import Etiqueta
from model.likes import Likes
from model.squabs import Squab


class PortadaHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        jinja = jinja2.get_jinja2(app=self.app)
        if usr:
            url_usr = users.create_logout_url("/")
            squabs = Squab.query().order(-Squab.hora).fetch()

            usr_email = usr.email()
            lista_squabs = []
            for squab in squabs:
                diccionario = {}
                diccionario["login"] = squab.login
                diccionario["hora"] = squab.hora
                diccionario["texto"] = squab.texto
                diccionario["etiquetas"] = Etiqueta.query(Etiqueta.squab_key == squab.key).fetch()
                nLikes = 0
                diccionario["lista_login_likes"] = []
                diccionario["gusto"] = False
                for li in Likes.query(Likes.squab_key == squab.key):
                    nLikes += 1
                    diccionario["lista_login_likes"].append(li.email.split("@")[0])
                    if li.email == usr_email:
                        diccionario["gusto"] = True
                        diccionario["url_id_disgustar"] = li.key.urlsafe()
                diccionario["nLikes"] = nLikes
                diccionario["url_id"] = squab.key.urlsafe()
                lista_squabs.append(diccionario)

            valores_plantilla = {
                "url_usr": url_usr,
                "usr_nickname": usr.nickname().split("@")[0],
                "usr_email": usr.email(),
                "lista_squabs": lista_squabs,
            }
            self.response.write(jinja.render_template("portada.html", **valores_plantilla))
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/portada', PortadaHandler)
], debug=True)
