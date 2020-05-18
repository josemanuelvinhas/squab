# encoding: utf-8
# Buscar
import re

import webapp2
from google.appengine.ext import ndb
from webapp2_extras import jinja2
from webapp2_extras.users import users

from model.etiquetas import Etiqueta
from model.likes import Likes
from model.squabs import Squab


class BuscarHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        jinja = jinja2.get_jinja2(app=self.app)
        if usr:
            url_usr = users.create_logout_url("/")
            usr_email = usr.email()
            filtro = True
            filtro_likes = ""
            filtro_etiquetas = ""
            lista_squads_definitiva = []
            resultados_et = True
            resultados_lk = True
            megusta = self.request.get("megusta", "")
            lista_etiquetas_get = self.request.GET.getall("etiqueta")
            filtro_user = self.request.get("user")

            lista_errores = self.comprobarCampos(lista_etiquetas_get, filtro_user)

            if len(lista_errores) > 0:
                valores_plantilla = {
                    "url_usr": url_usr,
                    "usr_nickname": usr.nickname().split("@")[0],
                    "usr_email": usr.email(),
                    "lista_errores": lista_errores
                }
                self.response.write(jinja.render_template("error.html", **valores_plantilla))
            else:
                if megusta == "on":
                    megusta = True
                    filtro_likes = [lk.squab_key for lk in Likes.query(Likes.email == usr_email)]
                    resultados_lk = len(filtro_likes) != 0
                else:
                    megusta == ""

                if len(lista_etiquetas_get) > 0:
                    filtro_etiquetas = [et.squab_key for et in
                                        Etiqueta.query(Etiqueta.etiqueta.IN(lista_etiquetas_get))]
                    resultados_et = len(filtro_etiquetas) != 0

                if resultados_lk and resultados_et:
                    if filtro_likes != "" and filtro_etiquetas != "" and filtro_user != "":
                        lista_squabs_filtrada = Squab.query(Squab.login == filtro_user,
                                                            ndb.AND(Squab.key.IN(filtro_etiquetas),
                                                                    Squab.key.IN(filtro_likes)
                                                                    )
                                                            ).order(-Squab.hora).fetch()
                    elif filtro_likes != "" and filtro_etiquetas != "":
                        lista_squabs_filtrada = Squab.query(ndb.AND(Squab.key.IN(filtro_etiquetas),
                                                                    Squab.key.IN(filtro_likes)
                                                                    )
                                                            ).order(-Squab.hora).fetch()
                    elif filtro_etiquetas != "" and filtro_user != "":
                        lista_squabs_filtrada = Squab.query(Squab.login == filtro_user,
                                                            Squab.key.IN(filtro_etiquetas)).order(
                            -Squab.hora).fetch()
                    elif filtro_likes != "" and filtro_user != "":
                        lista_squabs_filtrada = Squab.query(Squab.login == filtro_user,
                                                            Squab.key.IN(filtro_likes)).order(
                            -Squab.hora).fetch()
                    elif filtro_likes != "":
                        lista_squabs_filtrada = Squab.query(Squab.key.IN(filtro_likes)).order(-Squab.hora).fetch()
                    elif filtro_etiquetas != "":
                        lista_squabs_filtrada = Squab.query(Squab.key.IN(filtro_etiquetas)).order(-Squab.hora).fetch()
                    elif filtro_user != "":
                        lista_squabs_filtrada = Squab.query(Squab.login == filtro_user).order(-Squab.hora).fetch()
                    else:
                        lista_squabs_filtrada = Squab.query().order(-Squab.hora).fetch()
                        filtro = False

                for squab in lista_squabs_filtrada:
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
                    lista_squads_definitiva.append(diccionario)

                valores_plantilla = {
                    "url_usr": url_usr,
                    "usr_nickname": usr.nickname().split("@")[0],
                    "usr_email": usr.email(),
                    "lista_squabs": lista_squads_definitiva,
                    "lista_etiquetas": lista_etiquetas_get,
                    "user": filtro_user,
                    "megusta": megusta,
                    "filtro": filtro
                }
                self.response.write(jinja.render_template("buscar.html", **valores_plantilla))
        else:
            return self.redirect("/")

    def comprobarCampos(self, lista_etiquetas, user):
        lista_errores = []
        patron_etiquetas = re.compile('^[A-z0-9ñÑ]+$')
        for et in lista_etiquetas:
            if patron_etiquetas.match(et) == None:
                lista_errores.append(
                    "Error en la etiqueta: " + et + " --> No pueden estar vacias, no pueden contener espacios y solo se permiten numeros y letras sin acentos")
        patron_user = re.compile('^[^\s]*$')
        if patron_user.match(user) == None:
            lista_errores.append("Error en el apodo: " + user + " --> No puede contener espacios")
        return lista_errores


app = webapp2.WSGIApplication([
    ('/buscar', BuscarHandler)
], debug=True)
