import simplejson as json
import io
import os
import zipfile
from datetime            import date
from flask               import Flask, request, Response, send_file, render_template, abort
from functools           import wraps
from werkzeug.exceptions import NotFound

from lib.Config        import Configuration
from lib.DatabaseLayer import DatabaseLayer
from lib.objects       import Artist, Song, Source
from lib.TJA           import prepare_en_tja, get_file_type, clean_path, parse_tja

app  = Flask(__name__, static_folder='static',static_url_path='/static')
conf = Configuration()
dbl  = DatabaseLayer()

run_path = os.path.dirname(os.path.realpath(__file__))
app.config['ASSETS'] = os.path.join(run_path, 'assets')



def archive(song, orig=True):
    # Get data
    tja  = dbl.songs.read_tja(song)
    wave = dbl.songs.read_wave(song)
    meta = parse_tja(tja)
    bg   = None
    if song.obj_bg_video_picture:
        bg = dbl.songs.read_bg_video_picture(song)
    if not orig:
        tja = prepare_en_tja(tja, song, wave, bg=bg)
    # Make file names
    meta   = parse_tja(tja)
    folder = os.path.join(clean_path(meta['title']), )
    n_tja  = os.path.join(folder, folder)+'.tja'
    n_song = os.path.join(folder, meta['song'])
    n_info = os.path.join(folder, folder) + "_-_info.txt"
    n_bg   = None
    if bg:
        if   meta['movie'] and get_file_type(bg) in ['.mp4', '.wmv']:
            n_bg = os.path.join(folder, meta['movie'])
        elif meta['image'] and get_file_type(bg) in ['.png', '.jpg']:
            n_bg = os.path.join(folder, meta['picture'])
    # Zip everything
    blob = io.BytesIO()
    with zipfile.ZipFile(blob, "a", zipfile.ZIP_DEFLATED, False) as arch:
        arch.writestr(n_tja,  tja)
        arch.writestr(n_song, wave)
        arch.writestr(n_info, song.as_info_string(as_bytes=True))
        if n_bg:
            arch.writestr(n_bg, bg)
    blob.seek(0)
    return (blob, folder+'.zip')




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


@app.route('/download/orig/<id>', methods=['GET'])
def download_orig(id):
    try:
        song = dbl.songs.get_by_id(id)
        if song == None: abort(404)
        blob, name = archive(song, orig=True)
        return send_file(blob, mimetype="application/octet-stream",
                         as_attachment=True, download_name=name)
    except NotFound:
        abort(404)
    except Exception as e:
        print(e)
        abort(500)


@app.route('/download/eng/<id>', methods=['GET'])
def download_eng(id):
    try:
        song = dbl.songs.get_by_id(id)
        if song == None: abort(404)
        blob, name = archive(song, orig=False)
        return send_file(blob, mimetype="application/octet-stream",
                         as_attachment=True, download_name=name)
    except NotFound:
        abort(404)
    except Exception as e:
        print(e)
        abort(500)


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
