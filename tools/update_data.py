#!/usr/bin/env python3
"""Met à jour les CSV de Vampire Survivordle depuis le Vampire Survivors Wiki.

Utilisation (depuis la racine du dépôt, Python 3.8+, aucune dépendance) :

    python3 tools/update_data.py              # télécharge le wiki puis met à jour les CSV
    python3 tools/update_data.py --derive     # recalcule seulement les colonnes déduites
    python3 tools/update_data.py --dry-run    # affiche le rapport sans rien écrire

Règles :
- Les armes et personnages déjà présents gardent leurs champs rédigés à la main
  (Tags, Description, Unlock, années corrigées…). Les écarts avec le wiki sont listés
  dans le rapport ; --overwrite remplace les champs factuels par ceux du wiki.
- Les nouvelles armes reçoivent « À compléter » dans Tags, Colors et Unlock Time : les remplir à la main.
- evolutions.csv est entièrement reconstruit à partir du wiki.
- Colonnes déduites, recalculées à chaque fois : Unlock Type, Weapon Tags (personnages),
  Base Tags et Release (évolutions).

Après une mise à jour, régénérer le calendrier : python3 tools/build_calendar.py
"""
import argparse
import csv
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = 'https://vampire.survivors.wiki/api.php'
CACHE = os.path.join(ROOT, 'tools', 'wiki_cache.json')

SOURCES = {'': 'Jeu de base', 'lm': 'Legacy of Moonspell', 'bm': 'Legacy of the Bloodmoon',
           'tf': 'Tides of the Foscari', 'em': 'Emergency Meeting', 'og': 'Operation Guns',
           'oc': 'Ode to Castlevania', 'ed': 'Emerald Diorama', 'ac': 'Ante Chamber'}
STATS = [('recovery', 'Recovery'), ('armor', 'Armor'), ('movespeed', 'Move Speed'), ('might', 'Might'),
         ('speed', 'Speed'), ('duration', 'Duration'), ('area', 'Area'), ('cooldown', 'Cooldown'),
         ('amount', 'Amount'), ('revival', 'Revival'), ('magnet', 'Magnet'), ('luck', 'Luck'),
         ('growth', 'Growth'), ('greed', 'Greed'), ('curse', 'Curse'), ('reroll', 'Reroll'),
         ('skip', 'Skip'), ('banish', 'Banish')]
# Tags fusionnés : un même concept = un seul mot, sinon les cases orange perdent leur sens.
TAG_SYNONYMS = {'Explosion': 'Explosive', 'Explosions': 'Explosive', 'Spinning': 'Spin', 'Piercing': 'Pierce',
                'Penetrating': 'Pierce', 'Freezing': 'Freeze', 'Ice': 'Freeze', 'Healing': 'Heal', 'Waves': 'Wave',
                'Heavy': 'High Damage', 'Powerful': 'High Damage', 'Darkness': 'Shadow', 'Straight': 'Linear',
                'Boost': 'Buff', 'Double': 'Multi-shot'}
# Types de déblocage corrigés à la main quand la détection automatique se trompe.
UNLOCK_TYPE_OVERRIDES = {'Megalo Miang Moonspell': 'Évolution', 'Megalo Sargon': 'Évolution',
                         "Baal'Thamut": 'Évolution', 'Megalo Dracula': 'Énigme'}


# ---------------------------------------------------------------- wiki

def api(**params):
    params.update(format='json', formatversion='2')
    url = API + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'VampireSurvivordle-updater/1.0'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 * (attempt + 1))


def embedded_in(template):
    titles, cont = [], {}
    while True:
        r = api(action='query', list='embeddedin', eititle=template, eilimit='500', einamespace='0', **cont)
        titles += [x['title'] for x in r['query']['embeddedin']]
        if 'continue' not in r:
            return titles
        cont = r['continue']


def page_texts(titles):
    out = {}
    for i in range(0, len(titles), 50):
        batch = titles[i:i + 50]
        r = api(action='query', prop='revisions', rvprop='content', rvslots='main', redirects='1', titles='|'.join(batch))
        back = {x['to']: x['from'] for x in r['query'].get('redirects', [])}
        for x in r['query'].get('normalized', []):
            back.setdefault(x['to'], x['from'])
        for p in r['query']['pages']:
            name = back.get(p['title'], p['title'])
            out[name] = p['revisions'][0]['slots']['main']['content'] if 'revisions' in p else ''
        time.sleep(0.5)
    return out


def download():
    print('Téléchargement du wiki…', file=sys.stderr)
    chars = page_texts(embedded_in('Template:Infobox Character'))
    weapons = page_texts(embedded_in('Template:Infobox Weapon'))
    patches = sorted({p for t in list(chars.values()) + list(weapons.values()) for p in [intro_patch(t)] if p})
    return {'characters': chars, 'weapons': weapons, 'patches': page_texts(patches),
            'downloaded': datetime.datetime.now().isoformat(timespec='seconds')}


# ---------------------------------------------------------------- lecture du wikitexte

def template(text, name):
    """Champs d'un modèle {{name|clé=valeur…}}, en respectant les {{ }} et [[ ]] imbriqués."""
    start = text.find('{{' + name)
    if start < 0:
        return {}
    depth, end = 0, start
    while end < len(text):
        if text.startswith('{{', end):
            depth += 1
            end += 2
            continue
        if text.startswith('}}', end):
            depth -= 1
            end += 2
            if depth == 0:
                break
            continue
        end += 1
    body = text[start + 2 + len(name):end - 2]
    parts, cur, d, k = [], '', 0, 0
    while k < len(body):
        two = body[k:k + 2]
        if two in ('{{', '[['):
            d += 1
            cur += two
            k += 2
            continue
        if two in ('}}', ']]'):
            d -= 1
            cur += two
            k += 2
            continue
        if body[k] == '|' and d == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += body[k]
        k += 1
    parts.append(cur)
    fields = {}
    for p in parts:
        m = re.match(r'\s*([^=]+?)\s*=\s*(.*)$', p, re.S)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields


def clean(s):
    s = s or ''
    s = re.sub(r'\{\{[Ss]link\|([^}|]+)(?:\|[^}]*?txt=([^}|]+))?[^}]*\}\}', lambda m: m.group(2) or m.group(1), s)
    s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]+)\]\]', r'\1', s)
    s = re.sub(r'\{\{[^}]*\}\}', '', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = s.replace("'''", '').replace("''", '')
    return re.sub(r'\s+', ' ', s).strip()


def year_of(s):
    m = re.search(r'(20\d\d)', s or '')
    return int(m.group(1)) if m else None


def parse_date(s):
    s = (s or '').strip()
    for fmt in ('%d %B %Y', '%B %d %Y', '%B %d, %Y'):
        try:
            return datetime.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def history(text):
    """Entrées {{UL|…|date=…}} de l'historique, avec leur texte."""
    out = []
    for m in re.finditer(r'\{\{UL\|([^}]*)\}\}\s*\n((?:\*\*[^\n]*\n?)*)', text):
        date = re.search(r'(?:^|\|)date=([^|]*)', m.group(1))
        out.append({'date': date.group(1).strip() if date else '', 'text': m.group(2)})
    return out


def added_year(text):
    years = [year_of(h['date']) for h in history(text) if re.search(r'Added to (the )?game|Released', h['text'], re.I)]
    years = [y for y in years if y]
    return years[-1] if years else None


def intro_patch(text):
    m = re.search(r'(?:introduced|added) in \[\[((?:Patch|Version|Updates/)[^\]|]*)', text or '', re.I)
    return m.group(1) if m else None


def patch_year(text):
    m = re.search(r'\{\{News\|[^}]*?date=([^|}]*)', text or '') or re.search(r'date\s*=\s*([^|\n}]*)', text or '')
    return year_of(m.group(1)) if m else None


def split_list(s):
    return [t.strip() for t in (s or '').split(',') if t.strip()]


def unlock_type(text):
    l = text.lower()
    if 'available from the start' in l: return 'Départ'
    if 'coffin' in l: return 'Cercueil'
    if re.match(r'(fully )?evolv|unite |obtain the |evolve', l): return 'Évolution'
    if re.match(r'get .* to level', l): return "Niveau d'arme"
    if l.startswith('survive 20 minutes'): return 'Survie 20 min'
    if re.search(r'defeat(ing)? (a total of )?[\d,]+ |defeat 1 enemy|slay [\d,]+|try 3000|3,000,000', l): return 'Ennemis vaincus'
    if re.match(r'(earn|recover|complete|master|survive the|reach level|die a total|hold the|find \d+)', l): return 'Exploit'
    if re.search(r'\bdefeat\b', l): return 'Boss'
    return 'Énigme'


# ---------------------------------------------------------------- CSV

def read_csv(name):
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        return [], []
    with open(path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        return list(r), r.fieldnames


def write_csv(name, rows, fields):
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n', extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------- construction

def wiki_weapons(raw, char_years):
    """Armes « Normal » du wiki, au format de data.csv."""
    out = {}
    patch_years = {p: patch_year(t) for p, t in raw['patches'].items()}
    dlc_years = {}
    for t in raw['characters'].values():
        box = template(t, 'Infobox Character')
        y = year_of(box.get('release') or box.get('release1'))
        d = box.get('dlc', '')
        if y and (d not in dlc_years or y < dlc_years[d]):
            dlc_years[d] = y
    for title, text in raw['weapons'].items():
        box = template(text, 'Infobox Weapon')
        if box.get('type') != 'Normal':
            continue
        name = re.sub(r' \(weapon\)$', '', title)
        year = added_year(text) or patch_years.get(intro_patch(text)) or char_years.get(name) or dlc_years.get(box.get('dlc', ''))
        items = [clean(box.get(k)).replace('Armor (item)', 'Armor') for k in ('evolution-item', 'evolution-item2')]
        out[name] = {
            'Nom': name, 'Tags': 'À compléter', 'Colors': 'À compléter',
            'Evolution Item': ', '.join(i for i in items if i) or 'Aucun',
            'Base Damage': clean(box.get('damage')) or 'N/A',
            'Max Level': clean(box.get('max-level')) or 'N/A',
            'Unlock Time': 'À compléter',
            'Release': str(year) if year else 'N/A',
            'Source': SOURCES.get(box.get('dlc', ''), box.get('dlc', '')),
            'Evolution': clean(box.get('evolution')).replace(' (weapon)', '') or 'Aucune',
            'Description': clean(box.get('caption')),
        }
    return out


def wiki_evolutions(raw):
    weapon_titles = {re.sub(r' \(weapon\)$', '', t) for t in raw['weapons']}
    out = []
    for title, text in raw['weapons'].items():
        box = template(text, 'Infobox Weapon')
        if box.get('type') not in ('Evolution', 'Union'):
            continue
        req = [clean(box.get(f'requires{i}')) for i in range(1, 5)]
        req = [r for r in req if r]
        weapons = [r for r in req if r in weapon_titles]
        items = [r.replace('Armor (item)', 'Armor') for r in req if r not in weapon_titles]
        if not weapons:
            continue
        out.append({'Nom': re.sub(r' \(weapon\)$', '', title), 'Type': 'Union' if box['type'] == 'Union' else 'Évolution',
                    'Armes': ', '.join(weapons), 'Objets': ', '.join(items) or 'Aucun',
                    'Source': SOURCES.get(box.get('dlc', ''), box.get('dlc', ''))})
    return out


def wiki_characters(raw):
    out = {}
    for title, text in raw['characters'].items():
        box = template(text, 'Infobox Character')
        get = lambda k: next((box[x] for x in (k, k + '1') if box.get(x) and box[x] not in ('-', 'N/A')), '')
        name = re.sub(r' \(character\)$', '', title)
        weapon = clean(get('weapon')) or clean(box.get('hidden weapon'))
        weapons = [w for w in re.split(r'\s*[;,]\s*', weapon) if w and w.lower() not in ('no', 'n/a')]
        hp = get('maxhealth')
        release = parse_date(get('release'))
        if not release:  # personnage encore en bêta : date de sa première entrée d'historique
            dates = [parse_date(h['date']) for h in history(text)]
            dates = [d for d in dates if d]
            release = min(dates) if dates else 'N/A'
        out[name] = {
            'Nom': name, 'Arme': ', '.join(weapons) or 'N/A',
            'Source': SOURCES.get(box.get('dlc', ''), box.get('dlc', '')),
            'Secret': 'Oui' if (box.get('secret') or '').lower() == 'yes' else 'Non',
            'Max Health': hp if re.fullmatch(r'\d+', hp) else 'N/A',
            'Bonus': ', '.join(label for key, label in STATS if get(key)) or 'Aucun',
            'Release': release,
            'Description': clean(get('description')),
            'Unlock': 'Available from the start.' if clean(get('unlock')).lower() == 'default' else clean(get('unlock')),
        }
    return out


def derive(weapons, characters, evolutions):
    """Recalcule les colonnes déduites à partir des tags des armes."""
    for w in weapons:
        tags = []
        for t in split_list(w['Tags']):
            t = TAG_SYNONYMS.get(t, t)
            if t not in tags:
                tags.append(t)
        w['Tags'] = ', '.join(tags)
    tags = {w['Nom']: split_list(w['Tags']) for w in weapons if w['Tags'] != 'À compléter'}
    years = {w['Nom']: w['Release'] for w in weapons}
    evo_bases = {e['Nom']: split_list(e['Armes']) for e in evolutions}

    def bases(name, seen=()):
        if name in tags:
            return [name]
        if name in evo_bases and name not in seen:
            return [b for x in evo_bases[name] for b in bases(x, seen + (name,))]
        return []

    for c in characters:
        c['Unlock Type'] = UNLOCK_TYPE_OVERRIDES.get(c['Nom']) or unlock_type(c['Unlock'])
        b = {x for w in split_list(c['Arme']) for x in bases(w)}
        c['Weapon Tags'] = ', '.join(sorted({t for x in b for t in tags[x]})) or 'N/A'
    for e in evolutions:
        b = {x for w in split_list(e['Armes']) for x in bases(w)}
        e['Base Tags'] = ', '.join(sorted({t for x in b for t in tags[x]})) or 'N/A'
        ys = [int(years[x]) for x in b if str(years.get(x, '')).isdigit()]
        e['Release'] = str(max(ys)) if ys else 'N/A'


def merge(current, fresh, factual, overwrite, label, report):
    """Garde les lignes existantes, ajoute les nouvelles, signale les écarts factuels."""
    by_name = {r['Nom']: r for r in current}
    for name, new in fresh.items():
        if name not in by_name:
            current.append(new)
            report.append(f'+ {label} ajouté : {name}')
            continue
        row = by_name[name]
        for k in factual:
            if new.get(k) and new[k] != 'N/A' and row.get(k) != new[k]:
                report.append(f'~ {label} {name} · {k} : CSV « {row.get(k)} » / wiki « {new[k]} »' + (' → remplacé' if overwrite else ''))
                if overwrite:
                    row[k] = new[k]
    for name in by_name:
        if name not in fresh:
            report.append(f'? {label} absent du wiki (conservé) : {name}')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--derive', action='store_true', help='recalculer seulement les colonnes déduites (sans réseau)')
    ap.add_argument('--cache', action='store_true', help='réutiliser tools/wiki_cache.json au lieu de retélécharger')
    ap.add_argument('--overwrite', action='store_true', help='remplacer les champs factuels par ceux du wiki')
    ap.add_argument('--dry-run', action='store_true', help="n'écrire aucun fichier")
    args = ap.parse_args()

    weapons, w_fields = read_csv('data.csv')
    characters, c_fields = read_csv('characters.csv')
    evolutions, _ = read_csv('evolutions.csv')
    report = []

    if not args.derive:
        if args.cache and os.path.exists(CACHE):
            raw = json.load(open(CACHE, encoding='utf-8'))
        else:
            raw = download()
            if not args.dry_run:
                json.dump(raw, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
        fresh_chars = wiki_characters(raw)
        char_years = {}
        for c in fresh_chars.values():
            y = year_of(c['Release'])
            for w in split_list(c['Arme']):
                if y and (w not in char_years or y < char_years[w]):
                    char_years[w] = y
        merge(weapons, wiki_weapons(raw, char_years),
              ['Evolution Item', 'Base Damage', 'Max Level', 'Release', 'Source', 'Evolution'], args.overwrite, 'arme', report)
        merge(characters, fresh_chars,
              ['Arme', 'Source', 'Secret', 'Max Health', 'Bonus', 'Release'], args.overwrite, 'personnage', report)
        evolutions = wiki_evolutions(raw)
        report.append(f'= {len(evolutions)} évolutions et unions reconstruites')

    derive(weapons, characters, evolutions)
    for col, label in (('Tags', 'Tags'), ('Colors', 'Couleurs'), ('Unlock Time', 'Unlock Time (Early / Mid / Late)')):
        todo = [w['Nom'] for w in weapons if w.get(col) == 'À compléter']
        if todo:
            report.append(f'! {label} à compléter dans data.csv : ' + ', '.join(todo))

    w_fields = w_fields or ['Nom', 'Tags', 'Colors', 'Evolution Item', 'Base Damage', 'Max Level', 'Unlock Time',
                            'Release', 'Source', 'Evolution', 'Description']
    c_fields = [f for f in (c_fields or []) if f not in ('Unlock Type', 'Weapon Tags')] or \
        ['Nom', 'Arme', 'Source', 'Secret', 'Max Health', 'Bonus', 'Release', 'Description', 'Unlock']
    if not args.dry_run:
        write_csv('data.csv', weapons, w_fields)
        write_csv('characters.csv', characters, c_fields + ['Unlock Type', 'Weapon Tags'])
        write_csv('evolutions.csv', evolutions, ['Nom', 'Type', 'Armes', 'Objets', 'Source', 'Base Tags', 'Release'])
    print('\n'.join(report) or 'Aucun changement.')
    print(f'{len(weapons)} armes, {len(characters)} personnages, {len(evolutions)} évolutions'
          + (' (rien écrit : --dry-run)' if args.dry_run else ''))


if __name__ == '__main__':
    main()
