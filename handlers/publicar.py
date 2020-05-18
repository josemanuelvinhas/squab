# encoding: utf-8
# Publicar
import re
import time

import webapp2
from webapp2_extras.users import users
from webapp2_extras import jinja2

from model.etiquetas import Etiqueta
from model.squabs import Squab


class PublicarHandler(webapp2.RequestHandler):
    def post(self):
        usr = users.get_current_user()
        jinja = jinja2.get_jinja2(app=self.app)
        if usr:
            url_usr = users.create_logout_url("/")
            mensaje = self.request.get("mensaje")
            ruta = self.request.get("ruta", "Desconocido")
            lista_etiquetas = self.request.POST.getall("etiqueta")

            lista_errores = self.comprobarCampos(lista_etiquetas, mensaje)

            if len(lista_errores) > 0:
                valores_plantilla = {
                    "url_usr": url_usr,
                    "usr_nickname": usr.nickname().split("@")[0],
                    "usr_email": usr.email(),
                    "lista_errores": lista_errores
                }
                self.response.write(jinja.render_template("error.html", **valores_plantilla))
            else:
                squab = Squab(email=usr.email(),
                              login=usr.nickname().split("@")[0],
                              texto=mensaje
                              )
                sq_key = squab.put()

                for i in lista_etiquetas:
                    etiqueta = Etiqueta(etiqueta=i)
                    etiqueta.squab_key = sq_key
                    etiqueta.put()

                time.sleep(1)
                lista_rutas_permitidas = ["/perfil", "/portada"]
                if ruta not in lista_rutas_permitidas:
                    ruta = "/portada"
                return self.redirect(ruta)
        else:
            return self.redirect("/")

    def comprobarCampos(self, lista_etiquetas, mensaje):
        lista_errores = []
        patron_etiquetas = re.compile('^[A-z0-9ñÑ]+$')
        for et in lista_etiquetas:
            if patron_etiquetas.match(et) == None:
                lista_errores.append(
                    "Error en la etiqueta: " + et + " --> No pueden estar vacias, no pueden contener espacios y solo se permiten numeros y letras sin acentos")
        if len(mensaje) <= 0:
            lista_errores.append("Error en el mensaje --> No puede ser vacio")
        return lista_errores


app = webapp2.WSGIApplication([
    ('/publicar', PublicarHandler)
], debug=True)
