import collections
import json
import os
import polib
import sys

_TRANSLATIONS_ = os.path.join('etc', 'translations.json')
_PO_LOCATIONS_ = os.path.join('web', 'translations')
_MO_FILE_      = os.path.join('LC_MESSAGES', 'messages.mo')
_PO_FILE_      = os.path.join('LC_MESSAGES', 'messages.po')

def get_conf_path():
    run_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(run_path, '..', _TRANSLATIONS_)


def read_conf():
    t_path = get_conf_path()
    return json.loads(open(t_path, 'r').read())


def write_conf(data):
    t_path = get_conf_path()
    open(t_path, 'w').write(json.dumps(data, indent=4, ensure_ascii=False))


def add_locale(lang):
    data = read_conf()
    for key, langs in data.items():
      if lang not in langs:
          langs[lang] = []
    write_conf(data)


def generate():
    data   = read_conf()
    # Split the keys per language
    parsed = collections.defaultdict(dict)
    for key, langs in data.items():
        for lang, text in langs.items():
            parsed[lang][key] = ''.join(text)
    # Make an po file per language
    for lang, keys in parsed.items():
        po = polib.pofile('')
        for key, text in keys.items():
            po.append(polib.POEntry( msgid=key, msgstr=text))
        po_path = os.path.join(_PO_LOCATIONS_, lang, _PO_FILE_)
        os.makedirs(os.path.dirname(po_path), exist_ok=True)
        print(f'Generating "{po_path}"')
        po.save(po_path)


if __name__ == "__main__":
    import argparse
    argParser = argparse.ArgumentParser(description=f"Generate the web locale based on {_TRANSLATIONS_}")
    argParser.add_argument('action',            help='add/generate')
    argParser.add_argument('args',   nargs='?', help='arguments for the action')

    args = argParser.parse_args()

    if args.action.lower() == "add":
        lang = args.args
        if not lang:
            sys.exit("Specify a locale code (e.g. 'en')")
        add_locale(lang)
        sys.exit("Locale added")
    elif args.action.lower() == "generate":
        generate()
        sys.exit()
    print(f"Unknown action: {args.action}")
