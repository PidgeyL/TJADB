import decimal
import requests
import zenora
from collections.abc import Mapping, Container
from flask           import url_for
from sys             import getsizeof
from lib.Config      import Configuration
_URL_ = Configuration().web_url

conf        = Configuration()
discord_api = zenora.APIClient(conf.discord_bot_key)

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


def uniq(*args):
    return sorted( set( [a for a in args if a] ) )


def rename_key(d, old, new):
    if d.get(old):
        d[new] = old
        del d[old]
    return d


def simify(data):
    if isinstance(data,(list, tuple, set)):
        items = []
        for item in data:
            items.append(simify(item))
        return items
    elif isinstance(data, dict):
        rename_key(data, 'title_orig',    'title')
        rename_key(data, 'subtitle_orig', 'subtitle')
        rename_key(data, 'name_orig',     'name')
        for key, val in data.items():
            data[key] = simify(val)
    return data


def deep_getsizeof(o, ids = None):
    if ids == None:
        ids = set()
    d = deep_getsizeof
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))
    if isinstance(o, str):
        return r
    if isinstance(o, Mapping):
        return r + sum(d(k, ids) + d(v, ids) for k, v in o.items())
    if isinstance(o, Container):
        return r + sum(d(x, ids) for x in o)
    return r


class DictObj(dict):
    def __getattr__(self, attr):
        return self[attr]
    def __setattr__(self, attr, value):
        self[attr] = value
    def as_dict(self):
        return self


def is_image_url(url):
    if not isinstance(url, str):
        return False
    if url[:7].lower() not in ('http://', 'https:/'):
        return False
    r = requests.head(url)
    if r.headers["content-type"].startswith("image/"):
        return True
    return False


def _url_for(profile):
    if _URL_.lower().startswith("https://"):
        return url_for(profile, _scheme='https', _external=True)
    return url_for(profile)


def discord_profile(id):
    u = discord_api.users.get_user(id)
    return {'name': u.username, 'pfp_url': u.avatar_url}
