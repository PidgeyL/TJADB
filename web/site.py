import os
import string
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from collections   import defaultdict
from datetime      import date
from flask         import render_template, abort, send_from_directory, request, redirect
from flask_babel   import Babel
from flask_login   import LoginManager, current_user, login_required
from lib.functions   import number_format, uniq, DictObj
from web.api         import conf, dbl, app
from web.blueprints  import app_auth, load_user, app_profile

import web.api as api

# Babel Config
app.config['LANGUAGES'] = { 'en': 'English', 'es': 'Español', 'ja': '日本語'}
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

# Load site pieces
app.register_blueprint(app_profile) # Profile routes
app.register_blueprint(app_auth)    # User auth (Discord oauth)

# Discord OATH Config
app.config['SECRET_KEY'] = "Secret_Key"

# Auth config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user)


###################
# Logic Functions #
###################
# Works on any obj with .name_orig and name_en
def pager_prepare(obj_list):
    pdict = defaultdict(list)
    for obj in obj_list:
        if obj.name_en[0] in string.ascii_letters:
            pdict[obj.name_en[0].upper()].append(obj.as_dict())
        else:
            pdict['...'].append(obj.as_dict())
    for key, val in pdict.items():
        pdict[key] = sorted(val, key=lambda x: x['name_en'].lower())
    return pdict


##################
# ROUTE HANDLERS #
##################
@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys())

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/artists', methods=['GET'])
def artists():
    data = pager_prepare( api.api_artists() )
    return render_template('browse_names.html', names=data, link="/browse_artist/")


@app.route('/charters', methods=['GET'])
def charters():
    data = [DictObj({'name_en': x.charter_name, 'name_orig': x.charter_name,
             'id': x.id}) for x in api.api_charters() ]
    data = pager_prepare( data )
    return render_template('browse_names.html', names=data, link="/browse_charter/")


@app.route('/sources', methods=['GET'])
def sources():
    data = pager_prepare( api.api_sources() )
    return render_template('browse_names.html', names=data, link="/browse_source/")


@app.route('/browse', methods=['GET'])
def browse():
    data = api.api_browse()
    return render_template('browse.html', songlist=data)


@app.route('/browse_artist/<id>', methods=['GET'])
def browse_artist(id):
    data   = api.api_browse_artist(id)
    artist = dbl.artists.get_by_id(id)
    return render_template('artist.html', songlist=data, artist=artist)


@app.route('/browse_charter/<id>', methods=['GET'])
def browse_charter(id):
    data = api.api_browse_charter(id)
    user = dbl.users.get_by_id(id)
    return render_template('charter.html', songlist=data, charter=user)


@app.route('/browse_source/<id>', methods=['GET'])
def browse_source(id):
    data   = api.api_browse_source(id)
    source = dbl.sources.get_by_id(id)
    return render_template('source.html', songlist=data, source=source)


@app.route('/custom/nameplates', methods=['GET'])
def custom_nameplates():
    return render_template('custom/nameplates.html')


@app.route('/custom/dons', methods=['GET'])
def custom_dons():
    return render_template('custom/dons.html')


@app.route('/custom/puchichara', methods=['GET'])
def custom_puchichara():
    return render_template('custom/puchichara.html')


@app.route('/assets/<asset>', methods=['GET'])
def assets(asset):
    try:
        return send_from_directory(app.config['ASSETS'], asset, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/donate', methods=['GET'])
def donate():
    return render_template('donate.html')


###########
# Filters #
###########
@app.template_filter('number_format')
def number_format_filter(number):
    return number_format(number)

@app.template_filter('uniq')
def uniq_filter(args):
    return uniq(*args)

@app.template_filter('isnew')
def new_filter(day):
    td = date.today()
    return ( (td - day).days < 7 )



if __name__ == '__main__':
    app.run(host=conf.web_host, port=conf.web_port, debug=conf.web_debug)

