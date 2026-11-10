"""Tests de tools/update_data.py sur des extraits réels du wiki (sans réseau).

    python3 tools/test_update_data.py
"""
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import update_data as ud  # noqa: E402

BIG_TROUSER = """{{Confuse|Big Troubler}}
{{Infobox Character
|name = Big Trouser
|dlc =
|description = Gains +1% Greed every level. Gold Fever lasts longer.
|release = 4 August 2022
|weapon = Candybox
|unlock = Master all 16 [[Stage item|accessories]] in [[Moongolow]].
|secret = Yes
|maxhealth = 100
|recovery = -
|movespeed = +30%
|might = -
|greed = +20%
}}
'''Big Trouser''' is a [[secret]] playable [[character]]."""

BETA_CHAR = """{{Infobox Character
|name = Newcomer
|release =
|weapon = Magic Wand
|unlock = Survive 20 minutes in [[Biggus Discus]].
|secret = No
|maxhealth = 120
|armor = +1
}}
==Update history==
{{UH|
* {{UL|type=beta|update=Public-beta v1.17.108|date=16 October 2026}}
** Released in beta version.
}}"""

MAGIC_WAND = """{{Infobox Weapon
|id = MAGIC_MISSILE
|caption = Fires at the nearest enemy.
|type = Normal
|release = 27 October 2021
|evolution = Holy Wand
|evolution-item = Empty Tome
|damage = 10
}}
'''Magic Wand''' is a [[weapon]]."""

HOLY_WAND = """{{Infobox Weapon
|id = HOLY_MISSILE
|caption = Evolution of the Magic Wand. Fires with no delay.
|type = Evolution
|requires1 = Magic Wand
|requires2 = Empty Tome
|union=Spirit of Light
|damage = 30
}}"""

BONE = """{{Infobox Weapon
|caption = Throws a bouncing projectile.
|type = Normal
|evolution = Anima of Mortaccio
|evolution-item = Chaos Malachite
|damage = 5
}}
==Update history==
{{UH|
* {{UL|update=Patch 1.3.0|date=9 February 2023}}
** Added evolution by getting [[Chaos Malachite]].

* {{UL|update=There exist tales that don't exist.|date=27 October 2021}}
** Added to game.
}}"""

PAKO = """{{Infobox Weapon
|caption = May retaliate when losing health. Ignores Duration.
|type = Normal
|evolution = Mazo Familiar
|evolution-item = Hollow Heart
|damage = 20
}}
The '''Pako Battiliar''' is a [[Weapons|weapon]] that was introduced in [[Patch 1.9.0]]."""

NEW_GUN = """{{Infobox Weapon
|caption = Shoots [[Armor (item)|armored]] bullets.
|type = Normal
|dlc = og
|evolution = Big Gun
|evolution-item = Armor (item)
|evolution-item2 = Bracer
|damage = 12
|max-level = 8
}}
Introduced in [[Patch 1.3.0]]."""

RAW = {
    'characters': {'Big Trouser': BIG_TROUSER, 'Newcomer': BETA_CHAR},
    'weapons': {'Magic Wand': MAGIC_WAND, 'Holy Wand': HOLY_WAND, 'Bone': BONE,
                'Pako Battiliar': PAKO, 'New Gun': NEW_GUN},
    'patches': {'Patch 1.9.0': '{{News|date=22 February 2024|version=1.9.0}}',
                'Patch 1.3.0': '{{News|date=9 February 2023|version=1.3.0|source=steam}}'},
}


class ParsingTests(unittest.TestCase):
    def test_template_nested(self):
        box = ud.template(BIG_TROUSER, 'Infobox Character')
        self.assertEqual(box['unlock'], 'Master all 16 [[Stage item|accessories]] in [[Moongolow]].')
        self.assertEqual(ud.clean(box['unlock']), 'Master all 16 accessories in Moongolow.')

    def test_years(self):
        self.assertEqual(ud.added_year(BONE), 2021)
        self.assertEqual(ud.intro_patch(PAKO), 'Patch 1.9.0')
        self.assertEqual(ud.patch_year(RAW['patches']['Patch 1.9.0']), 2024)

    def test_characters(self):
        chars = ud.wiki_characters(RAW)
        bt = chars['Big Trouser']
        self.assertEqual((bt['Arme'], bt['Source'], bt['Secret'], bt['Max Health'], bt['Bonus'], bt['Release']),
                         ('Candybox', 'Jeu de base', 'Oui', '100', 'Move Speed, Greed', '2022-08-04'))
        self.assertEqual(chars['Newcomer']['Release'], '2026-10-16')  # personnage en bêta

    def test_weapons_and_evolutions(self):
        weapons = ud.wiki_weapons(RAW, {})
        self.assertEqual(weapons['Bone']['Release'], '2021')
        self.assertEqual(weapons['Pako Battiliar']['Release'], '2024')
        self.assertEqual(weapons['New Gun']['Evolution Item'], 'Armor, Bracer')
        self.assertEqual(weapons['New Gun']['Source'], 'Operation Guns')
        self.assertEqual(weapons['New Gun']['Max Level'], '8')
        self.assertNotIn('Holy Wand', weapons)
        evos = ud.wiki_evolutions(RAW)
        self.assertEqual(evos, [{'Nom': 'Holy Wand', 'Type': 'Évolution', 'Armes': 'Magic Wand',
                                 'Objets': 'Empty Tome', 'Source': 'Jeu de base'}])

    def test_unlock_type(self):
        self.assertEqual(ud.unlock_type('Find and open the coffin in Mad Forest.'), 'Cercueil')
        self.assertEqual(ud.unlock_type('Evolve the Silver Wind.'), 'Évolution')
        self.assertEqual(ud.unlock_type('Defeat a total of 3000 Lion Heads.'), 'Ennemis vaincus')
        self.assertEqual(ud.unlock_type('Make it feel at home.'), 'Énigme')


class EndToEndTest(unittest.TestCase):
    """Lance le script complet sur une copie du dépôt, avec le cache ci-dessus."""

    def test_update_keeps_manual_fields(self):
        tmp = tempfile.mkdtemp()
        try:
            root = os.path.dirname(HERE)
            for f in ('data.csv', 'characters.csv', 'evolutions.csv'):
                shutil.copy(os.path.join(root, f), tmp)
            os.makedirs(os.path.join(tmp, 'tools'))
            shutil.copy(os.path.join(HERE, 'update_data.py'), os.path.join(tmp, 'tools'))
            json.dump(RAW, open(os.path.join(tmp, 'tools', 'wiki_cache.json'), 'w', encoding='utf-8'))
            out = subprocess.run([sys.executable, 'tools/update_data.py', '--cache'], cwd=tmp,
                                 capture_output=True, text=True, check=True).stdout
            self.assertIn('+ arme ajouté : New Gun', out)
            self.assertIn('+ personnage ajouté : Newcomer', out)
            self.assertIn('Tags à compléter dans data.csv : New Gun', out)
            self.assertIn('Couleurs à compléter dans data.csv : New Gun', out)
            weapons = {r['Nom']: r for r in csv.DictReader(open(os.path.join(tmp, 'data.csv'), encoding='utf-8'))}
            self.assertEqual(weapons['Bone']['Tags'], 'Bouncing, Projectile')  # tags rédigés conservés
            self.assertEqual(weapons['New Gun']['Tags'], 'À compléter')
            chars = {r['Nom']: r for r in csv.DictReader(open(os.path.join(tmp, 'characters.csv'), encoding='utf-8'))}
            self.assertEqual(chars['Newcomer']['Unlock Type'], 'Survie 20 min')
            self.assertEqual(chars['Newcomer']['Weapon Tags'], 'Homing, Projectile')
            self.assertEqual(len(chars), 229)  # anciens personnages conservés + 1
        finally:
            shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main(verbosity=2)
