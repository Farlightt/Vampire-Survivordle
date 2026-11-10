"""Tests de tools/fetch_icons.py sans réseau (API et téléchargements simulés).

    python3 tools/test_fetch_icons.py
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fetch_icons as fi  # noqa: E402

PNG = bytes.fromhex('89504e470d0a1a0a0000000d4948445200000001000000010806000000'
                    '1f15c4890000000d49444154789c6360f8cfc0f01f0005fe02fea3ef6c7f0000000049454e44ae426082')


class FetchIconsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        root = os.path.dirname(HERE)
        for f in ('data.csv', 'characters.csv', 'evolutions.csv'):
            shutil.copy(os.path.join(root, f), self.tmp)
        os.makedirs(os.path.join(self.tmp, 'images', 'weapons'))
        open(os.path.join(self.tmp, 'images', 'weapons', 'whip.webp'), 'wb').close()
        self.saved = (fi.ROOT, fi.IMAGES, fi.api, fi.download)
        fi.ROOT, fi.IMAGES = self.tmp, os.path.join(self.tmp, 'images')
        self.asked = []

        def fake_api(**params):   # le wiki ne connaît que deux fichiers
            titles = params['titles'].split('|')
            self.asked += titles
            known = {'File:Icon-Axe.png', 'File:Select-Big Trouser.png'}
            return {'query': {'pages': [{'title': t, **({'imageinfo': [{'url': 'https://x/' + t}]} if t in known else {'missing': True})} for t in titles]}}
        fi.api = fake_api
        fi.download = lambda url: PNG

    def tearDown(self):
        fi.ROOT, fi.IMAGES, fi.api, fi.download = self.saved
        shutil.rmtree(self.tmp)

    def test_slug_matches_page(self):
        self.assertEqual(fi.slug("Guardian's Targe"), 'guardian_s_targe')
        self.assertEqual(fi.slug('Carréllo'), 'carrello')

    def test_missing_skips_existing(self):
        todo = fi.missing()
        self.assertNotIn('Whip', todo['weapons'])
        self.assertIn('Axe', todo['weapons'])
        self.assertIn('Big Trouser', todo['characters'])
        self.assertIn('Spinach', todo['items'])

    def test_download_and_index(self):
        sys.argv = ['fetch_icons.py']
        fi.main()
        index = json.load(open(os.path.join(self.tmp, 'images', 'icons.json')))
        self.assertIn('axe', index['weapons'])
        self.assertIn('whip', index['weapons'])
        self.assertIn('big_trouser', index['characters'])
        self.assertIn('File:Sprite-Spinach.png', self.asked)   # objets : préfixe Sprite- d'abord
        self.assertNotIn('File:Icon-Whip.png', self.asked)      # icône déjà présente : pas redemandée


if __name__ == '__main__':
    unittest.main(verbosity=2)
