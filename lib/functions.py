import decimal

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
