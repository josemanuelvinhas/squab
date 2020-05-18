# Main

import webapp2
from webapp2_extras import jinja2
from webapp2_extras.users import users


class MainHandler(webapp2.RequestHandler):
    def get(self):
        usr = users.get_current_user()
        jinja = jinja2.get_jinja2(app=self.app)
        if usr:
            return self.redirect("/portada")
        else:
            url_usr = users.create_login_url("/portada")
            valores_plantilla = {"url_usr": url_usr}
            self.response.write(jinja.render_template("index.html", **valores_plantilla))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
