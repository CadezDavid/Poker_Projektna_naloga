from funkcije import *
import bottle

@bottle.get('/')
def index():
    return bottle.template('homepage.tpl')