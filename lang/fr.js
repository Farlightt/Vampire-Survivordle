// Textes de l'interface en français. Les clés _one / _other gèrent le pluriel ; {x} est remplacé par une valeur.
window.VSDLE_LANG = window.VSDLE_LANG || {};
window.VSDLE_LANG.fr = {
    'meta.name': 'Français', 'meta.locale': 'fr-FR',
    'app.loading': 'Chargement…',
    'cat.weapons': 'Armes', 'cat.characters': 'Personnages', 'cat.evolutions': 'Évolutions', 'cat.descriptions': 'Descriptions',
    'mode.daily': 'Défi du jour', 'mode.free': 'Partie libre', 'mode.archive': 'Archives', 'archive.label': 'Défi du',

    'opt.title': 'Options', 'opt.hard': 'Mode difficile en partie libre', 'opt.hardDetail': '({full} au lieu de {easy})',
    'opt.limit': 'Essais limités ({n})', 'opt.cands': 'Afficher les réponses encore possibles',
    'opt.cb': 'Mode daltonien (bleu / orange / gris + symboles)', 'opt.sound': 'Effets sonores',
    'transfer.text': "Changer d'appareil : copie ton code de progression ici, colle-le sur l'autre appareil.",
    'transfer.copy': 'Copier mon code', 'transfer.import': 'Importer un code', 'transfer.placeholder': 'Colle ici un code de progression',

    'label.weapons': 'Arme du jour', 'label.characters': 'Personnage du jour', 'label.evolutions': 'Évolution du jour', 'label.descriptions': 'Description du jour',
    'placeholder.weapons': "Nom d'une arme…", 'placeholder.characters': "Nom d'un personnage…",
    'placeholder.evolutions': "Nom d'une évolution ou union…", 'placeholder.descriptions': "Nom d'une arme ou d'un personnage…",
    'empty.weapons': 'Propose une arme pour révéler les premiers indices.', 'empty.characters': 'Propose un personnage pour révéler les premiers indices.',
    'empty.evolutions': 'Propose une évolution pour révéler les premiers indices.', 'empty.descriptions': 'Propose une arme ou un personnage pour révéler les premiers indices.',
    'bonus.weapons': 'Bonus · arme du jour trouvée', 'bonus.characters': 'Bonus · personnage du jour trouvé', 'bonus.source': 'Source : {x}',

    'col.tags': 'Tags', 'col.colors': 'Couleurs', 'col.item': 'Objet évol.', 'col.damage': 'Dégâts', 'col.unlockTime': 'Déblocage',
    'col.source': 'Source', 'col.weapon': 'Arme', 'col.unlock': 'Déblocage', 'col.hp': 'PV', 'col.stats': 'Stats', 'col.release': 'Sortie',
    'col.baseWeapons': 'Armes de base', 'col.type': 'Type', 'col.weaponTags': 'Tags (arme)',

    'search.validate': 'Valider', 'status.over': 'Partie terminée',
    'btn.giveUp': 'Abandonner', 'btn.giveUpConfirm': "Confirmer l'abandon", 'btn.seeResult': 'Voir le résultat',
    'btn.share': 'Partager', 'btn.shareX': 'Partager sur X', 'btn.freePlay': 'Partie libre', 'btn.play': 'Jouer',

    'meta.free': 'Partie libre', 'meta.freeHard': 'Partie libre (difficile)', 'meta.archive': 'Archives',
    'meta.possible_one': '{n} réponse possible', 'meta.possible_other': '{n} réponses possibles',
    'guesses_one': '{n} essai', 'guesses_other': '{n} essais', 'hints_one': '{n} indice', 'hints_other': '{n} indices',

    'hint.button': "Révéler l'indice {i}/{n}", 'hint.wait_one': 'Indice {i}/{n} dans {k} essai', 'hint.wait_other': 'Indice {i}/{n} dans {k} essais',
    'hint.none': "Plus d'indice", 'hint.label': 'Indice {i}', 'hint.unused': 'Indice {i} (non utilisé)',
    'hint.firstLetter': 'Le nom commence par « {c} ».', 'hint.pattern': 'Forme du nom : {p}',
    'hint.evolvesInto': 'Évolue en {x}.', 'hint.noEvolution': "N'a pas d'évolution classique.", 'hint.noDescription': 'Pas de description.',
    'hint.unlock': 'Déblocage : {x}', 'hint.baseWeapon': 'Une des armes de base : {x}.', 'hint.startWeapon': 'Arme de départ : {x}.',

    'prompt.items_one': 'Objet requis', 'prompt.items_other': 'Objets requis', 'prompt.noItem': 'Aucun objet requis',
    'prompt.union': 'Obtenue en combinant plusieurs armes.', 'prompt.description': 'Description',

    'toast.unknown': 'Aucune réponse possible ne porte ce nom.', 'toast.already': 'Tu as déjà fait cette proposition.',
    'toast.copied': 'Résultat copié !', 'toast.copyManual': 'Copie le texte sélectionné.', 'toast.storage': 'Le stockage du navigateur est indisponible.',
    'toast.badCode': "Ce code de progression n'est pas valide.", 'toast.importConfirm': 'Clique encore pour remplacer la progression de cet appareil.',
    'toast.imported': 'Progression importée.', 'toast.codeCopied': 'Code copié !',

    'result.won': 'Trouvé en {tries} : {name}', 'result.indist': ' (indiscernable de {name})', 'result.lost': "C'était {name}",
    'result.outOfGuesses': "Plus d'essais. ",
    'end.win': 'Victoire !', 'end.lose': 'Perdu…', 'end.stats': 'Statistiques', 'end.foundIn': 'trouvé en {tries}', 'end.after': 'après {tries}',
    'stats.played': 'Jouées', 'stats.winPct': '% victoires', 'stats.streak': 'Série', 'stats.best': 'Record', 'stats.label': 'Statistiques · {x}',
    'countdown': 'Prochain défi du jour dans', 'countdown.note': 'minuit, heure de Paris',
    'cands.label': 'Réponses encore possibles : {n}', 'cands.more': 'et {n} autres…',
    'cell.manyStats': '{n} stats', 'cell.common': '({n} en commun)', 'cell.commonTags': 'Tags en commun : {x}',

    'share.lost': 'perdu', 'share.free': 'partie libre', 'share.hard': 'difficile', 'share.archive': 'archive',
    'share.weapons': 'Armes', 'share.characters': 'Personnages', 'share.evolutions': 'Évolutions', 'share.descriptions': 'Descriptions',
    'upload.text': 'Impossible de charger {file} automatiquement (page ouverte en local ?). Sélectionne le fichier :',

    'help.title': 'Comment jouer',
    'help.intro': "Trouve l'élément secret. Chaque proposition affiche son nom et une case par caractéristique.",
    'help.correct': 'Correct', 'help.partial': 'Partiel : un élément en commun, souligné (pour une arme de départ : un tag en commun).',
    'help.wrong': 'Faux', 'help.arrow': "La réponse est plus haute, plus récente ou se débloque plus tard (▼ : l'inverse).",
    'help.modes': "Évolutions : l'objet requis est donné. Descriptions : le texte du jeu est donné.",
    'help.hints': "Un indice se débloque après {steps} essais (compté 💡 dans le partage). Trouver l'arme du jour donne un bonus pour le personnage du jour, et inversement.",
    'help.daily': 'Défi du jour : le même pour tous, renouvelé à minuit (heure de Paris), sans les éléments obscurs. Archives : les 30 derniers jours. Options : mode difficile, essais limités, réponses possibles, mode daltonien, sons, transfert de progression.',
    'help.abbr': 'Stats : Rec Recovery · Arm Armor · MS Move Speed · Mgt Might · Spd Speed · Dur Duration · CD Cooldown · Amt Amount · Rev Revival · Mag Magnet · Lck Luck · Grw Growth · Grd Greed · Crs Curse · Rrl Reroll · Skp Skip · Ban Banish',
    'help.credit': 'Données : Vampire Survivors Wiki. Certaines années de sortie et couleurs sont estimées.',
    'aria.help': 'Comment jouer', 'aria.stats': 'Statistiques', 'aria.lang': 'Changer de langue', 'aria.sound': 'Activer ou couper le son', 'aria.close': 'Fermer',

    // Valeurs des données
    'val.Jeu de base': 'Jeu de base', 'val.Aucun': 'Aucun', 'val.Aucune': 'Aucune', 'val.Oui': 'Oui', 'val.Non': 'Non', 'val.N/A': '?',
    'val.Départ': 'Départ', 'val.Cercueil': 'Cercueil', 'val.Évolution': 'Évolution', "val.Niveau d'arme": "Niveau d'arme", 'val.Survie 20 min': 'Survie 20 min',
    'val.Ennemis vaincus': 'Ennemis vaincus', 'val.Exploit': 'Exploit', 'val.Boss': 'Boss', 'val.Énigme': 'Énigme',
    'val.Union': 'Union', 'val.Arme': 'Arme', 'val.Personnage': 'Personnage',
    'val.Early': 'Tôt', 'val.Mid': 'Milieu', 'val.Late': 'Tard',
    'val.Gray': 'Gris', 'val.Blue': 'Bleu', 'val.White': 'Blanc', 'val.Red': 'Rouge', 'val.Yellow': 'Jaune', 'val.Black': 'Noir',
    'val.Brown': 'Marron', 'val.Green': 'Vert', 'val.Purple': 'Violet', 'val.Orange': 'Orange', 'val.Pink': 'Rose',
};
