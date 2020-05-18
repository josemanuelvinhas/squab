# Perfil

import webapp2
from webapp2_extras import jinja2
from webapp2_extras.users import users

from model.etiquetas import Etiqueta
from model.likes import Likes
from model.squabs import Squab


class PerfilHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        jinja = jinja2.get_jinja2(app=self.app)
        if usr:
            url_usr = users.create_logout_url("/")
            email_usr = usr.email()

            squabs = Squab.query(Squab.email == email_usr).order(-Squab.hora)
            etiquetas = Etiqueta.query()
            likes = Likes.query()

            lista_squabs = []
            for squab in squabs.fetch():
                diccionario = {}
                diccionario["login"] = squab.login
                diccionario["hora"] = squab.hora
                diccionario["texto"] = squab.texto
                lista_etiquetas = []
                for et in etiquetas.fetch():
                    if et.squab_key == squab.key:
                        lista_etiquetas.append(et)
                diccionario["etiquetas"] = lista_etiquetas
                nLikes = 0
                lista_login_likes = []
                for li in likes.fetch():
                    if li.squab_key == squab.key:
                        nLikes += 1
                        lista_login_likes.append(li.email.split("@")[0])
                diccionario["lista_login_likes"] = lista_login_likes
                diccionario["nLikes"] = nLikes
                diccionario["url_id"] = squab.key.urlsafe()
                lista_squabs.append(diccionario)

            valores_plantilla = {
                "url_usr": url_usr,
                "usr_nickname": usr.nickname().split("@")[0],
                "usr_email": usr.email(),
                "lista_squabs": lista_squabs,
            }
            self.response.write(jinja.render_template("perfil.html", **valores_plantilla))
        else:
            return self.redirect("/")


app = webapp2.WSGIApplication([
    ('/perfil', PerfilHandler)
], debug=True)
