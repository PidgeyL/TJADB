import decimal
import os
import sys

run_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(run_path, ".."))

from flask   import render_template, abort
from web.api import conf, dbl, app

import web.api as api

##################
# ROUTE HANDLERS #
##################
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/browse', methods=['GET'])
def browse():
    data = api.api_browse()
    return render_template('browse.html', songlist=data)


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


###########
# Filters #
###########
@app.template_filter('number_format')
def number_format(number):
    if isinstance(number, type(None)):
        return ''
    if isinstance(number, str):
        try:
            number = float(number)
        except:
            return number
    if isinstance(number, int) and number == 0:
        return ''
    if isinstance(number, (float, decimal.Decimal)) and number == int(number):
        number = int(number)
    return str(number)



if __name__ == '__main__':
    app.run(host=conf.web_host, port=conf.web_port, debug=conf.web_debug)

