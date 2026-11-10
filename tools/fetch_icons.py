#!/usr/bin/env python3
"""Télécharge depuis le Vampire Survivors Wiki les icônes qui manquent dans images/.

    python3 tools/fetch_icons.py            # armes, objets et portraits de personnages manquants
    python3 tools/fetch_icons.py --dry-run  # liste ce qui serait téléchargé
    python3 tools/fetch_icons.py --index    # reconstruit seulement images/icons.json

Fichiers cherchés sur le wiki : « Icon-<Nom>.png » (armes, évolutions), « Sprite-<Nom>.png »
(objets passifs), « Select-<Nom>.png » (personnages). Si Pillow est installé (pip install pillow),
les images sont converties en WebP et les portraits réduits à 96 px ; sinon elles restent en PNG.
images/icons.json, lu par le jeu, est mis à jour à la fin.
"""
import argparse
import csv
import io
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, 'images')
API = 'https://vampire.survivors.wiki/api.php'
UA = {'User-Agent': 'VampireSurvivordle-icons/1.0'}
KINDS = {  # dossier : préfixes de fichier essayés sur le wiki, dans l'ordre
    'weapons': ['Icon-', 'Sprite-'],
    'items': ['Sprite-', 'Icon-'],
    'characters': ['Select-', 'Sprite-'],
}

try:
    from PIL import Image
except ImportError:
    Image = None


def slug(name):
    """Même règle que slug() dans index.html."""
    s = unicodedata.normalize('NFD', name)
    s = ''.join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r'[^a-z0-9]+', '_', s).strip('_')


def split_list(s):
    return [t.strip() for t in (s or '').split(',') if t.strip() and t.strip() not in ('Aucun', 'Aucune', 'N/A')]


def read(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def wanted():
    """Noms affichés par le jeu, par type d'icône."""
    weapons, chars, evos = read('data.csv'), read('characters.csv'), read('evolutions.csv')
    names = {
        'weapons': {w['Nom'] for w in weapons} | {e['Nom'] for e in evos}
                   | {x for e in evos for x in split_list(e['Armes'])} | {x for c in chars for x in split_list(c['Arme'])},
        'items': {x for w in weapons for x in split_list(w['Evolution Item'])} | {x for e in evos for x in split_list(e['Objets'])},
        'characters': {c['Nom'] for c in chars},
    }
    return {k: sorted(v) for k, v in names.items()}


def existing(kind):
    folder = os.path.join(IMAGES, kind)
    if not os.path.isdir(folder):
        return {}
    return {os.path.splitext(f)[0]: f for f in os.listdir(folder) if f.lower().endswith(('.webp', '.png'))}


def build_index():
    index = {kind: existing(kind) for kind in KINDS}
    with open(os.path.join(IMAGES, 'icons.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, separators=(',', ':'), sort_keys=True)
    return index


def api(**params):
    params.update(format='json', formatversion='2')
    req = urllib.request.Request(API + '?' + urllib.parse.urlencode(params), headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def image_urls(titles):
    """{titre de fichier: url} pour les fichiers qui existent sur le wiki."""
    found = {}
    for i in range(0, len(titles), 50):
        r = api(action='query', prop='imageinfo', iiprop='url', titles='|'.join(titles[i:i + 50]))
        back = {x['to']: x['from'] for x in r['query'].get('normalized', [])}
        for p in r['query']['pages']:
            if p.get('imageinfo'):
                found[back.get(p['title'], p['title'])] = p['imageinfo'][0]['url']
        time.sleep(0.3)
    return found


def download(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def save(kind, name, raw):
    folder = os.path.join(IMAGES, kind)
    os.makedirs(folder, exist_ok=True)
    if Image is not None:
        img = Image.open(io.BytesIO(raw)).convert('RGBA')
        if kind == 'characters' and max(img.size) > 96:
            img.thumbnail((96, 96), Image.NEAREST)
        path = os.path.join(folder, slug(name) + '.webp')
        img.save(path, 'WEBP', lossless=True)
    else:
        path = os.path.join(folder, slug(name) + '.png')
        with open(path, 'wb') as f:
            f.write(raw)
    return path


def missing():
    names = wanted()
    return {kind: [n for n in names[kind] if slug(n) not in existing(kind)] for kind in KINDS}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--index', action='store_true', help='reconstruire images/icons.json sans rien télécharger')
    args = ap.parse_args()

    if args.index:
        index = build_index()
        print(', '.join(f'{k} {len(v)}' for k, v in index.items()), '→ images/icons.json')
        return

    todo = missing()
    print('Manquantes : ' + ', '.join(f'{k} {len(v)}' for k, v in todo.items()))
    if Image is None:
        print('(Pillow absent : les images seront gardées en PNG, sans conversion.)', file=sys.stderr)
    not_found = []
    for kind, names in todo.items():
        if not names:
            continue
        candidates = {n: [f'File:{p}{n}.png' for p in KINDS[kind]] for n in names}
        urls = image_urls([t for ts in candidates.values() for t in ts])
        for name in names:
            url = next((urls[t] for t in candidates[name] if t in urls), None)
            if not url:
                not_found.append(f'{kind}: {name}')
                continue
            if args.dry_run:
                print(f'  {kind}: {name} ← {url}')
                continue
            print(f'  {kind}: {name} → {os.path.relpath(save(kind, name, download(url)), ROOT)}')
            time.sleep(0.2)
    if not args.dry_run:
        index = build_index()
        print('images/icons.json : ' + ', '.join(f'{k} {len(v)}' for k, v in index.items()))
    if not_found:
        print(f'Introuvables sur le wiki ({len(not_found)}) : ' + ', '.join(not_found))


if __name__ == '__main__':
    main()
