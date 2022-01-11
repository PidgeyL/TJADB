import simplejson as json
import os
from datetime          import date
from flask             import Flask, request, Response, send_file, send_from_directory, render_template
from functools         import wraps

from lib.Config        import Configuration
from lib.DatabaseLayer import DatabaseLayer
from lib.objects       import Artist, Song, Source

app  = Flask(__name__, static_folder='static',static_url_path='/static')
conf = Configuration()
dbl  = DatabaseLayer()

#app.config['ASSETS'] = os.path.join(run_path, 'assets')



####################
# Helper Functions #
####################
def dictify(data):
    if isinstance(data,(list, tuple, set)):
        items = []
        for item in data:
            items.append(dictify(item))
        return items
    elif isinstance(data, dict):
        for key, val in data.items():
            data[key] = dictify(val)
    elif isinstance(data, (Artist, Source)):
        return data.as_dict()
    elif isinstance(data, (Song)):
        return data.as_api_dict()
    elif isinstance(data, date):
        return data.strftime('%Y-%m-%d')
    return data


##############
# Decorators #
##############
def api_reply(funct):
    @wraps(funct)
    def api_wrapper(*args, **kwargs):
        try:
            data = funct(*args, **kwargs)
            if request.url_rule.rule.lower().startswith('/api/'):
                data = dictify(data)
                data = json.dumps(data)
                return Response(data, mimetype='application/json'), 200
            else:
                return data
        except Exception as e:
            print(e)
            return Response('{"Error": "%s"}'%e, mimetype='application/json'), 500
    return api_wrapper


@app.route('/api/artists', methods=['GET'])
@api_reply
def api_artists():
    return dbl.artists.get_all()


@app.route('/api/artist/<id>', methods=['GET'])
@api_reply
def api_artist(id):
    return dbl.artists.get_by_id(id)


@app.route('/api/browse', methods=['GET'])
@api_reply
def api_browse():
    return dbl.songs.get_all()


@app.route('/api/sources', methods=['GET'])
@api_reply
def api_sources():
    return dbl.sources.get_all()


@app.route('/api/source/<id>', methods=['GET'])
@api_reply
def api_source(id):
    return dbl.sources.get_by_id(id)

##################
# Error Messages #
##################
@app.errorhandler(404)
def page_not_found(e):
    if request.path.startswith('/api/'):
        return '{"status": "Page Not Found", "Error": 404}', 404
    else:
        return render_template('404.html'), 404




if __name__ == '__main__':
    app.run(host=conf.web_host, port=conf.web_port, debug=conf.web_debug)
