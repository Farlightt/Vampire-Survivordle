// English interface texts. _one / _other keys handle plurals; {x} is replaced by a value.
window.VSDLE_LANG = window.VSDLE_LANG || {};
window.VSDLE_LANG.en = {
    'meta.name': 'English', 'meta.locale': 'en-GB',
    'app.loading': 'Loading…',
    'cat.weapons': 'Weapons', 'cat.characters': 'Characters', 'cat.evolutions': 'Evolutions', 'cat.descriptions': 'Descriptions',
    'mode.daily': 'Daily', 'mode.free': 'Free play', 'mode.archive': 'Archive', 'archive.label': 'Challenge of',

    'opt.title': 'Options', 'opt.hard': 'Hard mode in free play', 'opt.hardDetail': '({full} instead of {easy})',
    'opt.limit': 'Limited guesses ({n})', 'opt.cands': 'Show remaining possible answers',
    'opt.cb': 'Colour-blind mode (blue / orange / grey + symbols)', 'opt.sound': 'Sound effects',
    'transfer.text': 'Switching device: copy your progress code here and paste it on the other device.',
    'transfer.copy': 'Copy my code', 'transfer.import': 'Import a code', 'transfer.placeholder': 'Paste a progress code here',

    'label.weapons': 'Daily weapon', 'label.characters': 'Daily character', 'label.evolutions': 'Daily evolution', 'label.descriptions': 'Daily description',
    'placeholder.weapons': 'Weapon name…', 'placeholder.characters': 'Character name…',
    'placeholder.evolutions': 'Evolution or union name…', 'placeholder.descriptions': 'Weapon or character name…',
    'empty.weapons': 'Guess a weapon to reveal the first clues.', 'empty.characters': 'Guess a character to reveal the first clues.',
    'empty.evolutions': 'Guess an evolution to reveal the first clues.', 'empty.descriptions': 'Guess a weapon or character to reveal the first clues.',
    'bonus.weapons': 'Bonus · daily weapon found', 'bonus.characters': 'Bonus · daily character found', 'bonus.source': 'Source: {x}',

    'col.tags': 'Tags', 'col.colors': 'Colours', 'col.item': 'Evo item', 'col.damage': 'Damage', 'col.unlockTime': 'Unlock',
    'col.source': 'Source', 'col.weapon': 'Weapon', 'col.unlock': 'Unlock', 'col.hp': 'HP', 'col.stats': 'Stats', 'col.release': 'Release',
    'col.baseWeapons': 'Base weapons', 'col.type': 'Type', 'col.weaponTags': 'Tags (weapon)',

    'search.validate': 'Guess', 'status.over': 'Game over',
    'btn.giveUp': 'Give up', 'btn.giveUpConfirm': 'Confirm give up', 'btn.seeResult': 'See result',
    'btn.share': 'Share', 'btn.shareX': 'Share on X', 'btn.freePlay': 'Free play', 'btn.play': 'Play',

    'meta.free': 'Free play', 'meta.freeHard': 'Free play (hard)', 'meta.archive': 'Archive',
    'meta.possible_one': '{n} possible answer', 'meta.possible_other': '{n} possible answers',
    'guesses_one': '{n} guess', 'guesses_other': '{n} guesses', 'hints_one': '{n} hint', 'hints_other': '{n} hints',

    'hint.button': 'Reveal hint {i}/{n}', 'hint.wait_one': 'Hint {i}/{n} in {k} guess', 'hint.wait_other': 'Hint {i}/{n} in {k} guesses',
    'hint.none': 'No more hints', 'hint.label': 'Hint {i}', 'hint.unused': 'Hint {i} (unused)',
    'hint.firstLetter': 'The name starts with “{c}”.', 'hint.pattern': 'Name shape: {p}',
    'hint.evolvesInto': 'Evolves into {x}.', 'hint.noEvolution': 'Has no regular evolution.', 'hint.noDescription': 'No description.',
    'hint.unlock': 'Unlock: {x}', 'hint.baseWeapon': 'One of the base weapons: {x}.', 'hint.startWeapon': 'Starting weapon: {x}.',

    'prompt.items_one': 'Required item', 'prompt.items_other': 'Required items', 'prompt.noItem': 'No item required',
    'prompt.union': 'Obtained by combining several weapons.', 'prompt.description': 'Description',

    'toast.unknown': 'No possible answer has that name.', 'toast.already': 'You already guessed that.',
    'toast.copied': 'Result copied!', 'toast.copyManual': 'Copy the selected text.', 'toast.storage': 'Browser storage is unavailable.',
    'toast.badCode': 'This progress code is not valid.', 'toast.importConfirm': "Click again to replace this device's progress.",
    'toast.imported': 'Progress imported.', 'toast.codeCopied': 'Code copied!',

    'result.won': 'Found in {tries}: {name}', 'result.indist': ' (indistinguishable from {name})', 'result.lost': 'It was {name}',
    'result.outOfGuesses': 'Out of guesses. ',
    'end.win': 'Victory!', 'end.lose': 'Defeat…', 'end.stats': 'Statistics', 'end.foundIn': 'found in {tries}', 'end.after': 'after {tries}',
    'stats.played': 'Played', 'stats.winPct': 'Win %', 'stats.streak': 'Streak', 'stats.best': 'Best', 'stats.label': 'Statistics · {x}',
    'countdown': 'Next daily challenge in', 'countdown.note': 'midnight, Paris time',
    'cands.label': 'Remaining possible answers: {n}', 'cands.more': 'and {n} more…',
    'cell.manyStats': '{n} stats', 'cell.common': '({n} shared)', 'cell.commonTags': 'Shared tags: {x}',

    'share.lost': 'lost', 'share.free': 'free play', 'share.hard': 'hard', 'share.archive': 'archive',
    'share.weapons': 'Weapons', 'share.characters': 'Characters', 'share.evolutions': 'Evolutions', 'share.descriptions': 'Descriptions',
    'upload.text': 'Could not load {file} automatically (page opened locally?). Select the file:',

    'help.title': 'How to play',
    'help.intro': 'Find the secret entry. Each guess shows its name and one tile per attribute.',
    'help.correct': 'Correct', 'help.partial': 'Partial: one element in common, underlined (for a starting weapon: one tag in common).',
    'help.wrong': 'Wrong', 'help.arrow': 'The answer is higher, more recent or unlocked later (▼: the opposite).',
    'help.modes': 'Evolutions: the required item is given. Descriptions: the in-game text is given.',
    'help.hints': 'A hint unlocks after {steps} guesses (counted as 💡 when sharing). Finding the daily weapon gives a bonus for the daily character, and vice versa.',
    'help.daily': 'Daily: the same for everyone, reset at midnight (Paris time), without obscure entries. Archive: the last 30 days. Options: hard mode, limited guesses, possible answers, colour-blind mode, sounds, progress transfer.',
    'help.abbr': 'Stats: Rec Recovery · Arm Armor · MS Move Speed · Mgt Might · Spd Speed · Dur Duration · CD Cooldown · Amt Amount · Rev Revival · Mag Magnet · Lck Luck · Grw Growth · Grd Greed · Crs Curse · Rrl Reroll · Skp Skip · Ban Banish',
    'help.credit': 'Data: Vampire Survivors Wiki. Some release years and colours are estimates.',
    'aria.help': 'How to play', 'aria.stats': 'Statistics', 'aria.lang': 'Change language', 'aria.sound': 'Toggle sound', 'aria.close': 'Close',

    'val.Jeu de base': 'Base game', 'val.Aucun': 'None', 'val.Aucune': 'None', 'val.Oui': 'Yes', 'val.Non': 'No', 'val.N/A': '?',
    'val.Départ': 'Start', 'val.Cercueil': 'Coffin', 'val.Évolution': 'Evolution', "val.Niveau d'arme": 'Weapon level', 'val.Survie 20 min': 'Survive 20 min',
    'val.Ennemis vaincus': 'Enemies defeated', 'val.Exploit': 'Feat', 'val.Boss': 'Boss', 'val.Énigme': 'Riddle',
    'val.Union': 'Union', 'val.Arme': 'Weapon', 'val.Personnage': 'Character',
    'val.Early': 'Early', 'val.Mid': 'Mid', 'val.Late': 'Late',
    'val.Gray': 'Grey', 'val.Blue': 'Blue', 'val.White': 'White', 'val.Red': 'Red', 'val.Yellow': 'Yellow', 'val.Black': 'Black',
    'val.Brown': 'Brown', 'val.Green': 'Green', 'val.Purple': 'Purple', 'val.Orange': 'Orange', 'val.Pink': 'Pink',
};
