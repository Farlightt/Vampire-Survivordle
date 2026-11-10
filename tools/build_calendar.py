#!/usr/bin/env python3
"""Génère daily.json : la réponse du défi du jour de chaque catégorie, pour chaque date.

    python3 tools/build_calendar.py            # complète le calendrier (30 jours passés -> 2 ans à venir)
    python3 tools/build_calendar.py --check    # vérifie que chaque réponse existe encore dans les CSV

Les dates déjà présentes dans daily.json ne sont jamais modifiées (tant que leur réponse
existe encore), si bien qu'une mise à jour des données ne change pas les défis prévus.
Les nouvelles dates sont tirées dans un paquet mélangé : une même réponse ne revient
pas avant d'avoir épuisé les autres. Les dates s'entendent à l'heure de Paris.
"""
import argparse
import csv
import datetime
import json
import os
import random
import unicodedata
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'daily.json')
PAST_DAYS, FUTURE_DAYS = 30, 730

# Doit rester identique aux « seed » de index.html (utilisés pour les dates d'avant le calendrier).
SEEDS = {'weapons': 'vsdle-w-', 'characters': 'vsdle-c-', 'evolutions': 'vsdle-e-', 'descriptions': 'vsdle-d-'}


def read(name):
    with open(os.path.join(ROOT, name), encoding='utf-8') as f:
        return list(csv.DictReader(f))


def normalize(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s or '') if not unicodedata.combining(c)).lower().strip()


def split_list(s):
    return [t.strip() for t in (s or '').split(',') if t.strip()]


def fnv1a(s):
    """Même hash que la fonction hash() de index.html (FNV-1a 32 bits sur les unités UTF-16)."""
    h = 2166136261
    data = s.encode('utf-16-le')
    for i in range(0, len(data), 2):
        h ^= data[i] | (data[i + 1] << 8)
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def easy_pools():
    """Mêmes sélections que les fonctions easy() / canBeSecret() de index.html, dans le même ordre."""
    weapons, chars, evos = read('data.csv'), read('characters.csv'), read('evolutions.csv')
    weapon_names = {w['Nom'] for w in weapons}
    desc = [{'Nom': w['Nom'], 'Description': w['Description'], 'Secret': ''} for w in weapons] + \
           [{'Nom': c['Nom'], 'Description': c['Description'], 'Secret': c['Secret']} for c in chars if c['Nom'] not in weapon_names]
    counts = {}
    for d in desc:
        counts[normalize(d['Description'])] = counts.get(normalize(d['Description']), 0) + 1

    def playable(d):
        text = normalize(d['Description'])
        return len(text) > 20 and counts[text] == 1 and \
            not any(len(w) > 3 and w in text for w in normalize(d['Nom']).split(' '))

    return {
        'weapons': [w['Nom'] for w in weapons if 'Choice' not in split_list(w['Tags'])],
        'characters': [c['Nom'] for c in chars if c['Secret'] == 'Non'],
        'evolutions': [e['Nom'] for e in evos if e['Type'] == 'Évolution' and e['Objets'] != 'Aucun'],
        'descriptions': [d['Nom'] for d in desc if playable(d) and d['Secret'] != 'Oui'],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()

    pools = easy_pools()
    today = datetime.datetime.now(ZoneInfo('Europe/Paris')).date()
    old = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}
    calendar = {}
    problems = []
    for cat, pool in pools.items():
        valid = set(pool)
        kept = {d: n for d, n in old.get(cat, {}).items() if n in valid}
        problems += [f'{cat} {d} : « {n} » n\'est plus une réponse possible' for d, n in old.get(cat, {}).items() if n not in valid]
        days = {}
        rng = random.Random('vsdle-calendar-' + cat)
        deck = []
        recent = []
        for i in range(-PAST_DAYS, FUTURE_DAYS + 1):
            date = (today + datetime.timedelta(days=i)).isoformat()
            if date in kept:
                name = kept[date]
            elif i <= 0:
                # jours déjà passés ou aujourd'hui : même tirage que l'ancienne méthode, pour ne rien changer
                name = pool[fnv1a(SEEDS[cat] + date) % len(pool)]
            else:
                if not deck:
                    deck = pool[:]
                    rng.shuffle(deck)
                # évite de reprendre une réponse vue dans la dernière moitié du paquet
                window = set(recent[-(len(pool) // 2):])
                pick = next((n for n in deck if n not in window), deck[0])
                deck.remove(pick)
                name = pick
            days[date] = name
            recent.append(name)
        calendar[cat] = days

    if args.check:
        print('\n'.join(problems) or 'Calendrier valide.')
        return
    json.dump(calendar, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    for p in problems:
        print('remplacé :', p)
    span = f'{(today - datetime.timedelta(days=PAST_DAYS)).isoformat()} → {(today + datetime.timedelta(days=FUTURE_DAYS)).isoformat()}'
    print(f'daily.json : {span}, ' + ', '.join(f'{c} {len(p)} réponses' for c, p in pools.items()))


if __name__ == '__main__':
    main()
