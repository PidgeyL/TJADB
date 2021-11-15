# Imports
import csv
import json
import logging
import os
import signal
import sys
import time
from functools import wraps

from flask               import Flask, request, Response, render_template, abort, jsonify
from logging.handlers    import RotatingFileHandler
from tornado.httpserver  import HTTPServer
from tornado.ioloop      import IOLoop
from tornado.wsgi        import WSGIContainer
from werkzeug.exceptions import NotFound

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from lib.DatabaseLayer import DatabaseLayer
from lib.TJA           import decode_tja, parse_tja, clean_path
from etc.Settings      import Settings

_FIELDS_ = ['title_orig', 'title_eng', 'subtitle_orig', 'subtitle_eng',
            'artist_orig', 'artist_eng', 'charter', 'bpm', 'vetted', 'd_kantan',
            'd_futsuu', 'd_muzukashii', 'd_oni', 'd_ura', 'source_orig',
            'source_eng', 'genre', 'comments', 'video_link', 'path', 'songpath',
            'tja_added', 'tja_updated']

# Variables
conf = Settings()
db   = DatabaseLayer()
app  = Flask(__name__, static_folder='static', static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024 # 25MB
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024 # 250MB
app.config['UPLOAD_FOLDER'] = '/data/test/upload'
app.config['UPLOAD_DATA']   = '/data/test/upload_data.csv'
####################
# Helper Functions #
####################
def write_line(data):
    data = [data]
    # If file does not exist: add header
    if not os.path.isfile(app.config['UPLOAD_DATA']):
        data = [_FIELDS_] + data
    # Write to file
    with open(app.config['UPLOAD_DATA'], mode='a', encoding="utf-8") as _f:
        writer = csv.writer(_f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
        for line in data:
            writer.writerow(line)


def get_autocomplete():
    songs   = db.songs.get_all()
    artists = {song.artist_orig : song.artist_eng  for song in songs}
    artists = sorted([(k, v) for k, v in artists.items()], key=lambda x: x[1])
    sources = {song.source_orig : song.source_eng  for song in songs}
    sources = sorted([(k, v) for k, v in sources.items()], key=lambda x: x[1])
    genres  = ["%s (%s)"%(g.name_eng, g.genre) for g in db.genres.get_all()]
    return {"artist_orig": [a[0] for a in artists],
            "artist_eng":  [a[1] for a in artists],
            "source_orig": [s[0] for s in sources],
            "source_eng":  [s[1] for s in sources],
            "genres":      genres,
            "charters":    [c.name for c in db.charters.get_all()]}


##################
# ROUTE HANDLERS #
##################
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    keep = {}
    if request.method == "POST":
        try:
            # Grab files
            tja = request.files['tja_file']
            ogg = request.files['ogg_file']
            # Get all the metadata
            line = []
            for field in _FIELDS_:
                if   field == 'vetted':
                    line.append("False")
                elif field == 'path':
                    line.append(None) # Skip for now, since it's generated later
                elif field == 'songpath':
                    line.append(ogg.filename)
                else:
                    line.append(request.form[field])
                    if field == 'genre':
                        line[-1] = line[-1].split("(")[1][:-1]
            # Make file path
            title = clean_path(line[_FIELDS_.index('title_orig')])
            chart = clean_path(line[_FIELDS_.index('charter')])
            tja_path = os.path.join(app.config['UPLOAD_FOLDER'], chart, title,
                                    title+'.tja')
            ogg_path = os.path.join(app.config['UPLOAD_FOLDER'], chart, title,
                                    clean_path(line[_FIELDS_.index('songpath')]))
            line[_FIELDS_.index('path')] = tja_path
            # Prevent double uploads
            if os.path.exists(tja_path):
                raise(Exception("Song already Uploaded"))
            # Make dirs
            if not os.path.exists(os.path.dirname(tja_path)):
                os.makedirs(os.path.dirname(tja_path))
            # Save files
            tja.save(tja_path)
            ogg.save(ogg_path)
            # Save info
            write_line(line)
            # send back "keep" args
            if 'artist_keep'   in request.form.keys():
                keep['artist_orig'] = request.form['artist_orig']
                keep['artist_eng']  = request.form['artist_eng']
            if 'source_keep'   in request.form.keys():
                keep['source_orig'] = request.form['source_orig']
                keep['source_eng']  = request.form['source_eng']
            if 'genre_keep'    in request.form.keys():
                keep['genre'] = request.form['genre']
            if 'charter_keep'  in request.form.keys():
                keep['charter'] = request.form['charter']
            if 'comments_keep' in request.form.keys():
                keep['comments'] = request.form['comments']
        except Exception as e:
            return "Error: " + str(e)
    return render_template('submit.html', **get_autocomplete(), keep=keep )


@app.route('/parse_tja', methods=['post'])
def _parse_tja():
    if 'file' not in request.files:
        print('No file part')
        return jsonify({'status': 'failure', 'message': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        print('No selected file')
        return jsonify({'status': 'failure', 'message': 'No file sent'})
    try:
        tja  = decode_tja( file.stream.read() )
        meta = {'status': 'success', 'data': parse_tja(tja)}
        return jsonify(meta)
    except Exception as e:
        print(e)
        return jsonify({'status': 'failure', 'message': 'Could not parse TJA'})


##################
# Error Messages #
##################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


###########
# Filters #
###########
@app.template_filter('keep')
def keep_filter(field):
    return field.split('_')[0]


########################
# Web Server Functions #
########################
# signal handlers
def sig_handler(sig, frame):
    print('Caught signal: %s' % sig)
    IOLoop.instance().add_callback(self.shutdown)

def shutdown(self):
    MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3
    print('Stopping http server')
    http_server.stop()

    print('Will shutdown in %s seconds ...' % MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = IOLoop.instance()
    deadline = time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            print('Shutdown')
    stop_loop()


if __name__ == '__main__':
    if conf.debug:
        # start debug flask server
        app.run(host=conf.host, port=conf.port, debug=True)
    else:
        # start asynchronous server using tornado wrapper for flask
        # ssl connection
        print("Server starting...")
        if conf.ssl:
            ssl_options = {"certfile": os.path.join(run_path, "../", conf.certfile),
                           "keyfile": os.path.join(run_path, "../", conf.keyfile)}
        else:
           ssl_options = None
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGINT,  sig_handler)

        http_server = HTTPServer(WSGIContainer(app), ssl_options=ssl_options)
        http_server.bind(conf.port, address=conf.host)
        http_server.start(0)  # Forks multiple sub-processes
        IOLoop.instance().start()
