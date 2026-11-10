// Textos de la interfaz en español. Las claves _one / _other gestionan el plural; {x} se sustituye por un valor.
window.VSDLE_LANG = window.VSDLE_LANG || {};
window.VSDLE_LANG.es = {
    'meta.name': 'Español', 'meta.locale': 'es-ES',
    'app.loading': 'Cargando…',
    'cat.weapons': 'Armas', 'cat.characters': 'Personajes', 'cat.evolutions': 'Evoluciones', 'cat.descriptions': 'Descripciones',
    'mode.daily': 'Reto diario', 'mode.free': 'Partida libre', 'mode.archive': 'Archivo', 'archive.label': 'Reto del',

    'opt.title': 'Opciones', 'opt.hard': 'Modo difícil en partida libre', 'opt.hardDetail': '({full} en lugar de {easy})',
    'opt.limit': 'Intentos limitados ({n})', 'opt.cands': 'Mostrar las respuestas aún posibles',
    'opt.cb': 'Modo daltónico (azul / naranja / gris + símbolos)', 'opt.sound': 'Efectos de sonido',
    'transfer.text': 'Cambiar de dispositivo: copia aquí tu código de progreso y pégalo en el otro dispositivo.',
    'transfer.copy': 'Copiar mi código', 'transfer.import': 'Importar un código', 'transfer.placeholder': 'Pega aquí un código de progreso',

    'label.weapons': 'Arma del día', 'label.characters': 'Personaje del día', 'label.evolutions': 'Evolución del día', 'label.descriptions': 'Descripción del día',
    'placeholder.weapons': 'Nombre de un arma…', 'placeholder.characters': 'Nombre de un personaje…',
    'placeholder.evolutions': 'Nombre de una evolución o unión…', 'placeholder.descriptions': 'Nombre de un arma o personaje…',
    'empty.weapons': 'Propón un arma para revelar las primeras pistas.', 'empty.characters': 'Propón un personaje para revelar las primeras pistas.',
    'empty.evolutions': 'Propón una evolución para revelar las primeras pistas.', 'empty.descriptions': 'Propón un arma o un personaje para revelar las primeras pistas.',
    'bonus.weapons': 'Bonus · arma del día encontrada', 'bonus.characters': 'Bonus · personaje del día encontrado', 'bonus.source': 'Origen: {x}',

    'col.tags': 'Tags', 'col.colors': 'Colores', 'col.item': 'Objeto evol.', 'col.damage': 'Daño', 'col.unlockTime': 'Desbloqueo',
    'col.source': 'Origen', 'col.weapon': 'Arma', 'col.unlock': 'Desbloqueo', 'col.hp': 'PV', 'col.stats': 'Stats', 'col.release': 'Salida',
    'col.baseWeapons': 'Armas base', 'col.type': 'Tipo', 'col.weaponTags': 'Tags (arma)',

    'search.validate': 'Validar', 'status.over': 'Partida terminada',
    'btn.giveUp': 'Rendirse', 'btn.giveUpConfirm': 'Confirmar rendición', 'btn.seeResult': 'Ver resultado',
    'btn.share': 'Compartir', 'btn.shareX': 'Compartir en X', 'btn.freePlay': 'Partida libre', 'btn.play': 'Jugar',

    'meta.free': 'Partida libre', 'meta.freeHard': 'Partida libre (difícil)', 'meta.archive': 'Archivo',
    'meta.possible_one': '{n} respuesta posible', 'meta.possible_other': '{n} respuestas posibles',
    'guesses_one': '{n} intento', 'guesses_other': '{n} intentos', 'hints_one': '{n} pista', 'hints_other': '{n} pistas',

    'hint.button': 'Revelar la pista {i}/{n}', 'hint.wait_one': 'Pista {i}/{n} en {k} intento', 'hint.wait_other': 'Pista {i}/{n} en {k} intentos',
    'hint.none': 'No hay más pistas', 'hint.label': 'Pista {i}', 'hint.unused': 'Pista {i} (no usada)',
    'hint.firstLetter': 'El nombre empieza por «{c}».', 'hint.pattern': 'Forma del nombre: {p}',
    'hint.evolvesInto': 'Evoluciona en {x}.', 'hint.noEvolution': 'No tiene evolución clásica.', 'hint.noDescription': 'Sin descripción.',
    'hint.unlock': 'Desbloqueo: {x}', 'hint.baseWeapon': 'Una de las armas base: {x}.', 'hint.startWeapon': 'Arma inicial: {x}.',

    'prompt.items_one': 'Objeto necesario', 'prompt.items_other': 'Objetos necesarios', 'prompt.noItem': 'No necesita objeto',
    'prompt.union': 'Se obtiene combinando varias armas.', 'prompt.description': 'Descripción',

    'toast.unknown': 'Ninguna respuesta posible tiene ese nombre.', 'toast.already': 'Ya has propuesto eso.',
    'toast.copied': '¡Resultado copiado!', 'toast.copyManual': 'Copia el texto seleccionado.', 'toast.storage': 'El almacenamiento del navegador no está disponible.',
    'toast.badCode': 'Este código de progreso no es válido.', 'toast.importConfirm': 'Haz clic otra vez para reemplazar el progreso de este dispositivo.',
    'toast.imported': 'Progreso importado.', 'toast.codeCopied': '¡Código copiado!',

    'result.won': 'Encontrado en {tries}: {name}', 'result.indist': ' (indistinguible de {name})', 'result.lost': 'Era {name}',
    'result.outOfGuesses': 'Sin intentos. ',
    'end.win': '¡Victoria!', 'end.lose': 'Derrota…', 'end.stats': 'Estadísticas', 'end.foundIn': 'encontrado en {tries}', 'end.after': 'tras {tries}',
    'stats.played': 'Jugadas', 'stats.winPct': '% victorias', 'stats.streak': 'Racha', 'stats.best': 'Récord', 'stats.label': 'Estadísticas · {x}',
    'countdown': 'Próximo reto diario en', 'countdown.note': 'medianoche, hora de París',
    'cands.label': 'Respuestas aún posibles: {n}', 'cands.more': 'y {n} más…',
    'cell.manyStats': '{n} stats', 'cell.common': '({n} en común)', 'cell.commonTags': 'Tags en común: {x}',

    'share.lost': 'perdido', 'share.free': 'partida libre', 'share.hard': 'difícil', 'share.archive': 'archivo',
    'share.weapons': 'Armas', 'share.characters': 'Personajes', 'share.evolutions': 'Evoluciones', 'share.descriptions': 'Descripciones',
    'upload.text': 'No se pudo cargar {file} automáticamente (¿página abierta en local?). Selecciona el archivo:',

    'help.title': 'Cómo jugar',
    'help.intro': 'Encuentra el elemento secreto. Cada intento muestra su nombre y una casilla por característica.',
    'help.correct': 'Correcto', 'help.partial': 'Parcial: un elemento en común, subrayado (para un arma inicial: un tag en común).',
    'help.wrong': 'Incorrecto', 'help.arrow': 'La respuesta es más alta, más reciente o se desbloquea más tarde (▼: lo contrario).',
    'help.modes': 'Evoluciones: se da el objeto necesario. Descripciones: se da el texto del juego.',
    'help.hints': 'Se desbloquea una pista tras {steps} intentos (cuenta como 💡 al compartir). Encontrar el arma del día da un bonus para el personaje del día, y viceversa.',
    'help.daily': 'Reto diario: el mismo para todos, se renueva a medianoche (hora de París), sin elementos oscuros. Archivo: los últimos 30 días. Opciones: modo difícil, intentos limitados, respuestas posibles, modo daltónico, sonidos, transferencia de progreso.',
    'help.abbr': 'Stats: Rec Recovery · Arm Armor · MS Move Speed · Mgt Might · Spd Speed · Dur Duration · CD Cooldown · Amt Amount · Rev Revival · Mag Magnet · Lck Luck · Grw Growth · Grd Greed · Crs Curse · Rrl Reroll · Skp Skip · Ban Banish',
    'help.credit': 'Datos: Vampire Survivors Wiki. Algunos años de salida y colores son estimaciones.',
    'aria.help': 'Cómo jugar', 'aria.stats': 'Estadísticas', 'aria.lang': 'Cambiar de idioma', 'aria.sound': 'Activar o silenciar el sonido', 'aria.close': 'Cerrar',

    'val.Jeu de base': 'Juego base', 'val.Aucun': 'Ninguno', 'val.Aucune': 'Ninguna', 'val.Oui': 'Sí', 'val.Non': 'No', 'val.N/A': '?',
    'val.Départ': 'Inicio', 'val.Cercueil': 'Ataúd', 'val.Évolution': 'Evolución', "val.Niveau d'arme": 'Nivel de arma', 'val.Survie 20 min': 'Sobrevivir 20 min',
    'val.Ennemis vaincus': 'Enemigos derrotados', 'val.Exploit': 'Hazaña', 'val.Boss': 'Jefe', 'val.Énigme': 'Enigma',
    'val.Union': 'Unión', 'val.Arme': 'Arma', 'val.Personnage': 'Personaje',
    'val.Early': 'Pronto', 'val.Mid': 'Medio', 'val.Late': 'Tarde',
    'val.Gray': 'Gris', 'val.Blue': 'Azul', 'val.White': 'Blanco', 'val.Red': 'Rojo', 'val.Yellow': 'Amarillo', 'val.Black': 'Negro',
    'val.Brown': 'Marrón', 'val.Green': 'Verde', 'val.Purple': 'Morado', 'val.Orange': 'Naranja', 'val.Pink': 'Rosa',
};
