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
