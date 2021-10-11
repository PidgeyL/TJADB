# Imports
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
from lib.TJA           import decode_tja, parse_tja
from etc.Settings      import Settings


# Variables
conf = Settings()
db   = DatabaseLayer()
app  = Flask(__name__, static_folder='static', static_url_path='/static')

app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024 # 25MB

####################
# Helper Functions #
####################
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
@app.route('/submit', methods=['GET'])
def submit():
    return render_template('submit.html', **get_autocomplete() )


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
