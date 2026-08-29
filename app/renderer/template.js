const DATA = JSON.parse(document.getElementById('dayData').textContent);
const LANG_NAMES = { la: "Latin / Latina", es: "Español" };
const MENU_LANG_NAMES = { la: "Latina", es: "Español", en: "English" };

/* ============================================================
   UI STRINGS - the app's own interface chrome (Settings panel,
   hour-selection screen, drawers, modals), independent of which
   language the liturgical TEXT itself is shown in. Driven by
   settings.menuLang, not by leftLang/rightLang.
   ============================================================ */
const UI = {
  en: {
    comingSoon: '(coming soon)', prayNow: 'Pray Now',
    betaLabel: 'Beta Tester Mode',
    tIntentions: 'Intentions', tDiary: 'Prayer Diary', tSettings: 'Settings', tBack: 'Choose another hour',
    tSmaller: 'Smaller text', tLarger: 'Larger text', tDebug: 'Beta debug menu',
    settingsTitle: 'Settings', backBtn: 'Back',
    secPresets: 'Preset Themes', secColorSync: 'Liturgical Color Sync', secTypography: 'Typography',
    secColors: 'Colors (Custom)', secLayout: 'Layout & Reading Mode', secBackground: 'Background', secLogo: 'Logo',
    syncLabel: "Tint accents to today's liturgical color",
    syncHint: "Updates automatically with the season and any saint's day (White, Green, Violet, Red, Rose). Overrides only the accent color, not your background/text colors.",
    fontMainLabel: 'Main Text font', fontRubricLabel: 'Rubrics font (headings/labels)',
    secondaryFontToggle: 'Use a separate font for the secondary language',
    secondaryFontHint: 'When off, the whole page uses one font. When on, the Main font applies to whichever language is set as Main, and this font applies to the other side.',
    fontLatinLabel: 'Secondary language font',
    fsMain: 'Main text size', fsRubric: 'Rubric size', fsLatin: 'Secondary language size',
    lineHeightLabel: 'Line height', paraSpacingLabel: 'Paragraph spacing',
    colorsHint: 'Editing any color below switches you to the Custom preset.',
    cBg: 'Background', cFg: 'Font color', cAccent: 'Accent / rubric color', cPanel: 'Panel background',
    readingModeLabel: 'Reading view', optScroll: 'Continuous scroll', optPaged: 'Paged / ribbon view',
    bilingualLabel: 'Bilingual display', optSideBySide: 'Side by side', optLatinOnly: 'Latin only', optVernOnly: 'Vernacular only',
    showDividersLabel: 'Show section dividers', showSymbolsLabel: 'Show liturgical symbols († ★)',
    dropCapLabel: 'Drop caps', optDcNone: 'None', optDcClean: 'Simple clean', optDcRoman: 'Classic Roman', optDcIllum: 'Medieval illuminated',
    sunsetLabel: 'Sunset-aware Vespers recommendation',
    sunsetHint: 'Uses your device location (asked only when enabled) to light up the Vespers "Pray Now" halo around actual local sunset instead of a fixed clock time.',
    menuLangLabel: 'Menu language', bgNoImage: 'No image set', bgUploadLabel: 'Upload background image',
    bgClearLabel: 'Remove background image', bgClearBtn: 'Clear', bgOverlayLabel: 'Overlay opacity (readability)',
    bgBlurLabel: 'Background blur', secTextures: 'Texture Presets', showLogoLabel: 'Show "Pro Omnibus Gentibus" logo',
    secPaterNoster: 'Our Father', paterNosterBreadLabel: '"Daily bread" wording',
    optCotidianum: 'Panem cotidianum (daily bread)', optSupersubstantialem: 'Panem supersubstantialem (supersubstantial bread)',
    paterNosterBreadHint: 'Two traditional Latin renderings of the Greek epiousios (Luke’s vs. Matthew’s Vulgate text) - applies to Latin, Spanish, and English alike.',
    secGroupAesthetics: 'Aesthetics', secGroupLiturgical: 'Liturgical',
    secPrayerElements: 'Liturgical',
    gloriaPatriLabel: 'Gloria Patri after each psalm and canticle',
    gloriaPatriHint: 'Adds the Glory Be after every psalm and canticle, before its antiphon is repeated.',
    sacredSilenceLabel: 'Sacred silence after the reading',
    sacredSilenceHint: 'Marks a pause for silent reflection after the short reading (Lectio Brevis), as recommended by the General Instruction.',
    marianLabel: 'Marian antiphon at the end of Compline',
    marianHint: 'A closing antiphon to Our Lady, prayed after Night Prayer’s own dismissal.',
    marianChoiceLabel: 'Which antiphon', marianNone: 'None',
    resetBtn: 'Reset all settings to default', resetConfirm: 'Reset all appearance settings to the default Parchment theme?',
    intentionsTitle: 'Personal Intentions',
    intentionsHint: "Checked intentions are added to today's Preces, just before the Pater Noster.",
    intentionsEmpty: 'No intentions yet - add one below.',
    intentionsPlaceholder: 'e.g. For the Holy Father, the Pope', addBtn: 'Add',
    intentionsMasterToggle: 'Include intentions in the Preces',
    diaryTitle: 'Prayer Diary', streakLabel: (n) => `Day${n === 1 ? '' : 's'} in a row`,
    markPrayed: 'Mark today as prayed', prayedDone: '✓ Prayed today',
    diaryNoteLabel: "Note on today's Lectio Brevis", diaryNotePlaceholder: "A thought on today's reading...",
    bookmarksHeading: 'Bookmarked Psalms', bookmarksEmpty: 'No bookmarks yet.',
    firstVisitTitle: 'Under Development', firstVisitDismiss: 'I understand, continue',
    firstVisitBody: 'This application is under active, deep development. Content is still being sourced and verified day by day - you may encounter missing text, mismatched translations, or other errors. Please pray with patience, and treat anything you see here as provisional.',
    debugTitle: 'Beta Debug Menu',
    debugHint: 'Raw settings state, editable directly - for bug hunting only. Invalid JSON is ignored.',
    debugApply: 'Apply JSON', debugClearStorage: 'Clear all local storage', debugReloadData: 'Force day-data refetch',
    debugPhoneSim: 'Open phone simulator (375×812)',
    tHymnal: 'Hymnal',
    infoTitle: 'About This Project', infoClose: 'Close',
    infoBody: 'Pro Omnibus Gentibus is free, always will be, and is fully open source. Read more below.',
    infoLinkMaking: 'How It Was Made', infoLinkBeta: 'Beta Guide', infoLinkFuture: 'Future Plans',
    hymnalTitle: 'Hymnal', hymnalSearchPlaceholder: 'Search hymns by title or first line…',
    hymnalFilterHour: 'Hour', hymnalFilterAllHours: 'All hours',
    hymnalFilterLang: 'Languages', hymnalFilterAllLangs: 'All', hymnalFilterMultiLang: 'Multi-language',
    hymnalFilterSingleLang: 'Single-language',
    hymnalLangFilterHint: '"Multi-language" means the hymn has more than one genuinely sung version. Most hymns here are single-language (e.g. sung in Latin) with a translation provided only so you can follow along.',
    hymnalAlsoSungLabel: 'Also a genuine sung version in this language (not just a translation for reading along)',
    hymnalEmpty: 'No hymns match.', hymnalCount: (n) => `${n} hymn${n === 1 ? '' : 's'}`,
    hymnalOfficialBadge: 'Official', hymnalUserBadge: 'Mine',
    hymnalViewLyrics: 'View lyrics', hymnalHideLyrics: 'Hide lyrics',
    hymnalAddBtn: '+ Add a hymn', hymnalAddFormTitle: 'Add a hymn',
    hymnalFieldTitle: 'Title', hymnalFieldHours: 'Used at these hours',
    hymnalFieldOriginalLang: 'Original language (the one actually sung)',
    hymnalFieldLyricsFor: (lang) => `Lyrics (${lang})`,
    hymnalLyricsHint: 'One line per line. Leave a blank line to mark a stanza break. Fill in whichever languages you have — you can leave others empty.',
    hymnalSaveBtn: 'Save hymn', hymnalCancelBtn: 'Cancel',
    hymnalDeleteBtn: 'Delete', hymnalDeleteConfirm: 'Delete this hymn? This can\'t be undone.',
    hymnalLocalNotice: 'Hymns you add are saved on this device only (there\'s no shared server for this app) — they won\'t appear for other people or other devices.',
    hymnalTitleRequired: 'Please enter a title.',
    hymnalHoursRequired: 'Please pick at least one hour.',
    hymnalLyricsRequired: 'Please enter lyrics in at least one language.',
    hymnRecommendedTag: 'Recommended for today',
  },
  es: {
    comingSoon: '(próximamente)', prayNow: 'Reza ahora',
    betaLabel: 'Modo de prueba beta',
    tIntentions: 'Intenciones', tDiary: 'Diario de oración', tSettings: 'Configuración', tBack: 'Elegir otra hora',
    tSmaller: 'Texto más pequeño', tLarger: 'Texto más grande', tDebug: 'Menú de depuración beta',
    settingsTitle: 'Configuración', backBtn: 'Volver',
    secPresets: 'Temas predefinidos', secColorSync: 'Sincronización del color litúrgico', secTypography: 'Tipografía',
    secColors: 'Colores (personalizado)', secLayout: 'Diseño y modo de lectura', secBackground: 'Fondo', secLogo: 'Logotipo',
    syncLabel: 'Teñir los acentos con el color litúrgico de hoy',
    syncHint: 'Se actualiza automáticamente según el tiempo litúrgico y cualquier fiesta (Blanco, Verde, Morado, Rojo, Rosa). Solo cambia el color de acento, no el fondo ni el texto.',
    fontMainLabel: 'Fuente del texto principal', fontRubricLabel: 'Fuente de las rúbricas (títulos/etiquetas)',
    secondaryFontToggle: 'Usar una fuente distinta para el idioma secundario',
    secondaryFontHint: 'Si está desactivado, toda la página usa una sola fuente. Si está activado, la fuente principal se aplica al idioma marcado como Principal, y esta fuente al otro lado.',
    fontLatinLabel: 'Fuente del idioma secundario',
    fsMain: 'Tamaño del texto principal', fsRubric: 'Tamaño de las rúbricas', fsLatin: 'Tamaño del idioma secundario',
    lineHeightLabel: 'Interlineado', paraSpacingLabel: 'Espaciado de párrafos',
    colorsHint: 'Cambiar cualquier color de abajo te lleva al tema personalizado.',
    cBg: 'Fondo', cFg: 'Color del texto', cAccent: 'Color de acento / rúbricas', cPanel: 'Fondo de los paneles',
    readingModeLabel: 'Modo de lectura', optScroll: 'Desplazamiento continuo', optPaged: 'Vista paginada / cinta',
    bilingualLabel: 'Visualización bilingüe', optSideBySide: 'Uno junto al otro', optLatinOnly: 'Solo latín', optVernOnly: 'Solo vernáculo',
    showDividersLabel: 'Mostrar separadores de sección', showSymbolsLabel: 'Mostrar símbolos litúrgicos († ★)',
    dropCapLabel: 'Capitulares', optDcNone: 'Ninguna', optDcClean: 'Sencilla', optDcRoman: 'Romana clásica', optDcIllum: 'Iluminada medieval',
    sunsetLabel: 'Recomendación de Vísperas según el atardecer',
    sunsetHint: 'Usa la ubicación de tu dispositivo (solo se solicita si activas esto) para encender el halo de "Reza ahora" de Vísperas cerca del atardecer real en lugar de una hora fija.',
    menuLangLabel: 'Idioma del menú', bgNoImage: 'Sin imagen', bgUploadLabel: 'Subir imagen de fondo',
    bgClearLabel: 'Quitar imagen de fondo', bgClearBtn: 'Quitar', bgOverlayLabel: 'Opacidad de la capa (legibilidad)',
    bgBlurLabel: 'Desenfoque del fondo', secTextures: 'Texturas predefinidas', showLogoLabel: 'Mostrar el logotipo "Pro Omnibus Gentibus"',
    secPaterNoster: 'Padre Nuestro', paterNosterBreadLabel: 'Expresión del "pan de cada día"',
    optCotidianum: 'Panem cotidianum (pan de cada día)', optSupersubstantialem: 'Panem supersubstantialem (pan supersustancial)',
    paterNosterBreadHint: 'Dos traducciones latinas tradicionales del griego epiousios (el texto de Lucas frente al de Mateo en la Vulgata) - se aplica al latín, español e inglés por igual.',
    secGroupAesthetics: 'Estética', secGroupLiturgical: 'Litúrgico',
    secPrayerElements: 'Litúrgico',
    gloriaPatriLabel: 'Gloria al Padre después de cada salmo y cántico',
    gloriaPatriHint: 'Añade el Gloria después de cada salmo y cántico, antes de repetir su antífona.',
    sacredSilenceLabel: 'Silencio sagrado después de la lectura',
    sacredSilenceHint: 'Marca una pausa de reflexión silenciosa después de la lectura breve, tal como recomienda la Instrucción General.',
    marianLabel: 'Antífona mariana al final de Completas',
    marianHint: 'Una antífona final a Nuestra Señora, rezada después de la despedida propia de Completas.',
    marianChoiceLabel: 'Qué antífona', marianNone: 'Ninguna',
    resetBtn: 'Restablecer toda la configuración', resetConfirm: '¿Restablecer toda la apariencia al tema Pergamino predeterminado?',
    intentionsTitle: 'Intenciones personales',
    intentionsHint: 'Las intenciones marcadas se añaden a las Preces de hoy, justo antes del Padrenuestro.',
    intentionsEmpty: 'Todavía no hay intenciones - añade una abajo.',
    intentionsPlaceholder: 'p. ej. Por el Santo Padre, el Papa', addBtn: 'Añadir',
    intentionsMasterToggle: 'Incluir intenciones en las Preces',
    diaryTitle: 'Diario de oración', streakLabel: (n) => `Día${n === 1 ? '' : 's'} seguido${n === 1 ? '' : 's'}`,
    markPrayed: 'Marcar como orado hoy', prayedDone: '✓ Orado hoy',
    diaryNoteLabel: 'Nota sobre la Lectio Brevis de hoy', diaryNotePlaceholder: 'Una reflexión sobre la lectura de hoy...',
    bookmarksHeading: 'Salmos marcados', bookmarksEmpty: 'Todavía no hay marcadores.',
    firstVisitTitle: 'En desarrollo', firstVisitDismiss: 'Entiendo, continuar',
    firstVisitBody: 'Esta aplicación está en desarrollo activo y profundo. El contenido todavía se está recopilando y verificando día a día - es posible que encuentres texto faltante, traducciones no correspondientes u otros errores. Por favor, ora con paciencia, y considera todo lo que veas aquí como provisional.',
    debugTitle: 'Menú de depuración beta',
    debugHint: 'Estado interno de configuración, editable directamente - solo para la caza de errores. El JSON inválido se ignora.',
    debugApply: 'Aplicar JSON', debugClearStorage: 'Borrar todo el almacenamiento local', debugReloadData: 'Forzar recarga de datos del día',
    debugPhoneSim: 'Abrir simulador de teléfono (375×812)',
    tHymnal: 'Himnario',
    infoTitle: 'Acerca de este proyecto', infoClose: 'Cerrar',
    infoBody: 'Pro Omnibus Gentibus es gratuito, lo será siempre, y es completamente de código abierto. Lee más abajo.',
    infoLinkMaking: 'Cómo se hizo', infoLinkBeta: 'Guía beta', infoLinkFuture: 'Planes futuros',
    hymnalTitle: 'Himnario', hymnalSearchPlaceholder: 'Buscar himnos por título o primer verso…',
    hymnalFilterHour: 'Hora', hymnalFilterAllHours: 'Todas las horas',
    hymnalFilterLang: 'Idiomas', hymnalFilterAllLangs: 'Todos', hymnalFilterMultiLang: 'Varios idiomas',
    hymnalFilterSingleLang: 'Un solo idioma',
    hymnalLangFilterHint: '"Varios idiomas" significa que el himno tiene más de una versión realmente cantada. La mayoría de los himnos de aquí son de un solo idioma (p. ej. cantados en latín) con una traducción provista solo para poder seguir el texto.',
    hymnalAlsoSungLabel: 'También es una versión realmente cantada en este idioma (no solo una traducción para seguir el texto)',
    hymnalEmpty: 'Ningún himno coincide.', hymnalCount: (n) => `${n} himno${n === 1 ? '' : 's'}`,
    hymnalOfficialBadge: 'Oficial', hymnalUserBadge: 'Mío',
    hymnalViewLyrics: 'Ver letra', hymnalHideLyrics: 'Ocultar letra',
    hymnalAddBtn: '+ Añadir un himno', hymnalAddFormTitle: 'Añadir un himno',
    hymnalFieldTitle: 'Título', hymnalFieldHours: 'Se usa en estas horas',
    hymnalFieldOriginalLang: 'Idioma original (el que se canta)',
    hymnalFieldLyricsFor: (lang) => `Letra (${lang})`,
    hymnalLyricsHint: 'Un verso por línea. Deja una línea en blanco para marcar un cambio de estrofa. Completa los idiomas que tengas — puedes dejar otros vacíos.',
    hymnalSaveBtn: 'Guardar himno', hymnalCancelBtn: 'Cancelar',
    hymnalDeleteBtn: 'Eliminar', hymnalDeleteConfirm: '¿Eliminar este himno? No se puede deshacer.',
    hymnalLocalNotice: 'Los himnos que añades se guardan solo en este dispositivo (esta aplicación no tiene servidor compartido) — no aparecerán para otras personas ni otros dispositivos.',
    hymnalTitleRequired: 'Por favor, escribe un título.',
    hymnalHoursRequired: 'Por favor, elige al menos una hora.',
    hymnalLyricsRequired: 'Por favor, escribe la letra en al menos un idioma.',
    hymnRecommendedTag: 'Recomendado para hoy',
  },
  la: {
    comingSoon: '(nondum)', prayNow: 'Ora Nunc',
    betaLabel: 'Modus Probationis',
    tIntentions: 'Intentiones', tDiary: 'Diarium Orationis', tSettings: 'Ordinationes', tBack: 'Aliam horam elige',
    tSmaller: 'Littera minor', tLarger: 'Littera maior', tDebug: 'Menu Probationis',
    settingsTitle: 'Ordinationes', backBtn: 'Redire',
    secPresets: 'Themata Provisa', secColorSync: 'Color Liturgicus Automaticus', secTypography: 'Typographia',
    secColors: 'Colores (Proprii)', secLayout: 'Forma et Modus Legendi', secBackground: 'Imago Fundi', secLogo: 'Signum',
    syncLabel: 'Colorem diei liturgici in ornamentis adhibere',
    syncHint: 'Automatice mutatur secundum tempus liturgicum et festa sanctorum (Albus, Viridis, Violaceus, Ruber, Roseus). Non mutat colorem fundi vel litterarum.',
    fontMainLabel: 'Character textus principalis', fontRubricLabel: 'Character rubricarum (titulorum)',
    secondaryFontToggle: 'Alium characterem pro lingua secundaria adhibere',
    secondaryFontHint: 'Si inactivum, tota pagina uno charactere utitur. Si activum, character principalis linguae Principali adhibetur, hic character alteri lateri.',
    fontLatinLabel: 'Character linguae secundariae',
    fsMain: 'Magnitudo textus principalis', fsRubric: 'Magnitudo rubricarum', fsLatin: 'Magnitudo linguae secundariae',
    lineHeightLabel: 'Spatium inter lineas', paraSpacingLabel: 'Spatium inter paragraphos',
    colorsHint: 'Quolibet colore mutato, ad thema proprium transfereris.',
    cBg: 'Fundus', cFg: 'Color litterarum', cAccent: 'Color ornamenti / rubricarum', cPanel: 'Fundus tabularum',
    readingModeLabel: 'Modus legendi', optScroll: 'Volumen continuum', optPaged: 'Paginae (cum vitta)',
    bilingualLabel: 'Ostensio bilinguis', optSideBySide: 'Utraque simul', optLatinOnly: 'Tantum Latine', optVernOnly: 'Tantum vernacule',
    showDividersLabel: 'Divisiones sectionum ostendere', showSymbolsLabel: 'Symbola liturgica ostendere († ★)',
    dropCapLabel: 'Litteræ initiales', optDcNone: 'Nullæ', optDcClean: 'Simplices', optDcRoman: 'Romanæ classicæ', optDcIllum: 'Illuminatæ medievales',
    sunsetLabel: 'Vesperæ secundum solis occasum commendatæ',
    sunsetHint: 'Situ tui instrumenti utitur (tantum si hoc activas) ut circulus "Ora Nunc" Vesperarum prope verum solis occasum accendatur, non hora fixa.',
    menuLangLabel: 'Lingua tabularum', bgNoImage: 'Nulla imago', bgUploadLabel: 'Imaginem fundi adde',
    bgClearLabel: 'Imaginem fundi tolle', bgClearBtn: 'Tolle', bgOverlayLabel: 'Opacitas velaminis (legibilitas)',
    bgBlurLabel: 'Confusio fundi', secTextures: 'Texturæ Provisæ', showLogoLabel: 'Signum "Pro Omnibus Gentibus" ostendere',
    secPaterNoster: 'Pater Noster', paterNosterBreadLabel: 'Verba "panis cotidiani"',
    optCotidianum: 'Panem cotidianum', optSupersubstantialem: 'Panem supersubstantialem',
    paterNosterBreadHint: 'Duæ formæ Latinæ traditionales verbi Græci epiousios (secundum Lucam et secundum Matthæum) - Latinæ, Hispanicæ, Anglicæque simul applicantur.',
    secGroupAesthetics: 'Pulchritudo', secGroupLiturgical: 'Liturgica',
    secPrayerElements: 'Liturgica',
    gloriaPatriLabel: 'Glória Patri post omnem psalmum et canticum',
    gloriaPatriHint: 'Glóriam Patri post omnem psalmum et canticum addit, antequam antiphona repetitur.',
    sacredSilenceLabel: 'Silentium sacrum post lectionem',
    sacredSilenceHint: 'Pausam silentii post lectionem brevem signat, sicut Institutio Generalis commendat.',
    marianLabel: 'Antiphona mariana in fine Completorii',
    marianHint: 'Antiphona finalis ad Beatam Virginem, post ipsam dimissionem Completorii dicta.',
    marianChoiceLabel: 'Quænam antiphona', marianNone: 'Nulla',
    resetBtn: 'Omnes ordinationes ad primam formam reddere', resetConfirm: 'Omnes ordinationes ad thema "Membrana" restituere?',
    intentionsTitle: 'Intentiones Personales',
    intentionsHint: 'Intentiones electæ hodiernis Precibus adduntur, ante Pater Noster.',
    intentionsEmpty: 'Nulla intentio adhuc - unam infra adde.',
    intentionsPlaceholder: 'e.g. Pro Summo Pontifice', addBtn: 'Adde',
    intentionsMasterToggle: 'Intentiones in Precibus includere',
    diaryTitle: 'Diarium Orationis', streakLabel: (n) => `Dies ${n === 1 ? '' : ''}continui`,
    markPrayed: 'Hodie oratum esse signa', prayedDone: '✓ Hodie oratum est',
    diaryNoteLabel: 'Nota de Lectione Brevi hodierna', diaryNotePlaceholder: 'Cogitatio de lectione hodierna...',
    bookmarksHeading: 'Psalmi Signati', bookmarksEmpty: 'Nulla signa adhuc.',
    firstVisitTitle: 'In Constructione', firstVisitDismiss: 'Intellego, pergere',
    firstVisitBody: 'Hæc applicatio adhuc diligenter et penitus in constructione est. Contentus dies ex die quæritur et verificatur - fieri potest ut textum deficientem, translationes non congruentes, aliosve errores invenias. Quæsumus patienter ora, et quidquid hic vides tamquam provisorium habe.',
    debugTitle: 'Menu Probationis Beta',
    debugHint: 'Status ordinationum crudus, directe mutabilis - tantum ad errores quærendos. JSON invalidum ignoratur.',
    debugApply: 'JSON Applicare', debugClearStorage: 'Omnem memoriam localem delere', debugReloadData: 'Data diei denuo petere',
    debugPhoneSim: 'Simulatorem telephonicum aperire (375×812)',
    tHymnal: 'Hymnarium',
    infoTitle: 'De Hoc Consilio', infoClose: 'Claudere',
    infoBody: 'Pro Omnibus Gentibus gratuitum est, semper erit, et fontes eius omnino aperti sunt. Plura infra lege.',
    infoLinkMaking: 'Quomodo Factum Sit', infoLinkBeta: 'Index Probationis', infoLinkFuture: 'Consilia Futura',
    hymnalTitle: 'Hymnarium', hymnalSearchPlaceholder: 'Hymnos quaere secundum titulum vel primum versum…',
    hymnalFilterHour: 'Hora', hymnalFilterAllHours: 'Omnes horæ',
    hymnalFilterLang: 'Linguæ', hymnalFilterAllLangs: 'Omnes', hymnalFilterMultiLang: 'Plures linguæ',
    hymnalFilterSingleLang: 'Una lingua',
    hymnalLangFilterHint: '"Plures linguæ" significat hymnum plus una versione revera cantata habere. Plerique hymni hic unius linguæ sunt (e.g. Latine cantati) cum translatione tantum ad legendum data.',
    hymnalAlsoSungLabel: 'Etiam versio vere cantata in hac lingua (non tantum translatio ad legendum)',
    hymnalEmpty: 'Nullus hymnus convenit.', hymnalCount: (n) => `${n} hymn${n === 1 ? 'us' : 'i'}`,
    hymnalOfficialBadge: 'Officialis', hymnalUserBadge: 'Meus',
    hymnalViewLyrics: 'Verba videre', hymnalHideLyrics: 'Verba celare',
    hymnalAddBtn: '+ Hymnum addere', hymnalAddFormTitle: 'Hymnum addere',
    hymnalFieldTitle: 'Titulus', hymnalFieldHours: 'His horis adhibetur',
    hymnalFieldOriginalLang: 'Lingua originalis (quæ revera cantatur)',
    hymnalFieldLyricsFor: (lang) => `Verba (${lang})`,
    hymnalLyricsHint: 'Unus versus per lineam. Lineam vacuam relinque ut mutationem strophæ signes. Linguas quas habes comple - alias vacuas relinquere potes.',
    hymnalSaveBtn: 'Hymnum servare', hymnalCancelBtn: 'Cancellare',
    hymnalDeleteBtn: 'Delere', hymnalDeleteConfirm: 'Delere hunc hymnum? Hoc revocari non potest.',
    hymnalLocalNotice: 'Hymni quos addis tantum in hoc instrumento servantur (nullus servus communis huic applicationi est) - aliis personis vel instrumentis non apparebunt.',
    hymnalTitleRequired: 'Quæsumus, titulum scribe.',
    hymnalHoursRequired: 'Quæsumus, saltem unam horam elige.',
    hymnalLyricsRequired: 'Quæsumus, verba in saltem una lingua scribe.',
    hymnRecommendedTag: 'Hodie commendatus',
  },
};
function ui() { return UI[settings.menuLang] || UI.en; }

/* ============================================================
   SETTINGS ENGINE
   Everything the Settings tab controls lives in one object,
   persisted to localStorage, applied to :root as CSS custom
   properties (see template.html's :root block for the full list
   of variables a preset can drive).
   ============================================================ */
const SETTINGS_KEY = 'loth_settings_v1';
const INTENTIONS_KEY = 'loth_intentions_v1';
const DIARY_KEY = 'loth_diary_v1';
const LASTPOS_KEY = 'loth_lastpos_v1';
const USER_HYMNS_KEY = 'loth_user_hymns_v1';

const FONT_CHOICES = [
  { id: 'garamond', label: 'EB Garamond', css: "'EB Garamond', Georgia, 'Times New Roman', serif" },
  { id: 'cormorant', label: 'Cormorant Garamond', css: "'Cormorant Garamond', Georgia, serif" },
  { id: 'cardo', label: 'Cardo (manuscript)', css: "'Cardo', 'Palatino Linotype', Georgia, serif" },
  { id: 'cinzel', label: 'Cinzel (inscriptional)', css: "'Cinzel', Georgia, serif" },
  { id: 'crimson', label: 'Crimson Text', css: "'Crimson Text', Georgia, serif" },
  { id: 'alegreya', label: 'Alegreya', css: "'Alegreya', Georgia, serif" },
  { id: 'unifraktur', label: 'UnifrakturCook (blackletter)', css: "'UnifrakturCook', 'Cardo', serif" },
  { id: 'romanuncial', label: 'Roman Uncial', css: "'Roman Uncial Modern', 'Cardo', serif" },
  { id: 'kliment', label: 'Kliment', css: "'Kliment Std', 'Cardo', serif" },
  { id: 'georgia', label: 'Georgia (system serif)', css: "Georgia, 'Times New Roman', serif" },
  { id: 'sans', label: 'Clean Sans-serif', css: "-apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" },
];
function fontCss(id) { const f = FONT_CHOICES.find(f => f.id === id); return f ? f.css : FONT_CHOICES[0].css; }

const TEXTURE_CHOICES = [
  { id: 'none', label: 'None' },
  { id: 'vellum', label: 'Aged Vellum' },
  { id: 'leather', label: 'Dark Leather' },
  { id: 'stone', label: 'Monastic Stone' },
  { id: 'glass', label: 'Stained Glass Grain' },
];
function textureBackgroundImage(id) {
  switch (id) {
    case 'vellum':
      return "radial-gradient(ellipse at 20% 20%, rgba(200,170,110,0.25), transparent 60%)," +
        "radial-gradient(ellipse at 80% 70%, rgba(150,110,60,0.18), transparent 55%)," +
        "repeating-linear-gradient(0deg, rgba(120,90,50,0.04) 0px, rgba(120,90,50,0.04) 1px, transparent 1px, transparent 3px)";
    case 'leather':
      return "radial-gradient(ellipse at 30% 30%, rgba(90,60,30,0.5), transparent 60%)," +
        "radial-gradient(ellipse at 75% 80%, rgba(40,25,15,0.6), transparent 55%)," +
        "repeating-radial-gradient(circle at 50% 50%, rgba(0,0,0,0.08) 0px, transparent 2px, transparent 6px)";
    case 'stone':
      return "radial-gradient(circle at 15% 15%, rgba(255,255,255,0.05), transparent 40%)," +
        "radial-gradient(circle at 85% 85%, rgba(0,0,0,0.12), transparent 45%)," +
        "repeating-linear-gradient(45deg, rgba(0,0,0,0.03) 0px, rgba(0,0,0,0.03) 2px, transparent 2px, transparent 10px)";
    case 'glass':
      return "repeating-linear-gradient(60deg, rgba(120,60,140,0.10) 0px, rgba(60,120,180,0.08) 12px, rgba(180,140,40,0.09) 24px, rgba(160,30,50,0.08) 36px)";
    default:
      return 'none';
  }
}

const PRESETS = {
  parchment: {
    label: 'Parchment', bg: '#faf3e6', fg: '#2b241c', accent: '#7a5c3e', accentSoft: '#ceb98f',
    panelBg: '#fffaf0', panelBorder: '#e0d2b0', fontMain: 'garamond', fontRubric: 'cinzel', fontLatin: 'cormorant',
    texture: 'vellum',
  },
  light: {
    label: 'Light', bg: '#ffffff', fg: '#1c1c1c', accent: '#3a5a8c', accentSoft: '#cfe0f5',
    panelBg: '#f7f8fa', panelBorder: '#dde1e6', fontMain: 'georgia', fontRubric: 'sans', fontLatin: 'georgia',
    texture: 'none',
  },
  dark: {
    label: 'Dark', bg: '#1c1d21', fg: '#e7e6e2', accent: '#c8a86a', accentSoft: '#4a4436',
    panelBg: '#26272c', panelBorder: '#3a3b41', fontMain: 'georgia', fontRubric: 'cinzel', fontLatin: 'georgia',
    texture: 'none',
  },
  oled: {
    label: 'OLED Black', bg: '#000000', fg: '#e5e5e5', accent: '#b8925a', accentSoft: '#2a2a2a',
    panelBg: '#0a0a0a', panelBorder: '#232323', fontMain: 'georgia', fontRubric: 'cinzel', fontLatin: 'georgia',
    texture: 'none',
  },
  candlelight: {
    label: 'Warm Candlelight', bg: '#2a1c10', fg: '#f0dcb8', accent: '#e0a84a', accentSoft: '#4a3218',
    panelBg: '#33230f', panelBorder: '#5a3f1c', fontMain: 'cormorant', fontRubric: 'cinzel', fontLatin: 'cormorant',
    texture: 'leather',
  },
  highcontrast: {
    label: 'High-Contrast Dark', bg: '#000000', fg: '#ffffff', accent: '#ffd54a', accentSoft: '#3a3a00',
    panelBg: '#111111', panelBorder: '#ffffff', fontMain: 'sans', fontRubric: 'sans', fontLatin: 'sans',
    texture: 'none',
  },
  sepia: {
    label: 'Sepia Reader', bg: '#f1e7d0', fg: '#4a3b28', accent: '#8a5a2a', accentSoft: '#e2c99a',
    panelBg: '#f8f0dc', panelBorder: '#d8c294', fontMain: 'crimson', fontRubric: 'cinzel', fontLatin: 'crimson',
    texture: 'vellum',
  },
  monastic: {
    label: 'Monastic Stone', bg: '#e8e6e1', fg: '#2e2c28', accent: '#5a5650', accentSoft: '#cfcbc2',
    panelBg: '#f0eee9', panelBorder: '#c9c5bc', fontMain: 'alegreya', fontRubric: 'cinzel', fontLatin: 'alegreya',
    texture: 'stone',
  },
  stainedglass: {
    label: 'Stained Glass', bg: '#171326', fg: '#ece6ff', accent: '#c9a3ff', accentSoft: '#352a52',
    panelBg: '#1f1a33', panelBorder: '#3f3460', fontMain: 'cormorant', fontRubric: 'cinzel', fontLatin: 'cormorant',
    texture: 'glass',
  },
  custom: { label: 'Custom' },
};

function defaultSettings() {
  return {
    preset: 'parchment',
    liturgicalColorSync: true,
    bg: PRESETS.parchment.bg, fg: PRESETS.parchment.fg,
    accent: PRESETS.parchment.accent, accentSoft: PRESETS.parchment.accentSoft,
    panelBg: PRESETS.parchment.panelBg, panelBorder: PRESETS.parchment.panelBorder,
    fontMain: 'garamond', fontRubric: 'cinzel', fontLatin: 'cormorant',
    fontSizeMain: 18, fontSizeRubric: 12, fontSizeLatin: 18,
    lineHeight: 1.65, paraSpacing: 0.9,
    readingMode: 'scroll', // 'scroll' | 'paged'
    bilingualMode: 'sideBySide', // 'sideBySide' | 'latinOnly' | 'vernacularOnly'
    showDividers: true, showSymbols: true, dropCapStyle: 'clean', // 'none'|'clean'|'roman'|'illuminated'
    texture: 'vellum',
    bgImage: null, bgOverlayOpacity: 0.82, bgBlur: 0,
    showLogo: true,
    sunsetAwareVespers: false,
    menuLang: 'es',
    useSecondaryFont: true,
    intentionsEnabled: true,
    paterNosterBread: 'supersubstantialem', // 'supersubstantialem' | 'cotidianum'
    showGloriaPatri: true,
    sacredSilence: true,
    marianAntiphonEnabled: true,
    marianAntiphonChoice: 'salve_regina', // key into MARIAN_ANTIPHONS, or 'none'
  };
}

function loadSettings() {
  try {
    const stored = JSON.parse(localStorage.getItem(SETTINGS_KEY) || '{}');
    return Object.assign(defaultSettings(), stored);
  } catch (e) { return defaultSettings(); }
}
function saveSettings() {
  try { localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings)); } catch (e) { /* storage unavailable */ }
}

let settings = loadSettings();
// Deliberately NOT persisted - each new visit that wants the beta English
// translation has to see the warning again, not just once ever.
let betaMode = false;

function applyPreset(id) {
  const p = PRESETS[id];
  settings.preset = id;
  if (p && id !== 'custom') {
    settings.bg = p.bg; settings.fg = p.fg; settings.accent = p.accent; settings.accentSoft = p.accentSoft;
    settings.panelBg = p.panelBg; settings.panelBorder = p.panelBorder;
    settings.fontMain = p.fontMain; settings.fontRubric = p.fontRubric; settings.fontLatin = p.fontLatin;
    settings.texture = p.texture;
  }
  saveSettings();
  applySettingsToDOM();
  if (document.getElementById('settingsScreen') && !document.getElementById('settingsScreen').classList.contains('hidden')) {
    renderSettingsScreen();
  }
}

// Liturgical color -> accent override. When sync is on, headers/rubrics/
// borders tint to today's actual liturgical color regardless of the chosen
// preset's own accent - this only touches --accent/--accent-soft, never
// --bg/--fg, so legibility (a preset's own careful contrast choice) is never
// put at risk by whatever color the calendar happens to be.
const LITURGICAL_COLOR_ACCENTS = {
  white:  { accent: '#8a7638', accentSoft: '#f3ecc9' },
  green:  { accent: '#2f6b3a', accentSoft: '#cfe8d2' },
  violet: { accent: '#5a3c8a', accentSoft: '#e0d3f2' },
  red:    { accent: '#a3272c', accentSoft: '#f3cfd0' },
  rose:   { accent: '#b9587f', accentSoft: '#f6d9e4' },
};

function applySettingsToDOM() {
  const root = document.documentElement;
  const dayData = currentDayData();
  let accent = settings.accent, accentSoft = settings.accentSoft;
  if (settings.liturgicalColorSync && dayData && dayData.liturgical_meta) {
    const lc = LITURGICAL_COLOR_ACCENTS[dayData.liturgical_meta.color];
    if (lc) { accent = lc.accent; accentSoft = lc.accentSoft; }
  }
  root.style.setProperty('--bg', settings.bg);
  root.style.setProperty('--fg', settings.fg);
  root.style.setProperty('--accent', accent);
  root.style.setProperty('--accent-soft', accentSoft);
  root.style.setProperty('--panel-bg', settings.panelBg);
  root.style.setProperty('--panel-border', settings.panelBorder);
  root.style.setProperty('--link', accent);
  root.style.setProperty('--font-main', fontCss(settings.fontMain));
  root.style.setProperty('--font-rubric', fontCss(settings.fontRubric));
  // "Secondary language font" only actually differs from Main when the
  // toggle is on - off means one font for the whole page, matching what a
  // reader who's never touched Settings would expect by default.
  root.style.setProperty('--font-latin', settings.useSecondaryFont ? fontCss(settings.fontLatin) : fontCss(settings.fontMain));
  root.style.setProperty('--font-size-main', settings.fontSizeMain + 'px');
  root.style.setProperty('--font-size-rubric', settings.fontSizeRubric + 'px');
  root.style.setProperty('--font-size-latin', settings.useSecondaryFont ? (settings.fontSizeLatin + 'px') : (settings.fontSizeMain + 'px'));
  root.style.setProperty('--line-height', settings.lineHeight);
  root.style.setProperty('--para-spacing', settings.paraSpacing + 'em');

  const bgImg = settings.bgImage ? `url("${settings.bgImage}")` : 'none';
  const texImg = textureBackgroundImage(settings.texture);
  const combined = settings.bgImage
    ? bgImg
    : (texImg !== 'none' ? texImg : 'none');
  root.style.setProperty('--bg-image', combined);
  root.style.setProperty('--bg-overlay-opacity', settings.bgImage ? settings.bgOverlayOpacity : 0);
  root.style.setProperty('--bg-blur', settings.bgImage ? settings.bgBlur + 'px' : '0px');

  document.body.classList.toggle('hide-dividers', !settings.showDividers);
  document.body.classList.toggle('hide-symbols', !settings.showSymbols);
  document.body.classList.remove('dropcap-none', 'dropcap-clean', 'dropcap-roman', 'dropcap-illuminated');
  document.body.classList.add('dropcap-' + settings.dropCapStyle);
  document.body.classList.toggle('reading-paged', settings.readingMode === 'paged');

  document.querySelectorAll('.app-logo').forEach(el => el.style.display = settings.showLogo ? '' : 'none');
}

/* ============================================================
   LOGO (inline SVG placeholder - "Pro Omnibus Gentibus")
   ============================================================ */
function logoSvg(size) {
  return `<svg width="${size}" height="${size}" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <circle cx="32" cy="32" r="30" fill="none" stroke="currentColor" stroke-width="1.5"/>
    <circle cx="32" cy="32" r="25" fill="none" stroke="currentColor" stroke-width="0.75"/>
    <path d="M32 12 L32 52 M18 22 L46 22" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M32 12 L26 20 L38 20 Z" fill="currentColor"/>
    <circle cx="32" cy="32" r="3.4" fill="none" stroke="currentColor" stroke-width="1.2"/>
  </svg>`;
}
function renderLogo(elId, small) {
  const el = document.getElementById(elId);
  if (!el) return;
  el.style.color = 'var(--accent)';
  el.innerHTML = logoSvg(small ? 28 : 40) +
    `<div class="wordmark"><span class="big">Pro Omnibus Gentibus</span><span class="small">Liturgia Horarum</span></div>`;
  el.style.display = settings.showLogo ? '' : 'none';
}

/* ============================================================
   LITURGICAL CALENDAR HERO
   ============================================================ */
function heroHtml(dayData, left) {
  if (!dayData) return '';
  const meta = dayData.liturgical_meta || { color: 'green', rank: {}, title: null };
  const dateHuman = (dayData.date_human && (dayData.date_human[left] || dayData.date_human.en)) || '';
  const title = meta.title ? (meta.title[left] || meta.title.en) : (dayData.day_description[left] || dayData.day_description.en);
  const rankText = meta.rank ? (meta.rank[left] || meta.rank.en || '') : '';
  const colorLabel = { white: 'White', green: 'Green', violet: 'Violet', red: 'Red', rose: 'Rose' }[meta.color] || meta.color;
  return `
    <div class="hero-text">
      <p class="hero-date">${esc(dateHuman)}</p>
      <p class="hero-title">${title}</p>
      ${rankText ? `<p class="hero-rank">${esc(rankText)}</p>` : ''}
    </div>
    <span class="color-badge color-${meta.color}"><span class="dot"></span>${esc(colorLabel)}</span>
  `;
}
function renderHero() {
  const dayData = currentDayData();
  const left = leftSel ? leftSel.value : DATA.languages[0];
  const html = heroHtml(dayData, left);
  const a = document.getElementById('heroHourSelect'); if (a) a.innerHTML = html;
  const b = document.getElementById('heroMain'); if (b) b.innerHTML = html;
}

/* ============================================================
   DATE / TIMEZONE HELPERS (shared by hour-select screen and main)
   ============================================================ */
const COMMON_TIMEZONES = [
  'UTC', 'Europe/Rome', 'Europe/Madrid', 'Europe/London', 'Europe/Paris',
  'America/New_York', 'America/Chicago', 'America/Denver', 'America/Los_Angeles',
  'America/Mexico_City', 'America/Bogota', 'America/Sao_Paulo', 'America/Argentina/Buenos_Aires',
  'Asia/Manila', 'Asia/Tokyo', 'Asia/Kolkata', 'Australia/Sydney', 'Pacific/Auckland',
];
let tzList = COMMON_TIMEZONES;
try {
  if (typeof Intl.supportedValuesOf === 'function') tzList = Intl.supportedValuesOf('timeZone');
} catch (e) { /* fall back to curated list */ }
const browserTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
if (!tzList.includes(browserTz)) tzList = [browserTz, ...tzList];

function isoDateInTimeZone(tz) {
  return new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date());
}
function closestAvailableDate(isoTarget) {
  if (DATA.dates[isoTarget]) return isoTarget;
  const targetMs = new Date(isoTarget).getTime();
  let best = DATA.date_order[0], bestDiff = Infinity;
  for (const iso of DATA.date_order) {
    const diff = Math.abs(new Date(iso).getTime() - targetMs);
    if (diff < bestDiff) { bestDiff = diff; best = iso; }
  }
  return best;
}
function currentDayData() {
  if (!dateSel || !dateSel.value) {
    const todayIso = closestAvailableDate(isoDateInTimeZone(browserTz));
    return DATA.dates[todayIso];
  }
  return DATA.dates[dateSel.value];
}

/* ============================================================
   HOUR SELECTION SCREEN
   ============================================================ */
// Fixed-clock windows (local time) used unless sunset-aware Vespers is on
// and a real sunset could be computed for the viewer's location.
function recommendedHourByClock(hour24) {
  if (hour24 >= 5 && hour24 < 12) return 'lauds';
  if (hour24 >= 21 || hour24 < 5) return 'compline';
  return 'vespers'; // 12:00-20:59 - the long afternoon/evening stretch
}

// Simple NOAA-style approximate sunset calculation (good to a few minutes,
// which is plenty for "should the Vespers halo be lit"). Returns a Date for
// today's sunset at the given lat/lon, or null if the sun doesn't set today
// (polar regions) - callers already have a clock-time fallback for that.
function approximateSunset(lat, lon, date) {
  const rad = Math.PI / 180;
  const start = new Date(Date.UTC(date.getFullYear(), 0, 1));
  const dayOfYear = Math.floor((date - start) / 86400000) + 1;
  const decl = 23.44 * rad * Math.sin(rad * (360 / 365) * (dayOfYear - 81));
  const latRad = lat * rad;
  const cosH = -Math.tan(latRad) * Math.tan(decl);
  if (cosH < -1 || cosH > 1) return null; // sun never sets / never rises today at this latitude
  const hourAngle = Math.acos(cosH) / rad; // degrees
  const solarNoonUtcHours = 12 - lon / 15; // rough, ignores equation of time (fine for this purpose)
  const sunsetUtcHours = solarNoonUtcHours + hourAngle / 15;
  const sunset = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  sunset.setUTCHours(0, 0, 0, 0);
  sunset.setUTCMilliseconds(sunsetUtcHours * 3600000);
  return sunset;
}

let cachedGeo = null;
function recommendedHourNow(callback) {
  const now = new Date();
  const clockHour = now.getHours();
  const clockPick = recommendedHourByClock(clockHour);
  if (!settings.sunsetAwareVespers || !navigator.geolocation) {
    callback(clockPick);
    return;
  }
  const useGeo = (pos) => {
    cachedGeo = pos;
    const sunset = approximateSunset(pos.coords.latitude, pos.coords.longitude, now);
    if (!sunset) { callback(clockPick); return; }
    const diffMin = (now - sunset) / 60000;
    if (diffMin >= -90 && diffMin <= 210) { callback('vespers'); return; } // 1.5h before to 3.5h after sunset
    // Outside the sunset-driven Vespers window: still use fixed windows for Lauds/Compline.
    callback(clockPick === 'vespers' ? (diffMin < 0 ? 'lauds' : 'compline') : clockPick);
  };
  if (cachedGeo) { useGeo(cachedGeo); return; }
  navigator.geolocation.getCurrentPosition(useGeo, () => callback(clockPick), { timeout: 4000 });
}

function renderHourCards() {
  const dayData = currentDayData();
  // Hour-card names follow the Menu Language (navigation chrome), not the
  // Main/Vernacular content-language pickers - DATA.hour_labels already has
  // en/es/la, matching MENU_LANG_NAMES' keys exactly.
  const labels = (DATA.hour_labels && DATA.hour_labels[settings.menuLang]) || DATA.hour_labels.en || {};
  const s = ui();
  const container = document.getElementById('hourCards');
  if (!container || !dayData) return;

  recommendedHourNow((prayNowHour) => {
    let html = '';
    for (const h of DATA.hour_order) {
      const implemented = DATA.implemented_hours.includes(h);
      const isPrayNow = implemented && h === prayNowHour;
      html += `<button class="hour-card${isPrayNow ? ' pray-now' : ''}" data-hour="${esc(h)}"
                 data-praynow-label="${esc(s.prayNow)}" ${implemented ? '' : 'disabled'}>
        <p class="hc-name">${esc(labels[h] || h)}</p>
        ${!implemented ? `<p class="hc-soon">${esc(s.comingSoon)}</p>` : ''}
      </button>`;
    }
    container.innerHTML = html;
    container.querySelectorAll('.hour-card:not(:disabled)').forEach(btn => {
      btn.addEventListener('click', () => {
        if (hourSel) hourSel.value = btn.dataset.hour;
        goToMainScreen();
      });
    });
  });
}

/* ============================================================
   SCREEN NAVIGATION
   ============================================================ */
function showScreen(id) {
  ['hourSelectScreen', 'mainScreen', 'settingsScreen', 'hymnalScreen'].forEach(s => {
    document.getElementById(s).classList.toggle('hidden', s !== id);
  });
  window.scrollTo(0, 0);
}
function goToHourSelect() {
  showScreen('hourSelectScreen');
  renderHero();
  renderHourCards();
}
function goToMainScreen() {
  showScreen('mainScreen');
  applyChrome();
  saveLastPosition();
}
let settingsReturnScreen = 'hourSelectScreen';
function openSettings(fromScreenId) {
  settingsReturnScreen = fromScreenId;
  showScreen('settingsScreen');
  renderSettingsScreen();
}
function closeSettings() {
  showScreen(settingsReturnScreen);
  applySettingsToDOM();
  if (settingsReturnScreen === 'hourSelectScreen') { renderHero(); renderHourCards(); }
  else { renderHero(); render(); }
}

let hymnalReturnScreen = 'hourSelectScreen';
function openHymnal(fromScreenId) {
  hymnalReturnScreen = fromScreenId;
  showScreen('hymnalScreen');
  renderHymnalScreen();
}
function closeHymnal() {
  showScreen(hymnalReturnScreen);
  if (hymnalReturnScreen === 'hourSelectScreen') { renderHero(); renderHourCards(); }
  else { renderHero(); render(); }
}

const PROJECT_DOCS = {
  making: 'making-pog.html',
  beta: 'beta-guide.html',
  future: 'future-plans.html',
};
function docLangParam() {
  // The docs only ship Spanish and English; Latin menu users default to Spanish.
  return settings.menuLang === 'en' ? 'en' : 'es';
}
function openInfoModal() {
  const s = ui();
  document.getElementById('infoModalTitle').textContent = s.infoTitle;
  document.getElementById('infoModalBody').textContent = s.infoBody;
  document.getElementById('infoModalClose').textContent = s.infoClose;
  const lang = docLangParam();
  const makingLink = document.getElementById('infoLinkMaking');
  const betaLink = document.getElementById('infoLinkBeta');
  const futureLink = document.getElementById('infoLinkFuture');
  makingLink.textContent = s.infoLinkMaking; makingLink.href = `${PROJECT_DOCS.making}?lang=${lang}`;
  betaLink.textContent = s.infoLinkBeta; betaLink.href = `${PROJECT_DOCS.beta}?lang=${lang}`;
  futureLink.textContent = s.infoLinkFuture; futureLink.href = `${PROJECT_DOCS.future}?lang=${lang}`;
  document.getElementById('infoModal').classList.remove('hidden');
}
function closeInfoModal() {
  document.getElementById('infoModal').classList.add('hidden');
}

function saveLastPosition() {
  try {
    localStorage.setItem(LASTPOS_KEY, JSON.stringify({
      date: dateSel ? dateSel.value : null, hour: hourSel ? hourSel.value : null, ts: Date.now(),
    }));
  } catch (e) { /* storage unavailable */ }
}
function loadLastPosition() {
  try { return JSON.parse(localStorage.getItem(LASTPOS_KEY) || 'null'); } catch (e) { return null; }
}

/* ============================================================
   EXISTING RENDER PIPELINE (ported, extended for bilingual mode,
   paging, dividers, symbols, drop caps)
   ============================================================ */
const leftSel = document.getElementById('leftLang');
const rightSel = document.getElementById('rightLang');
const hourSel = document.getElementById('hourSelect');
const tzSel = document.getElementById('tzSelect');
const dateSel = document.getElementById('dateSelect');
const tzNote = document.getElementById('tzNote');

let hymnChoiceByHour = {};

function poolsFromRawHymns(raw) {
  // Build a pool for every hour tag actually present in the data, not a
  // fixed 3-item list - see build_hymn_pools()'s docstring (render_day.py)
  // for why. Matters here in particular because user-added hymns (Hymnal
  // screen) can be tagged with any hour.
  const contexts = new Set();
  for (const [hid, h] of Object.entries(raw)) {
    if (hid === '_note') continue;
    for (const ctx of (h.applicability || [])) contexts.add(ctx);
  }
  const pools = {};
  for (const ctx of contexts) {
    pools[ctx] = [];
    for (const [hid, h] of Object.entries(raw)) {
      if (hid === '_note') continue;
      if ((h.applicability || []).includes(ctx)) {
        const lines = {};
        for (const lang of DATA.languages) lines[lang] = (h.lines && h.lines[lang]) || [];
        pools[ctx].push({ id: hid, title: h.title, original_language: h.original_language,
          also_sung_in: h.also_sung_in || [], lines });
      }
    }
  }
  return pools;
}
// Personal hymns a user has added themselves (Hymnal screen) - saved only
// on this device (localStorage), same as Intentions/Diary. Kept as their
// own list, not written into content/proper_texts/hymns.json (there's no
// backend for that to reach), and folded into DATA.hymn_pools at render
// time instead so they show up both in the Hymnal browsing screen AND the
// existing per-hour hymn-choice dropdown.
function loadUserHymns() {
  try { return JSON.parse(localStorage.getItem(USER_HYMNS_KEY) || '[]'); } catch (e) { return []; }
}
function saveUserHymns(list) {
  try { localStorage.setItem(USER_HYMNS_KEY, JSON.stringify(list)); } catch (e) { /* storage unavailable */ }
}
function mergeUserHymnsIntoPools() {
  if (!DATA.hymn_pools) DATA.hymn_pools = {};
  // Idempotent: strip any previously-merged user hymns first, so calling
  // this again after a fresh fetch (which overwrites DATA.hymn_pools
  // wholesale) or after an add/delete never double-adds or leaves stale
  // copies behind.
  for (const ctx of Object.keys(DATA.hymn_pools)) {
    DATA.hymn_pools[ctx] = DATA.hymn_pools[ctx].filter(h => !h.user_added);
  }
  for (const h of loadUserHymns()) {
    const lines = {};
    for (const lang of DATA.languages) lines[lang] = (h.lines && h.lines[lang]) || [];
    const entry = { id: h.id, title: h.title, original_language: h.original_language,
      also_sung_in: h.also_sung_in || [], lines, user_added: true };
    for (const ctx of (h.applicability || [])) {
      if (!DATA.hymn_pools[ctx]) DATA.hymn_pools[ctx] = [];
      DATA.hymn_pools[ctx].push(entry);
    }
  }
}
mergeUserHymnsIntoPools();

// Relative to docs/*.html itself (a docs/content/... copy kept in sync by
// render_day.py's copy_docs_assets, not "../content" up to the project
// root) - GitHub Pages serves docs/ AS the site root, so "../" would 404
// there even though it happens to also work under the local dev server.
fetch('content/proper_texts/hymns.json')
  .then(r => r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)))
  .then(raw => { DATA.hymn_pools = poolsFromRawHymns(raw); mergeUserHymnsIntoPools(); render(); })
  .catch(() => { /* no server, or fetch blocked under file:// - keep the baked-in pool */ });

for (const iso of DATA.date_order) {
  fetch('/api/day?date=' + encodeURIComponent(iso))
    .then(r => r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)))
    .then(fresh => { DATA.dates[iso] = fresh; render(); renderHero(); })
    .catch(() => { /* dev_server.py not running - keep the baked-in day */ });
}

function populateDateOptions() {
  const left = leftSel.value;
  const prev = dateSel.value;
  dateSel.innerHTML = '';
  for (const iso of DATA.date_order) {
    const o = document.createElement('option');
    o.value = iso;
    const dh = DATA.dates[iso].date_human;
    o.textContent = (dh && (dh[left] || dh.en)) || iso;
    dateSel.appendChild(o);
  }
  if (prev && DATA.dates[prev]) dateSel.value = prev;
}

function populateTimezoneOptions() {
  const left = leftSel.value;
  const regionNames = (DATA.tz_region_names && DATA.tz_region_names[left]) || {};
  const prev = tzSel.value;
  tzSel.innerHTML = '';
  for (const tz of tzList) {
    const o = document.createElement('option');
    o.value = tz;
    const slash = tz.indexOf('/');
    if (slash === -1) {
      o.textContent = tz.replace(/_/g, ' ');
    } else {
      const region = tz.slice(0, slash);
      const rest = tz.slice(slash + 1).replace(/_/g, ' ');
      o.textContent = (regionNames[region] || region) + ' / ' + rest;
    }
    tzSel.appendChild(o);
  }
  tzSel.value = prev && tzList.includes(prev) ? prev : browserTz;
}

const TZNOTE_TEXT = {
  en: (today, tz, first, last) => `&#9888; Today is <strong>${today}</strong> in ${tz}, which is outside the ` +
    `range of dates generated for this demo (<strong>${first}</strong> to <strong>${last}</strong>). ` +
    `Showing the closest available date instead.`,
  es: (today, tz, first, last) => `&#9888; Hoy es <strong>${today}</strong> en ${tz}, fecha fuera del ` +
    `intervalo generado para esta demo (<strong>${first}</strong> a <strong>${last}</strong>). ` +
    `Se muestra la fecha disponible más cercana.`,
  la: (today, tz, first, last) => `&#9888; Hodie est <strong>${today}</strong> in ${tz}, dies extra ` +
    `intervallum ad hanc demonstrationem generatum (<strong>${first}</strong> usque ad <strong>${last}</strong>). ` +
    `Dies proxima disponibilis ostenditur.`,
};
function updateTzNote() {
  const left = leftSel.value;
  const tz = tzSel.value;
  const todayInTz = isoDateInTimeZone(tz);
  if (DATA.dates[todayInTz]) {
    tzNote.style.display = 'none';
  } else {
    tzNote.style.display = '';
    const first = DATA.date_order[0], last = DATA.date_order[DATA.date_order.length - 1];
    const build = TZNOTE_TEXT[left] || TZNOTE_TEXT.en;
    tzNote.innerHTML = build(todayInTz, tz.replace(/_/g, ' '), first, last);
  }
}
function onTzChange() {
  updateTzNote();
  dateSel.value = closestAvailableDate(isoDateInTimeZone(tzSel.value));
  render();
}
tzSel.addEventListener('change', onTzChange);

// English (beta) is never part of DATA.languages (there is no stored English
// content) - it's added/removed from these two dropdowns purely as a UI
// option, gated by the beta-mode checkbox in the top bar. See
// applyBetaEnglishTranslation for how a selection of 'en' is actually filled.
function populateLanguageSelectors() {
  const prevLeft = leftSel.value, prevRight = rightSel.value;
  for (const sel of [leftSel, rightSel]) {
    sel.innerHTML = '';
    for (const code of DATA.languages) {
      const o = document.createElement('option');
      o.value = code; o.textContent = LANG_NAMES[code] || code;
      sel.appendChild(o);
    }
    if (betaMode) {
      const o = document.createElement('option');
      o.value = 'en'; o.textContent = 'English (beta, machine-translated)';
      sel.appendChild(o);
    }
  }
  leftSel.value = (prevLeft && [...leftSel.options].some(o => o.value === prevLeft)) ? prevLeft : DATA.languages[0];
  rightSel.value = (prevRight && [...rightSel.options].some(o => o.value === prevRight))
    ? prevRight : (DATA.languages[1] || DATA.languages[0]);
}
populateLanguageSelectors();

function populateHourOptions() {
  const left = leftSel.value;
  const prev = hourSel.value;
  const labels = (DATA.hour_labels && DATA.hour_labels[left]) || {};
  const comingSoon = (DATA.chrome_labels[left] || DATA.chrome_labels.en).coming_soon;
  hourSel.innerHTML = '';
  for (const h of DATA.hour_order) {
    const o = document.createElement('option');
    o.value = h;
    o.textContent = labels[h] || h;
    if (!DATA.implemented_hours.includes(h)) {
      o.disabled = true;
      o.textContent += ' ' + comingSoon;
    }
    hourSel.appendChild(o);
  }
  hourSel.value = DATA.hour_order.includes(prev) ? prev : DATA.default_hour;
}

function updateChromeLabels() {
  const left = leftSel.value;
  const cl = DATA.chrome_labels[left] || DATA.chrome_labels.en;
  document.getElementById('tzLabel').textContent = cl.timezone;
  document.getElementById('dateLabel').textContent = cl.date;
  document.getElementById('hourLabel').textContent = cl.hour;
  document.getElementById('leftLabel').textContent = cl.main;
  document.getElementById('rightLabel').textContent = (left === 'la') ? cl.vernacular : cl.translation;
}

function applyChrome() {
  updateChromeLabels();
  populateHourOptions();
  populateDateOptions();
  populateTimezoneOptions();
  updateTzNote();
  renderHero();
  render();
}
leftSel.addEventListener('change', applyChrome);

/* ============================================================
   MENU LANGUAGE (Latin / Español / English) - the app's own
   interface chrome, independent of the Main/Vernacular content
   language pickers above.
   ============================================================ */
function syncMenuLangSelects() {
  [document.getElementById('menuLangSelectA'), document.getElementById('menuLangSelectB')].forEach(sel => {
    if (!sel) return;
    if (sel.options.length === 0) {
      Object.entries(MENU_LANG_NAMES).forEach(([code, label]) => {
        const o = document.createElement('option'); o.value = code; o.textContent = label;
        sel.appendChild(o);
      });
    }
    sel.value = settings.menuLang;
  });
}
function refreshChromeText() {
  const s = ui();
  document.getElementById('betaLabelA').textContent = s.betaLabel;
  document.getElementById('betaLabelB').textContent = s.betaLabel;
  document.getElementById('btnIntentions').title = s.tIntentions;
  document.getElementById('btnIntentionsFromHourSelect').title = s.tIntentions;
  document.getElementById('btnDiary').title = s.tDiary;
  document.getElementById('btnDiaryFromHourSelect').title = s.tDiary;
  document.getElementById('btnSettings').title = s.tSettings;
  document.getElementById('btnSettingsFromHourSelect').title = s.tSettings;
  document.getElementById('btnBackToHourSelect').title = s.tBack;
  document.getElementById('btnDebug').title = s.tDebug;
  document.getElementById('btnDebugFromHourSelect').title = s.tDebug;
  document.getElementById('btnHymnal').title = s.tHymnal;
  document.getElementById('btnHymnalFromHourSelect').title = s.tHymnal;
  document.getElementById('fontMinus').title = s.tSmaller;
  document.getElementById('fontPlus').title = s.tLarger;
  renderHourCards();
  if (!document.getElementById('settingsScreen').classList.contains('hidden')) renderSettingsScreen();
  if (!document.getElementById('hymnalScreen').classList.contains('hidden')) renderHymnalScreen();
}
['menuLangSelectA', 'menuLangSelectB'].forEach(id => {
  document.getElementById(id).addEventListener('change', e => {
    settings.menuLang = e.target.value; saveSettings();
    syncMenuLangSelects(); refreshChromeText();
  });
});

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
function mdLite(escaped) {
  return escaped
    .replace(/\$([^$]*)\$/g, '<strong>$1</strong>')
    .replace(/_([^_]*)_/g, '<em>$1</em>');
}
function renderUnitContent(unit, lang) {
  const val = unit.content ? unit.content[lang] : null;
  if (val === null || val === undefined) return '<em>[not yet sourced]</em>';
  return mdLite(esc(val)).replace(/\n/g, '<br>');
}

function renderAlignedRows(unit, left, right, single) {
  const isPsalm = (unit.kind === 'psalm');
  const missingLabel = isPsalm ? '[missing]' : '[not yet sourced]';
  const leftRaw = unit.content ? unit.content[left] : null;
  const rightRaw = single ? leftRaw : (unit.content ? unit.content[right] : null);
  const leftEmpty = !leftRaw || leftRaw.length === 0;
  const rightEmpty = !rightRaw || rightRaw.length === 0;

  if (leftEmpty && rightEmpty) {
    return single
      ? `<tr><td class="single"><em>${missingLabel}</em></td></tr>`
      : `<tr><td class="col-left"><em>${missingLabel}</em></td><td class="col-right"><em>${missingLabel}</em></td></tr>`;
  }

  if (!single) {
    var rows = `<tr><td class="col-left"><div class="unit-label">${left.toUpperCase()}</div></td>` +
                `<td class="col-right"><div class="unit-label">${right.toUpperCase()}</div></td></tr>`;
  } else {
    var rows = '';
  }

  if (isPsalm) {
    const leftMap = new Map((leftRaw || []).map(([n, t]) => [String(n), t]));
    const rightMap = new Map((rightRaw || []).map(([n, t]) => [String(n), t]));
    const nums = Array.from(new Set([...leftMap.keys(), ...rightMap.keys()]))
      .sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
    let first = true;
    for (const n of nums) {
      const dc = first ? ' dropcap' : ''; first = false;
      const lt = leftMap.has(n) ? `<span class="vn">${esc(n)}</span> ${esc(leftMap.get(n))}` : '<em>&mdash;</em>';
      if (single) {
        rows += `<tr><td class="single${dc}">${lt}</td></tr>`;
      } else {
        const rt = rightMap.has(n) ? `<span class="vn">${esc(n)}</span> ${esc(rightMap.get(n))}` : '<em>&mdash;</em>';
        rows += `<tr><td class="col-left${dc}">${lt}</td><td class="col-right">${rt}</td></tr>`;
      }
    }
    return rows;
  }

  const maxLen = Math.max(leftRaw ? leftRaw.length : 0, rightRaw ? rightRaw.length : 0);
  for (let i = 0; i < maxLen; i++) {
    const lt = (leftRaw && leftRaw[i] !== undefined) ? mdLite(esc(leftRaw[i])) : '<em>&mdash;</em>';
    if (single) {
      rows += `<tr><td class="single hymn-line">${lt}</td></tr>`;
    } else {
      const rt = (rightRaw && rightRaw[i] !== undefined) ? mdLite(esc(rightRaw[i])) : '<em>&mdash;</em>';
      rows += `<tr><td class="col-left hymn-line">${lt}</td><td class="col-right hymn-line">${rt}</td></tr>`;
    }
  }
  return rows;
}

function renderHymnChoiceRows(unit, left, right) {
  const ctx = unit.hour;
  const pool = (DATA.hymn_pools && DATA.hymn_pools[ctx]) || [];
  const opts = pool
    .filter(h => h.lines[h.original_language] && h.lines[h.original_language].length)
    .map(h => ({ id: h.id, lang: h.original_language, title: h.title }));
  if (opts.length === 0) {
    return `<tr><td colspan="2"><em>[not yet sourced]</em></td></tr>`;
  }
  opts.sort((a, b) => (a.lang === left ? 0 : 1) - (b.lang === left ? 0 : 1));

  // The server picks a recommended hymn per hour based on what kind of day
  // it is (a martyr's, a virgin's, Marian, the Ordinary Time weekday cycle,
  // etc. - see recommend_hymn_id() in render_day.py) - used as the default
  // selection only the first time this hour is shown; once the person picks
  // something themselves (or on any later render), their choice sticks.
  let choiceId = hymnChoiceByHour[ctx];
  if (!choiceId || !opts.some(o => o.id === choiceId)) {
    choiceId = (unit.recommended && opts.some(o => o.id === unit.recommended)) ? unit.recommended : opts[0].id;
    hymnChoiceByHour[ctx] = choiceId;
  }

  let selectHtml = `<select class="hymn-select" data-hour="${esc(ctx)}">`;
  for (const o of opts) {
    const picked = (o.id === choiceId) ? ' selected' : '';
    const recTag = (o.id === unit.recommended) ? ` — ${esc(ui().hymnRecommendedTag)}` : '';
    selectHtml += `<option value="${esc(o.id)}"${picked}>` +
      `${esc(o.title)} (${esc(LANG_NAMES[o.lang] || o.lang)})${recTag}</option>`;
  }
  selectHtml += `</select>`;
  let rows = `<tr><td colspan="2" class="hymn-picker">${selectHtml}</td></tr>`;

  const hymn = pool.find(h => h.id === choiceId);
  const sungLines = hymn.lines[hymn.original_language] || [];
  const translatedLines = hymn.lines[right] || [];
  const single = (hymn.original_language === right);

  if (single) {
    for (const line of sungLines) {
      rows += `<tr><td class="single hymn-line">${esc(line)}</td></tr>`;
    }
  } else if (translatedLines.length === 0) {
    sungLines.forEach((line, i) => {
      const rt = (i === 0) ? '<em>[not yet sourced]</em>' : '';
      rows += `<tr><td class="col-left hymn-line">${esc(line)}</td><td class="col-right hymn-line">${rt}</td></tr>`;
    });
  } else {
    const maxLen = Math.max(sungLines.length, translatedLines.length);
    for (let i = 0; i < maxLen; i++) {
      const lt = sungLines[i] !== undefined ? esc(sungLines[i]) : '';
      const rt = translatedLines[i] !== undefined ? esc(translatedLines[i]) : '';
      rows += `<tr><td class="col-left hymn-line">${lt}</td><td class="col-right hymn-line">${rt}</td></tr>`;
    }
  }
  return rows;
}
function onHymnSelectChange(e) {
  const sel = e.target;
  hymnChoiceByHour[sel.dataset.hour] = sel.value;
  render();
}

// Decorative † / ★ markers next to certain rubric labels - purely cosmetic,
// toggled by the Settings tab's "decorative symbols" switch.
const SYMBOL_BY_LABEL = {
  reading: '†', concluding_prayer: '†', responsory: '★',
  psalm: '★', canticle: '★', intercessions: '†',
};

// Preces (intentions) get the user's own checked Personal Intentions spliced
// in as extra petition lines, right before the Pater Noster - matches the
// real structure of the Hour (intercessions, then the Our Father).
function intentionExtraLines(unit) {
  if (unit.label !== 'intercessions') return null;
  if (!settings.intentionsEnabled) return null; // master toggle, independent of each intention's own checkbox
  const checked = loadIntentions().filter(i => i.checked);
  if (checked.length === 0) return null;
  return checked.map(i => `— ${i.text}.`);
}

// Swaps the Our Father's "daily bread" line (index 4 of static.json's
// our_father arrays) for whichever of the two traditional Latin renderings
// (cotidianum/supersubstantialem - Luke's vs. Matthew's Vulgate translation
// of epiousios) the Settings tab has picked, in every language at once.
// Returns a shallow clone so the original DATA object is never mutated.
function applyPaterNosterBread(unit) {
  if (unit.label !== 'our_father' || !DATA.our_father_bread_variants) return unit;
  const variant = DATA.our_father_bread_variants[settings.paterNosterBread];
  if (!variant) return unit;
  const clone = Object.assign({}, unit, { content: {} });
  for (const lang of Object.keys(unit.content)) {
    const lines = unit.content[lang];
    if (!Array.isArray(lines)) { clone.content[lang] = lines; continue; }
    const newLines = lines.slice();
    if (newLines.length > 4 && variant[lang]) newLines[4] = variant[lang];
    clone.content[lang] = newLines;
  }
  return clone;
}

let currentPages = [['placeholder']]; // rebuilt by render(); each entry is one page's HTML string
let currentPageIndex = 0;

// Fixed, non-date-dependent liturgical formulas - never sourced per-day like
// psalms/readings are, so they live here as plain constants rather than
// flowing through render_day.py.
const GLORIA_PATRI_TEXT = {
  la: 'Glória Patri, et Fílio, et Spirítui Sancto. Sicut erat in princípio, et nunc, et semper, et in sǽcula sæculórum. Amen.',
  es: 'Gloria al Padre, y al Hijo, y al Espíritu Santo. Como era en el principio, ahora y siempre, por los siglos de los siglos. Amén.',
  en: 'Glory be to the Father, and to the Son, and to the Holy Spirit. As it was in the beginning, is now, and ever shall be, world without end. Amen.',
};
const SACRED_SILENCE_LABEL = { la: 'Silentium sacrum', es: 'Silencio sagrado', en: 'Sacred Silence' };

const MARIAN_ANTIPHONS = {
  none: { title: { la: '', es: '', en: '' } },
  alma_redemptoris: {
    title: { la: 'Alma Redemptóris Mater', es: 'Alma Redemptoris Mater', en: 'Alma Redemptoris Mater' },
    text: {
      la: 'Alma Redemptóris Mater, quæ pérvia cæli porta manes, et stella maris, succúrre cadénti, súrgere qui curat pópulo: tu quæ genuísti, natúra miránte, tuum sanctum Genitórem, Virgo prius ac postérius, Gabriélis ab ore sumens illud Ave, peccatórum miserére.',
      es: 'Madre amable del Redentor, puerta del cielo siempre abierta, y estrella del mar: socorre al pueblo que, aun cayendo, se esfuerza por levantarse. Tú que, para asombro de la naturaleza, engendraste a tu santo Creador, Virgen antes y después del parto, y de labios de Gabriel recibiste aquel Ave, ten piedad de los pecadores.',
      en: 'Loving Mother of the Redeemer, gate of heaven, star of the sea, assist your people who have fallen yet strive to rise again. To the wonderment of nature you bore your Creator, yet remained a virgin after as before. You who received Gabriel’s joyful greeting, have mercy on us poor sinners.',
    },
  },
  ave_regina: {
    title: { la: 'Ave, Regína Cælórum', es: 'Ave, Reina de los Cielos', en: 'Hail, Queen of Heaven' },
    text: {
      la: 'Ave, Regína cælórum, Ave, Dómina Angelórum: Salve, radix, salve, porta, Ex qua mundo lux est orta: Gaude, Virgo gloriósa, Super omnes speciósa, Vale, o valde decóra, Et pro nobis Christum exóra.',
      es: 'Salve, Reina de los cielos; salve, Señora de los ángeles; salve, raíz, salve, puerta, por donde vino al mundo la luz. Alégrate, Virgen gloriosa, hermosa entre todas; adiós, oh bellísima, y ruega por nosotros a Cristo.',
      en: 'Hail, Queen of Heaven; hail, Lady of the Angels; hail, root of Jesse, hail, gate of Heaven, through whom the light of the world has arisen. Rejoice, glorious Virgin, lovely beyond all others; farewell, most beautiful of all, and pray for us to Christ.',
    },
  },
  regina_caeli: {
    title: { la: 'Regína Cæli', es: 'Reina del Cielo', en: 'Queen of Heaven' },
    text: {
      la: 'Regína cæli, lætáre, allelúia: Quia quem meruísti portáre, allelúia: Resurréxit, sicut dixit, allelúia: Ora pro nobis Deum, allelúia.',
      es: 'Reina del cielo, alégrate, aleluya; porque el Señor, a quien mereciste llevar en tu seno, aleluya, ha resucitado según predijo, aleluya; ruega al Señor por nosotros, aleluya.',
      en: 'Queen of Heaven, rejoice, alleluia. For he whom you were worthy to bear, alleluia, has risen as he said, alleluia. Pray for us to God, alleluia.',
    },
  },
  salve_regina: {
    title: { la: 'Salve, Regína', es: 'Salve, Reina', en: 'Hail, Holy Queen' },
    text: {
      la: 'Salve, Regína, mater misericórdiæ, vita, dulcédo, et spes nostra, salve. Ad te clamámus éxsules fílii Hevæ. Ad te suspirámus geméntes et flentes in hac lacrimárum valle. Eia ergo, advocáta nostra, illos tuos misericórdes óculos ad nos convérte. Et Iesum benedíctum fructum ventris tui, nobis post hoc exsílium osténde. O clemens, o pia, o dulcis Virgo María.',
      es: 'Dios te salve, Reina y Madre de misericordia, vida, dulzura y esperanza nuestra; Dios te salve. A ti llamamos los desterrados hijos de Eva; a ti suspiramos, gimiendo y llorando en este valle de lágrimas. Ea, pues, Señora, abogada nuestra, vuelve a nosotros esos tus ojos misericordiosos; y después de este destierro muéstranos a Jesús, fruto bendito de tu vientre. ¡Oh clementísima, oh piadosa, oh dulce siempre Virgen María!',
      en: 'Hail, Holy Queen, Mother of Mercy, our life, our sweetness, and our hope. To thee do we cry, poor banished children of Eve. To thee do we send up our sighs, mourning and weeping in this valley of tears. Turn then, most gracious advocate, thine eyes of mercy toward us, and after this our exile, show unto us the blessed fruit of thy womb, Jesus. O clement, O loving, O sweet Virgin Mary.',
    },
  },
};

function renderFixedBilingualRow(textObj, uLeft, uRight, single, rowClass) {
  const left = textObj[uLeft] || textObj.en || '';
  const right = single ? left : (textObj[uRight] || textObj.en || '');
  if (single) {
    return `<tr class="${rowClass}"><td class="single">${esc(left)}</td></tr>`;
  }
  return `<tr class="${rowClass}"><td class="col-left">${esc(left)}</td><td class="col-right">${esc(right)}</td></tr>`;
}

function render() {
  const dayData = currentDayData();
  if (!dayData) return;
  let intentionCellCounter = 0;
  const pendingIntentionCells = []; // {id, lang, text} - translated in place once the table is in the DOM
  let left = leftSel.value, right = rightSel.value;
  const hour = hourSel.value;

  if (settings.bilingualMode === 'latinOnly') { left = 'la'; right = 'la'; }
  else if (settings.bilingualMode === 'vernacularOnly') {
    const vern = DATA.languages.find(l => l !== 'la') || DATA.languages[0];
    left = vern; right = vern;
  }
  const single = (left === right);

  document.getElementById('dateHeading').innerHTML = dayData.day_description[left] || dayData.day_description.en;
  document.getElementById('metaLine').textContent = (dayData.date_human[left] || dayData.date_human.en);

  const units = dayData.hours[hour] || [];
  const labels = DATA.unit_labels[left] || DATA.unit_labels.en;
  let html = '';
  let firstUnit = true;
  for (const unit of units) {
    let labelText = labels[unit.label] || unit.label;
    if (unit.repeated) labelText += ' ' + (labels.repeated || '');
    if (unit.ref) labelText += ` (${esc(unit.ref)})`;
    const symbol = SYMBOL_BY_LABEL[unit.label] ? `<span class="section-symbol">${SYMBOL_BY_LABEL[unit.label]}</span>` : '';
    const dividerClass = (!firstUnit) ? ' unit-divider' : '';
    firstUnit = false;

    // Beta English isn't real stored content for most units (DATA.languages
    // stays ['la','es']) - it's a live translation of the Spanish text laid
    // over the same structure. A handful of universal, invariant texts
    // (static.json's Deus in Adiutorium, Our Father, Compline's fixed
    // formulas) DO carry genuine sourced English though - unit.content.en
    // is only ever present for those, so its mere presence is what decides
    // whether this unit needs live translation at all. left/right (kept as
    // 'en' throughout) still drive the visible "EN" label and the
    // single/two-column layout decision above.
    const unitHasRealEnglish = !!(unit.content && unit.content.en !== undefined && unit.content.en !== null);
    const uLeft = (left === 'en') ? (unitHasRealEnglish ? 'en' : 'es') : left;
    const uRight = (right === 'en') ? (unitHasRealEnglish ? 'en' : 'es') : right;
    const mtSkip = (left === 'en' || right === 'en') ? (unitHasRealEnglish ? '1' : '0') : '1';

    html += `<tr class="unit-header${dividerClass}" data-mt-skip="${mtSkip}"><th colspan="2">${symbol}${esc(labelText)}${symbol}</th></tr>`;
    if (unit.label === 'psalmody_gap') {
      html += `<tr><td colspan="2"><em>${esc(labels.psalmody_gap_note || labels.missing)}</em></td></tr>`;
    } else if (unit.label === 'vespers_omitted_holy_saturday') {
      html += `<tr><td colspan="2"><em>${esc(labels.vespers_omitted_holy_saturday_note || labels.missing)}</em></td></tr>`;
    } else if (unit.kind === 'psalm' || unit.kind === 'lines') {
      html += renderAlignedRows(applyPaterNosterBread(unit), uLeft, uRight, single);
      const extra = intentionExtraLines(unit);
      if (extra) {
        for (const line of extra) {
          const idL = 'intent-cell-' + (intentionCellCounter++);
          if (single) {
            html += `<tr><td class="single hymn-line" id="${idL}">${esc(line)}</td></tr>`;
            pendingIntentionCells.push({ id: idL, lang: uLeft, text: line });
          } else {
            const idR = 'intent-cell-' + (intentionCellCounter++);
            html += `<tr><td class="col-left hymn-line" id="${idL}">${esc(line)}</td>` +
                    `<td class="col-right hymn-line" id="${idR}"></td></tr>`;
            pendingIntentionCells.push({ id: idL, lang: uLeft, text: line });
            pendingIntentionCells.push({ id: idR, lang: uRight, text: line });
          }
        }
      }
      // A real psalm or canticle (not the verse-numbered short reading,
      // which also happens to use kind:"psalm" for its line formatting)
      // traditionally closes with the Gloria Patri, before its antiphon
      // is repeated - settings.showGloriaPatri makes that optional.
      if (unit.kind === 'psalm' && unit.label !== 'reading' && settings.showGloriaPatri) {
        html += renderFixedBilingualRow(GLORIA_PATRI_TEXT, uLeft, uRight, single, 'gloria-patri-row');
      }
      if (unit.label === 'reading' && settings.sacredSilence) {
        html += renderFixedBilingualRow(SACRED_SILENCE_LABEL, uLeft, uRight, single, 'sacred-silence-row');
      }
    } else if (unit.kind === 'hymn_choice') {
      html += renderHymnChoiceRows(unit, uLeft, uRight);
    } else if (single) {
      html += `<tr><td class="single dropcap">${renderUnitContent(unit, uLeft)}</td></tr>`;
      if (unit.label === 'reading' && settings.sacredSilence) {
        html += renderFixedBilingualRow(SACRED_SILENCE_LABEL, uLeft, uRight, single, 'sacred-silence-row');
      }
    } else {
      html += `<tr><td class="col-left dropcap"><div class="unit-label">${left.toUpperCase()}</div>${renderUnitContent(unit, uLeft)}</td>` +
              `<td class="col-right"><div class="unit-label">${right.toUpperCase()}</div>${renderUnitContent(unit, uRight)}</td></tr>`;
      if (unit.label === 'reading' && settings.sacredSilence) {
        html += renderFixedBilingualRow(SACRED_SILENCE_LABEL, uLeft, uRight, single, 'sacred-silence-row');
      }
    }
  }

  // Marian antiphon (Salve Regina and its seasonal siblings) is a fixed
  // closing devotion, traditionally added after Night Prayer's own
  // dismissal - not part of any day's sourced content, so it's appended
  // here client-side rather than flowing through render_day.py.
  if (hour === 'compline' && settings.marianAntiphonEnabled && settings.marianAntiphonChoice !== 'none') {
    const ant = MARIAN_ANTIPHONS[settings.marianAntiphonChoice];
    if (ant && ant.text) {
      const uLeft = (left === 'en') ? 'es' : left;
      const uRight = (right === 'en') ? 'es' : right;
      const titleText = ant.title[uLeft] || ant.title.en;
      html += `<tr class="unit-header unit-divider"><th colspan="2">${esc(titleText)}</th></tr>`;
      html += renderFixedBilingualRow(ant.text, uLeft, uRight, single, 'marian-antiphon-row');
    }
  }

  const table = document.getElementById('mainTable');
  table.innerHTML = html;
  table.querySelectorAll('.hymn-select').forEach(sel => sel.addEventListener('change', onHymnSelectChange));
  // Only the very first content cell of the hour gets a drop cap (a whole
  // hour's worth of drop caps would be visual noise, not an ornament).
  const dcs = table.querySelectorAll('.dropcap');
  dcs.forEach((el, i) => { if (i > 0) el.classList.remove('dropcap'); });

  if (left === 'en' || right === 'en') {
    applyBetaEnglishTranslation(table, left === 'en', right === 'en');
  }
  applyIntentionTranslations(pendingIntentionCells);

  setupPaging(table);
}

// Each Personal Intention line is entered once by the person praying, then
// shown translated into whichever language(s) the Preces column(s) are
// actually displaying (see translateIntentionFor) - a cell is patched in
// place once its translation resolves, exactly like the beta-English pass.
function applyIntentionTranslations(pending) {
  pending.forEach(({ id, lang, text }) => {
    const cell = document.getElementById(id);
    if (!cell) return;
    if (lang === 'en') { cell.textContent = text; return; } // assumed-source language, nothing to translate
    cell.classList.add('mt-pending');
    translateIntentionFor(text, lang).then(translated => {
      cell.classList.remove('mt-pending');
      cell.innerHTML = mdLite(esc(translated));
    });
  });
}

// "Paged" reading mode chunks the already-rendered table rows into pages by
// unit-header boundary (never splitting a unit's own rows across pages) and
// shows one page at a time with Prev/Next controls + the ribbon bookmark.
function setupPaging(table) {
  const allRows = Array.from(table.querySelectorAll('tr'));
  const pages = [];
  let current = [];
  for (const row of allRows) {
    if (row.classList.contains('unit-header') && current.length > 0 && current.length >= 6) {
      pages.push(current);
      current = [];
    }
    current.push(row);
  }
  if (current.length) pages.push(current);
  currentPages = pages.length ? pages : [allRows];
  currentPageIndex = 0;
  applyPaging();
}
function applyPaging() {
  const table = document.getElementById('mainTable');
  const allRows = Array.from(table.querySelectorAll('tr'));
  allRows.forEach(r => r.style.display = '');
  if (settings.readingMode !== 'paged') {
    updatePagerIndicator();
    return;
  }
  const activeRows = new Set(currentPages[currentPageIndex] || []);
  allRows.forEach(r => { r.style.display = activeRows.has(r) ? '' : 'none'; });
  updatePagerIndicator();
}
function updatePagerIndicator() {
  const total = currentPages.length;
  const text = `Page ${currentPageIndex + 1} of ${total}`;
  ['pagerIndicator', 'pagerIndicatorBottom'].forEach(id => {
    const el = document.getElementById(id); if (el) el.textContent = text;
  });
  ['pagerPrev', 'pagerPrevBottom'].forEach(id => {
    const el = document.getElementById(id); if (el) el.disabled = (currentPageIndex === 0);
  });
  ['pagerNext', 'pagerNextBottom'].forEach(id => {
    const el = document.getElementById(id); if (el) el.disabled = (currentPageIndex >= currentPages.length - 1);
  });
}
function pagerGo(delta) {
  currentPageIndex = Math.max(0, Math.min(currentPages.length - 1, currentPageIndex + delta));
  applyPaging();
  document.querySelector('.content-wrap').scrollIntoView({ behavior: 'smooth', block: 'start' });
}
['pagerPrev', 'pagerPrevBottom'].forEach(id => document.getElementById(id).addEventListener('click', () => pagerGo(-1)));
['pagerNext', 'pagerNextBottom'].forEach(id => document.getElementById(id).addEventListener('click', () => pagerGo(1)));

leftSel.addEventListener('change', render);
rightSel.addEventListener('change', () => { render(); saveLastPosition(); });
hourSel.addEventListener('change', () => { render(); saveLastPosition(); });
dateSel.addEventListener('change', () => { render(); renderHero(); saveLastPosition(); });

/* ============================================================
   QUICK FONT NUDGE
   ============================================================ */
document.getElementById('fontMinus').addEventListener('click', () => {
  settings.fontSizeMain = Math.max(12, settings.fontSizeMain - 1);
  settings.fontSizeLatin = Math.max(12, settings.fontSizeLatin - 1);
  saveSettings(); applySettingsToDOM();
});
document.getElementById('fontPlus').addEventListener('click', () => {
  settings.fontSizeMain = Math.min(32, settings.fontSizeMain + 1);
  settings.fontSizeLatin = Math.min(32, settings.fontSizeLatin + 1);
  saveSettings(); applySettingsToDOM();
});

/* ============================================================
   INTENTIONS DRAWER
   ============================================================ */
function loadIntentions() {
  try { return JSON.parse(localStorage.getItem(INTENTIONS_KEY) || '[]'); } catch (e) { return []; }
}
function saveIntentions(list) {
  try { localStorage.setItem(INTENTIONS_KEY, JSON.stringify(list)); } catch (e) { /* storage unavailable */ }
}
function openIntentionsDrawer() {
  closeDrawers();
  const s = ui();
  const backdrop = document.createElement('div');
  backdrop.className = 'drawer-backdrop'; backdrop.id = 'drawerBackdrop';
  backdrop.addEventListener('click', closeDrawers);
  document.body.appendChild(backdrop);

  const drawer = document.createElement('div');
  drawer.className = 'drawer'; drawer.id = 'activeDrawer';
  drawer.innerHTML = `
    <div class="drawer-header"><h3>${esc(s.intentionsTitle)}</h3><button class="icon-btn" id="closeDrawerBtn">&times;</button></div>
    <div class="drawer-body">
      <div class="settings-row">
        <label for="intentionsMasterToggle">${esc(s.intentionsMasterToggle)}</label>
        <div class="settings-control">${toggleHtml('intentionsMasterToggle', settings.intentionsEnabled)}</div>
      </div>
      <p class="settings-hint">${esc(s.intentionsHint)}</p>
      <div id="intentionsList"></div>
      <div class="add-intention-row">
        <input type="text" id="newIntentionInput" placeholder="${esc(s.intentionsPlaceholder)}">
        <button id="addIntentionBtn">${esc(s.addBtn)}</button>
      </div>
    </div>`;
  document.body.appendChild(drawer);
  document.getElementById('closeDrawerBtn').addEventListener('click', closeDrawers);
  document.getElementById('intentionsMasterToggle').addEventListener('change', (e) => {
    settings.intentionsEnabled = e.target.checked; saveSettings(); render();
  });
  renderIntentionsList();
  document.getElementById('addIntentionBtn').addEventListener('click', addIntention);
  document.getElementById('newIntentionInput').addEventListener('keydown', e => { if (e.key === 'Enter') addIntention(); });
}
function renderIntentionsList() {
  const list = loadIntentions();
  const el = document.getElementById('intentionsList');
  if (!el) return;
  if (list.length === 0) {
    el.innerHTML = `<p class="settings-hint">${esc(ui().intentionsEmpty)}</p>`;
    return;
  }
  el.innerHTML = list.map((it, i) => `
    <div class="intention-item">
      <input type="checkbox" data-i="${i}" ${it.checked ? 'checked' : ''}>
      <span class="intention-text">${esc(it.text)}</span>
      <button data-del="${i}" title="Remove">&times;</button>
    </div>`).join('');
  el.querySelectorAll('input[type=checkbox]').forEach(cb => cb.addEventListener('change', () => {
    const l = loadIntentions(); l[+cb.dataset.i].checked = cb.checked; saveIntentions(l); render();
  }));
  el.querySelectorAll('button[data-del]').forEach(btn => btn.addEventListener('click', () => {
    const l = loadIntentions(); l.splice(+btn.dataset.del, 1); saveIntentions(l); renderIntentionsList(); render();
  }));
}
function addIntention() {
  const input = document.getElementById('newIntentionInput');
  const text = input.value.trim();
  if (!text) return;
  const l = loadIntentions(); l.push({ text, checked: true }); saveIntentions(l);
  input.value = ''; renderIntentionsList(); render();
}

/* ============================================================
   HYMNAL SCREEN - browse/search/filter the full hymn library
   (official content/proper_texts/hymns.json entries + personal ones
   from loadUserHymns()), and a form to add your own. DATA.hymn_pools
   (grouped by hour, see poolsFromRawHymns/mergeUserHymnsIntoPools) is
   the source of truth; this screen just re-flattens it back to one
   list per hymn (recovering which hours each id applies to) since
   browsing/searching cuts across hours rather than picking one.
   ============================================================ */
let hymnalFilters = { search: '', hour: '', langCount: 'all' };
const hymnalExpanded = new Set();

const ALL_HOURS_ORDER_JS = DATA.hour_order || ['office_of_readings', 'lauds', 'terce', 'sext', 'none_hour', 'vespers', 'compline'];
function stripDiacritics(s) {
  return (s || '').normalize('NFD').replace(new RegExp('[\\u0300-\\u036f]', 'g'), '');
}
function hourLabel(hour) {
  const labels = (DATA.hour_labels && DATA.hour_labels[settings.menuLang]) || {};
  return labels[hour] || (hour.charAt(0).toUpperCase() + hour.slice(1).replace(/_/g, ' '));
}
function allHymnEntries() {
  const byId = new Map();
  for (const [hour, pool] of Object.entries(DATA.hymn_pools || {})) {
    for (const h of pool) {
      if (!byId.has(h.id)) byId.set(h.id, Object.assign({}, h, { hours: [] }));
      byId.get(h.id).hours.push(hour);
    }
  }
  return Array.from(byId.values()).sort((a, b) => a.title.localeCompare(b.title));
}
function hymnSungLangCount(h) {
  // "Multi-language" means the hymn genuinely has more than one SUNG
  // version (a separately-attested original setting in each language),
  // not merely that a translation exists for following along. Every
  // official hymn today is single-language by this definition - Spanish
  // is a comprehension translation of the Latin original, not a second
  // sung version - see also_sung_in's doc in build_hymn_pools()
  // (render_day.py). original_language always counts as one sung
  // language; also_sung_in lists any additional ones.
  return 1 + (h.also_sung_in || []).length;
}
function filteredHymnEntries() {
  const q = stripDiacritics(hymnalFilters.search.toLowerCase()).trim();
  return allHymnEntries().filter(h => {
    if (hymnalFilters.hour && !h.hours.includes(hymnalFilters.hour)) return false;
    const sungCount = hymnSungLangCount(h);
    if (hymnalFilters.langCount === 'multi' && sungCount < 2) return false;
    if (hymnalFilters.langCount === 'single' && sungCount !== 1) return false;
    if (!q) return true;
    const firstLine = Object.values(h.lines || {}).flat().find(l => l && l.trim()) || '';
    const haystack = stripDiacritics((h.title + ' ' + firstLine).toLowerCase());
    return haystack.includes(q);
  });
}

function renderHymnalScreen() {
  const s = ui();
  const body = document.getElementById('hymnalBody');
  document.getElementById('hymnalTitle').textContent = s.hymnalTitle;
  const hours = ALL_HOURS_ORDER_JS.filter(h => (DATA.hymn_pools || {})[h] && DATA.hymn_pools[h].length);
  body.innerHTML = `
    <p class="settings-hint">${esc(s.hymnalLocalNotice)}</p>
    <div class="hymnal-controls">
      <input type="text" id="hymnalSearch" placeholder="${esc(s.hymnalSearchPlaceholder)}" value="${esc(hymnalFilters.search)}">
      <select id="hymnalHourFilter">
        <option value="">${esc(s.hymnalFilterAllHours)}</option>
        ${hours.map(h => `<option value="${esc(h)}"${h === hymnalFilters.hour ? ' selected' : ''}>${esc(hourLabel(h))}</option>`).join('')}
      </select>
      <select id="hymnalLangFilter">
        <option value="all"${hymnalFilters.langCount === 'all' ? ' selected' : ''}>${esc(s.hymnalFilterAllLangs)}</option>
        <option value="multi"${hymnalFilters.langCount === 'multi' ? ' selected' : ''}>${esc(s.hymnalFilterMultiLang)}</option>
        <option value="single"${hymnalFilters.langCount === 'single' ? ' selected' : ''}>${esc(s.hymnalFilterSingleLang)}</option>
      </select>
      <button id="hymnalAddToggleBtn">${esc(s.hymnalAddBtn)}</button>
    </div>
    <p class="settings-hint">${esc(s.hymnalLangFilterHint)}</p>
    <div id="hymnalAddFormWrap"></div>
    <div id="hymnalCount" class="settings-hint"></div>
    <div id="hymnalList" class="hymnal-list"></div>`;

  document.getElementById('hymnalSearch').addEventListener('input', e => {
    hymnalFilters.search = e.target.value; renderHymnalList();
  });
  document.getElementById('hymnalHourFilter').addEventListener('change', e => {
    hymnalFilters.hour = e.target.value; renderHymnalList();
  });
  document.getElementById('hymnalLangFilter').addEventListener('change', e => {
    hymnalFilters.langCount = e.target.value; renderHymnalList();
  });
  document.getElementById('hymnalAddToggleBtn').addEventListener('click', toggleHymnalAddForm);

  renderHymnalList();
}

function renderHymnalList() {
  const s = ui();
  const listEl = document.getElementById('hymnalList');
  const countEl = document.getElementById('hymnalCount');
  if (!listEl) return;
  const entries = filteredHymnEntries();
  countEl.textContent = s.hymnalCount(entries.length);
  if (entries.length === 0) {
    listEl.innerHTML = `<p class="settings-hint">${esc(s.hymnalEmpty)}</p>`;
    return;
  }
  listEl.innerHTML = entries.map(h => {
    const expanded = hymnalExpanded.has(h.id);
    const badge = h.user_added
      ? `<span class="hymnal-badge hymnal-badge-mine">${esc(s.hymnalUserBadge)}</span>`
      : `<span class="hymnal-badge">${esc(s.hymnalOfficialBadge)}</span>`;
    const hourBadges = h.hours.map(hh => `<span class="hymnal-hour-badge">${esc(hourLabel(hh))}</span>`).join('');
    const langNames = Object.keys(h.lines || {}).filter(l => h.lines[l] && h.lines[l].some(x => x.trim()));
    let lyricsHtml = '';
    if (expanded) {
      const sungLangs = new Set([h.original_language, ...(h.also_sung_in || [])]);
      lyricsHtml = `<div class="hymnal-lyrics">${langNames.map(lang => `
        <div class="hymnal-lyrics-col">
          <div class="hymnal-lyrics-lang">${esc(LANG_NAMES[lang] || lang.toUpperCase())}${sungLangs.has(lang) ? ' &#9835;' : ''}</div>
          ${h.lines[lang].map(line => line.trim() ? `<div class="hymn-line">${esc(line)}</div>` : `<div class="hymnal-stanza-break"></div>`).join('')}
        </div>`).join('')}</div>`;
    }
    const deleteBtn = h.user_added
      ? `<button class="hymnal-del-btn" data-del="${esc(h.id)}" title="${esc(s.hymnalDeleteBtn)}">&times;</button>` : '';
    return `
      <div class="hymnal-card">
        <div class="hymnal-card-header">
          <div class="hymnal-card-title">${esc(h.title)} ${badge}</div>
          <div class="hymnal-card-hours">${hourBadges}</div>
          <button class="hymnal-toggle-btn" data-toggle="${esc(h.id)}">${expanded ? esc(s.hymnalHideLyrics) : esc(s.hymnalViewLyrics)}</button>
          ${deleteBtn}
        </div>
        ${lyricsHtml}
      </div>`;
  }).join('');

  listEl.querySelectorAll('button[data-toggle]').forEach(btn => btn.addEventListener('click', () => {
    const id = btn.dataset.toggle;
    if (hymnalExpanded.has(id)) hymnalExpanded.delete(id); else hymnalExpanded.add(id);
    renderHymnalList();
  }));
  listEl.querySelectorAll('button[data-del]').forEach(btn => btn.addEventListener('click', () => {
    if (!confirm(ui().hymnalDeleteConfirm)) return;
    const id = btn.dataset.del;
    saveUserHymns(loadUserHymns().filter(h => h.id !== id));
    mergeUserHymnsIntoPools();
    renderHymnalList();
  }));
}

let hymnalAddFormOpen = false;
function toggleHymnalAddForm() {
  hymnalAddFormOpen = !hymnalAddFormOpen;
  renderHymnalAddForm();
}
function renderHymnalAddForm() {
  const s = ui();
  const wrap = document.getElementById('hymnalAddFormWrap');
  if (!wrap) return;
  if (!hymnalAddFormOpen) { wrap.innerHTML = ''; return; }
  wrap.innerHTML = `
    <div class="hymnal-add-form">
      <h3>${esc(s.hymnalAddFormTitle)}</h3>
      <label>${esc(s.hymnalFieldTitle)}
        <input type="text" id="hymnalNewTitle">
      </label>
      <fieldset class="hymnal-hours-fieldset">
        <legend>${esc(s.hymnalFieldHours)}</legend>
        ${ALL_HOURS_ORDER_JS.map(h => `
          <label class="hymnal-hour-check"><input type="checkbox" value="${esc(h)}"> ${esc(hourLabel(h))}</label>`).join('')}
      </fieldset>
      <label>${esc(s.hymnalFieldOriginalLang)}
        <select id="hymnalNewOrigLang">
          ${DATA.languages.map(l => `<option value="${esc(l)}">${esc(LANG_NAMES[l] || l)}</option>`).join('')}
        </select>
      </label>
      ${DATA.languages.map(l => `
        <label>${esc(s.hymnalFieldLyricsFor(LANG_NAMES[l] || l))}
          <textarea id="hymnalNewLyrics_${esc(l)}" rows="6"></textarea>
        </label>
        <label class="hymnal-hour-check" data-also-sung-for="${esc(l)}">
          <input type="checkbox" id="hymnalAlsoSung_${esc(l)}"> ${esc(s.hymnalAlsoSungLabel)}
        </label>`).join('')}
      <p class="settings-hint">${esc(s.hymnalLyricsHint)}</p>
      <div class="hymnal-add-form-actions">
        <button id="hymnalSaveBtn">${esc(s.hymnalSaveBtn)}</button>
        <button id="hymnalCancelBtn">${esc(s.hymnalCancelBtn)}</button>
      </div>
    </div>`;
  document.getElementById('hymnalCancelBtn').addEventListener('click', () => { hymnalAddFormOpen = false; renderHymnalAddForm(); });
  document.getElementById('hymnalSaveBtn').addEventListener('click', saveNewHymn);
}
function saveNewHymn() {
  const s = ui();
  const title = document.getElementById('hymnalNewTitle').value.trim();
  if (!title) { alert(s.hymnalTitleRequired); return; }
  const applicability = Array.from(document.querySelectorAll('.hymnal-hours-fieldset input:checked')).map(cb => cb.value);
  if (applicability.length === 0) { alert(s.hymnalHoursRequired); return; }
  const original_language = document.getElementById('hymnalNewOrigLang').value;
  const lines = {};
  const also_sung_in = [];
  let anyLyrics = false;
  for (const l of DATA.languages) {
    const raw = document.getElementById('hymnalNewLyrics_' + l).value;
    const arr = raw.split('\n').map(x => x.replace(/\r$/, ''));
    while (arr.length && arr[arr.length - 1].trim() === '') arr.pop();
    const hasText = arr.some(x => x.trim());
    if (hasText) anyLyrics = true;
    lines[l] = arr;
    // The original language is always "sung" by definition, so its own
    // checkbox (if checked) is redundant - only additional languages count.
    const alsoSungCb = document.getElementById('hymnalAlsoSung_' + l);
    if (l !== original_language && hasText && alsoSungCb && alsoSungCb.checked) also_sung_in.push(l);
  }
  if (!anyLyrics) { alert(s.hymnalLyricsRequired); return; }
  const list = loadUserHymns();
  list.push({
    id: 'user_' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
    title, applicability, lines, original_language, also_sung_in, user_added: true, date_added: new Date().toISOString(),
  });
  saveUserHymns(list);
  mergeUserHymnsIntoPools();
  hymnalAddFormOpen = false;
  renderHymnalAddForm();
  renderHymnalList();
}

/* ============================================================
   PRAYER DIARY (streak, prayed-today, journal, bookmarks)
   ============================================================ */
function loadDiary() {
  try { return JSON.parse(localStorage.getItem(DIARY_KEY) || '{"days":{},"bookmarks":[]}'); }
  catch (e) { return { days: {}, bookmarks: [] }; }
}
function saveDiary(d) {
  try { localStorage.setItem(DIARY_KEY, JSON.stringify(d)); } catch (e) { /* storage unavailable */ }
}
function todayKey() { return isoDateInTimeZone(browserTz); }
function computeStreak(diary) {
  let streak = 0;
  let d = new Date();
  for (;;) {
    const key = new Intl.DateTimeFormat('en-CA', { year: 'numeric', month: '2-digit', day: '2-digit' }).format(d);
    if (diary.days[key] && diary.days[key].prayed) { streak++; d.setDate(d.getDate() - 1); }
    else break;
  }
  return streak;
}
function openDiaryDrawer() {
  closeDrawers();
  const s = ui();
  const diary = loadDiary();
  const key = todayKey();
  const entry = diary.days[key] || { prayed: false, note: '' };
  const streak = computeStreak(diary);

  const backdrop = document.createElement('div');
  backdrop.className = 'drawer-backdrop'; backdrop.id = 'drawerBackdrop';
  backdrop.addEventListener('click', closeDrawers);
  document.body.appendChild(backdrop);

  const drawer = document.createElement('div');
  drawer.className = 'drawer'; drawer.id = 'activeDrawer';
  drawer.innerHTML = `
    <div class="drawer-header"><h3>${esc(s.diaryTitle)}</h3><button class="icon-btn" id="closeDrawerBtn">&times;</button></div>
    <div class="drawer-body">
      <div class="diary-streak">
        <div class="streak-num">${streak}</div>
        <div class="streak-label">${esc(s.streakLabel(streak))}</div>
      </div>
      <button class="diary-prayed-btn${entry.prayed ? ' done' : ''}" id="markPrayedBtn">
        ${entry.prayed ? esc(s.prayedDone) : esc(s.markPrayed)}
      </button>
      <div class="diary-journal">
        <label class="settings-hint" for="diaryNote">${esc(s.diaryNoteLabel)}</label>
        <textarea id="diaryNote" placeholder="${esc(s.diaryNotePlaceholder)}">${esc(entry.note || '')}</textarea>
      </div>
      <h3 style="margin-top:1.2rem;">${esc(s.bookmarksHeading)}</h3>
      <div class="diary-bookmarks-list" id="bookmarksList"></div>
    </div>`;
  document.body.appendChild(drawer);
  document.getElementById('closeDrawerBtn').addEventListener('click', closeDrawers);

  document.getElementById('markPrayedBtn').addEventListener('click', () => {
    const d = loadDiary();
    const e = d.days[key] || { prayed: false, note: '' };
    e.prayed = !e.prayed;
    d.days[key] = e;
    saveDiary(d);
    openDiaryDrawer(); // re-render with the new streak/state
  });
  document.getElementById('diaryNote').addEventListener('blur', (e) => {
    const d = loadDiary();
    const day = d.days[key] || { prayed: false, note: '' };
    day.note = e.target.value;
    d.days[key] = day;
    saveDiary(d);
  });
  renderBookmarksList();
}
function renderBookmarksList() {
  const diary = loadDiary();
  const el = document.getElementById('bookmarksList');
  if (!el) return;
  if (!diary.bookmarks || diary.bookmarks.length === 0) {
    el.innerHTML = `<p class="settings-hint">${esc(ui().bookmarksEmpty)}</p>`;
    return;
  }
  el.innerHTML = diary.bookmarks.map((b, i) =>
    `<div class="bm-item"><span>${esc(b)}</span><button data-bm="${i}">&times;</button></div>`).join('');
  el.querySelectorAll('button[data-bm]').forEach(btn => btn.addEventListener('click', () => {
    const d = loadDiary(); d.bookmarks.splice(+btn.dataset.bm, 1); saveDiary(d); renderBookmarksList();
  }));
}

function closeDrawers() {
  const b = document.getElementById('drawerBackdrop'); if (b) b.remove();
  const d = document.getElementById('activeDrawer'); if (d) d.remove();
}

/* ============================================================
   SETTINGS SCREEN (builds every control into #settingsBody)
   ============================================================ */
function toggleHtml(id, checked) {
  return `<label class="toggle"><input type="checkbox" id="${id}" ${checked ? 'checked' : ''}>
    <span class="track"></span><span class="thumb"></span></label>`;
}

// A live "what will this actually look like" panel, kept in the Settings
// screen itself so a change is visible without leaving to check the real
// page. Reuses the exact same rendering functions and CSS classes as the
// main prayer table (renderUnitContent/renderAlignedRows) - every color,
// font, size, drop-cap style, divider, and symbol toggle that touches those
// classes takes effect automatically via the cascading CSS variables /
// body classes render() already sets; only the bilingual-column layout
// needs the preview to be rebuilt explicitly (see wireSettingsControls).
function renderSettingsPreview() {
  const el = document.getElementById('settingsPreview');
  if (!el) return;
  const dayData = currentDayData();
  if (!dayData) { el.innerHTML = ''; return; }
  const vespers = dayData.hours.vespers || [];
  const deusUnit = vespers.find(u => u.label === 'deus');
  const ofUnit = vespers.find(u => u.label === 'our_father');
  const psalmUnit = vespers.find(u => u.kind === 'psalm');

  let pLeft = 'la', pRight = 'es', pSingle = false;
  if (settings.bilingualMode === 'latinOnly') { pLeft = 'la'; pRight = 'la'; pSingle = true; }
  else if (settings.bilingualMode === 'vernacularOnly') { pLeft = 'es'; pRight = 'es'; pSingle = true; }

  const sectionRow = (label, first) =>
    `<tr class="unit-header${first ? '' : ' unit-divider'}" data-mt-skip="1"><th colspan="2"><span class="section-symbol">†</span>${esc(label)}<span class="section-symbol">†</span></th></tr>`;

  let html = `<p class="settings-preview-label">Live Preview</p><table class="preview-table">`;
  if (deusUnit) {
    html += sectionRow('Deus in Adiutorium', true);
    html += pSingle
      ? `<tr><td class="single dropcap">${renderUnitContent(deusUnit, pLeft)}</td></tr>`
      : `<tr><td class="col-left dropcap"><div class="unit-label">${pLeft.toUpperCase()}</div>${renderUnitContent(deusUnit, pLeft)}</td>` +
        `<td class="col-right"><div class="unit-label">${pRight.toUpperCase()}</div>${renderUnitContent(deusUnit, pRight)}</td></tr>`;
  }
  if (psalmUnit) {
    html += sectionRow('Psalmus', false);
    html += renderAlignedRows(psalmUnit, pLeft, pRight, pSingle);
  }
  if (ofUnit) {
    html += sectionRow('Pater Noster', false);
    html += renderAlignedRows(applyPaterNosterBread(ofUnit), pLeft, pRight, pSingle);
  }
  html += `</table>`;
  el.innerHTML = html;
  const dcs = el.querySelectorAll('.dropcap');
  dcs.forEach((cell, i) => { if (i > 0) cell.classList.remove('dropcap'); });
}
function renderSettingsScreen() {
  const s = ui();
  const body = document.getElementById('settingsBody');
  document.getElementById('settingsTitle').textContent = s.settingsTitle;
  body.innerHTML = `
    <div class="settings-group-heading">${s.secGroupAesthetics}</div>

    <div class="settings-section">
      <h3>${s.secPresets}</h3>
      <div class="preset-grid" id="presetGrid"></div>
    </div>

    <div class="settings-section">
      <h3>${s.secColorSync}</h3>
      <div class="settings-row">
        <label for="syncColor">${s.syncLabel}</label>
        <div class="settings-control">${toggleHtml('syncColor', settings.liturgicalColorSync)}</div>
      </div>
      <p class="settings-hint">${s.syncHint}</p>
    </div>

    <div class="settings-section">
      <h3>${s.secTypography}</h3>
      <div class="settings-row"><label>${s.menuLangLabel}</label>
        <div class="settings-control"><select id="menuLangSelectSettings"></select></div></div>
      <div class="settings-row stacked"><label>${s.fontMainLabel}</label><div class="settings-control" id="fontMainRow"></div></div>
      <div class="settings-row stacked"><label>${s.fontRubricLabel}</label><div class="settings-control" id="fontRubricRow"></div></div>
      <div class="settings-row"><label for="useSecondaryFont">${s.secondaryFontToggle}</label>
        <div class="settings-control">${toggleHtml('useSecondaryFont', settings.useSecondaryFont)}</div></div>
      <p class="settings-hint">${s.secondaryFontHint}</p>
      <div class="settings-row stacked"><label>${s.fontLatinLabel}</label><div class="settings-control" id="fontLatinRow"></div></div>
      <div class="settings-row"><label for="fsMain">${s.fsMain}</label>
        <div class="settings-control"><input type="range" id="fsMain" min="13" max="30" value="${settings.fontSizeMain}"><span id="fsMainVal">${settings.fontSizeMain}px</span></div></div>
      <div class="settings-row"><label for="fsRubric">${s.fsRubric}</label>
        <div class="settings-control"><input type="range" id="fsRubric" min="9" max="20" value="${settings.fontSizeRubric}"><span id="fsRubricVal">${settings.fontSizeRubric}px</span></div></div>
      <div class="settings-row"><label for="fsLatin">${s.fsLatin}</label>
        <div class="settings-control"><input type="range" id="fsLatin" min="13" max="30" value="${settings.fontSizeLatin}"><span id="fsLatinVal">${settings.fontSizeLatin}px</span></div></div>
      <div class="settings-row"><label for="lineHeight">${s.lineHeightLabel}</label>
        <div class="settings-control"><input type="range" id="lineHeight" min="1.2" max="2.4" step="0.05" value="${settings.lineHeight}"><span id="lineHeightVal">${settings.lineHeight}</span></div></div>
      <div class="settings-row"><label for="paraSpacing">${s.paraSpacingLabel}</label>
        <div class="settings-control"><input type="range" id="paraSpacing" min="0.2" max="2.5" step="0.1" value="${settings.paraSpacing}"><span id="paraSpacingVal">${settings.paraSpacing}em</span></div></div>
    </div>

    <div class="settings-section">
      <h3>${s.secColors}</h3>
      <p class="settings-hint">${s.colorsHint}</p>
      <div class="settings-row"><label for="cBg">${s.cBg}</label><div class="settings-control"><input type="color" id="cBg" value="${settings.bg}"></div></div>
      <div class="settings-row"><label for="cFg">${s.cFg}</label><div class="settings-control"><input type="color" id="cFg" value="${settings.fg}"></div></div>
      <div class="settings-row"><label for="cAccent">${s.cAccent}</label><div class="settings-control"><input type="color" id="cAccent" value="${settings.accent}"></div></div>
      <div class="settings-row"><label for="cPanel">${s.cPanel}</label><div class="settings-control"><input type="color" id="cPanel" value="${settings.panelBg}"></div></div>
    </div>

    <div class="settings-section">
      <h3>${s.secLayout}</h3>
      <div class="settings-row"><label for="readingMode">${s.readingModeLabel}</label>
        <div class="settings-control">
          <select id="readingMode">
            <option value="scroll"${settings.readingMode==='scroll'?' selected':''}>${s.optScroll}</option>
            <option value="paged"${settings.readingMode==='paged'?' selected':''}>${s.optPaged}</option>
          </select>
        </div></div>
      <div class="settings-row"><label for="bilingualMode">${s.bilingualLabel}</label>
        <div class="settings-control">
          <select id="bilingualMode">
            <option value="sideBySide"${settings.bilingualMode==='sideBySide'?' selected':''}>${s.optSideBySide}</option>
            <option value="latinOnly"${settings.bilingualMode==='latinOnly'?' selected':''}>${s.optLatinOnly}</option>
            <option value="vernacularOnly"${settings.bilingualMode==='vernacularOnly'?' selected':''}>${s.optVernOnly}</option>
          </select>
        </div></div>
      <div class="settings-row"><label for="showDividers">${s.showDividersLabel}</label><div class="settings-control">${toggleHtml('showDividers', settings.showDividers)}</div></div>
      <div class="settings-row"><label for="showSymbols">${s.showSymbolsLabel}</label><div class="settings-control">${toggleHtml('showSymbols', settings.showSymbols)}</div></div>
      <div class="settings-row"><label for="dropCapStyle">${s.dropCapLabel}</label>
        <div class="settings-control">
          <select id="dropCapStyle">
            <option value="none"${settings.dropCapStyle==='none'?' selected':''}>${s.optDcNone}</option>
            <option value="clean"${settings.dropCapStyle==='clean'?' selected':''}>${s.optDcClean}</option>
            <option value="roman"${settings.dropCapStyle==='roman'?' selected':''}>${s.optDcRoman}</option>
            <option value="illuminated"${settings.dropCapStyle==='illuminated'?' selected':''}>${s.optDcIllum}</option>
          </select>
        </div></div>
      <div class="settings-row"><label for="sunsetAware">${s.sunsetLabel}</label><div class="settings-control">${toggleHtml('sunsetAware', settings.sunsetAwareVespers)}</div></div>
      <p class="settings-hint">${s.sunsetHint}</p>
    </div>

    <div class="settings-section">
      <h3>${s.secBackground}</h3>
      <div class="bg-upload-preview" id="bgPreview">${settings.bgImage ? '' : s.bgNoImage}</div>
      <div class="settings-row"><label for="bgUpload">${s.bgUploadLabel}</label>
        <div class="settings-control"><input type="file" id="bgUpload" accept="image/*"></div></div>
      <div class="settings-row"><label for="bgClear">${s.bgClearLabel}</label>
        <div class="settings-control"><button class="icon-btn text" id="bgClear">${s.bgClearBtn}</button></div></div>
      <div class="settings-row"><label for="bgOverlay">${s.bgOverlayLabel}</label>
        <div class="settings-control"><input type="range" id="bgOverlay" min="0" max="1" step="0.02" value="${settings.bgOverlayOpacity}"><span id="bgOverlayVal">${settings.bgOverlayOpacity}</span></div></div>
      <div class="settings-row"><label for="bgBlur">${s.bgBlurLabel}</label>
        <div class="settings-control"><input type="range" id="bgBlur" min="0" max="20" step="1" value="${settings.bgBlur}"><span id="bgBlurVal">${settings.bgBlur}px</span></div></div>
      <h3 style="margin-top:1.1rem;">${s.secTextures}</h3>
      <div class="texture-grid" id="textureGrid"></div>
    </div>

    <div class="settings-section">
      <h3>${s.secLogo}</h3>
      <div class="settings-row"><label for="showLogo">${s.showLogoLabel}</label><div class="settings-control">${toggleHtml('showLogo', settings.showLogo)}</div></div>
    </div>

    <div class="settings-group-heading">${s.secGroupLiturgical}</div>

    <div class="settings-section">
      <h3>${s.secPrayerElements}</h3>
      <div class="settings-row"><label for="paterNosterBread">${s.paterNosterBreadLabel}</label>
        <div class="settings-control">
          <select id="paterNosterBread">
            <option value="supersubstantialem"${settings.paterNosterBread==='supersubstantialem'?' selected':''}>${s.optSupersubstantialem}</option>
            <option value="cotidianum"${settings.paterNosterBread==='cotidianum'?' selected':''}>${s.optCotidianum}</option>
          </select>
        </div></div>
      <p class="settings-hint">${s.paterNosterBreadHint}</p>
      <div class="settings-row"><label for="showGloriaPatri">${s.gloriaPatriLabel}</label>
        <div class="settings-control">${toggleHtml('showGloriaPatri', settings.showGloriaPatri)}</div></div>
      <p class="settings-hint">${s.gloriaPatriHint}</p>
      <div class="settings-row"><label for="sacredSilence">${s.sacredSilenceLabel}</label>
        <div class="settings-control">${toggleHtml('sacredSilence', settings.sacredSilence)}</div></div>
      <p class="settings-hint">${s.sacredSilenceHint}</p>
      <div class="settings-row"><label for="marianAntiphonEnabled">${s.marianLabel}</label>
        <div class="settings-control">${toggleHtml('marianAntiphonEnabled', settings.marianAntiphonEnabled)}</div></div>
      <p class="settings-hint">${s.marianHint}</p>
      <div class="settings-row"><label for="marianAntiphonChoice">${s.marianChoiceLabel}</label>
        <div class="settings-control"><select id="marianAntiphonChoice"></select></div></div>
    </div>

    <div class="settings-reset"><button id="resetSettingsBtn">${s.resetBtn}</button></div>
  `;

  const mlSel = document.getElementById('menuLangSelectSettings');
  Object.entries(MENU_LANG_NAMES).forEach(([code, label]) => {
    const o = document.createElement('option'); o.value = code; o.textContent = label;
    if (code === settings.menuLang) o.selected = true;
    mlSel.appendChild(o);
  });
  mlSel.addEventListener('change', e => {
    settings.menuLang = e.target.value; saveSettings();
    syncMenuLangSelects(); renderSettingsScreen(); refreshChromeText();
  });

  const marianSel = document.getElementById('marianAntiphonChoice');
  Object.entries(MARIAN_ANTIPHONS).forEach(([key, ant]) => {
    const o = document.createElement('option');
    o.value = key;
    o.textContent = (key === 'none') ? s.marianNone : (ant.title[settings.menuLang] || ant.title.en);
    if (key === settings.marianAntiphonChoice) o.selected = true;
    marianSel.appendChild(o);
  });
  marianSel.addEventListener('change', e => {
    settings.marianAntiphonChoice = e.target.value; saveSettings(); render();
  });

  // Presets
  const grid = document.getElementById('presetGrid');
  grid.innerHTML = Object.entries(PRESETS).filter(([id]) => id !== 'custom').map(([id, p]) => `
    <div class="preset-card${settings.preset === id ? ' active' : ''}" data-preset="${id}">
      <div class="swatch" style="background:${p.bg}; border-color:${p.accent};"></div>
      ${esc(p.label)}
    </div>`).join('') + `
    <div class="preset-card${settings.preset === 'custom' ? ' active' : ''}" data-preset="custom">
      <div class="swatch" style="background: linear-gradient(135deg, ${settings.bg}, ${settings.accent});"></div>
      Custom
    </div>`;
  grid.querySelectorAll('.preset-card').forEach(card => card.addEventListener('click', () => {
    applyPreset(card.dataset.preset);
  }));

  // Font pickers
  ['fontMain', 'fontRubric', 'fontLatin'].forEach(key => {
    const row = document.getElementById(key + 'Row');
    row.innerHTML = `<div class="font-swatch-row">` + FONT_CHOICES.map(f =>
      `<div class="font-swatch${settings[key] === f.id ? ' active' : ''}" data-key="${key}" data-font="${f.id}" style="font-family:${f.css}">${esc(f.label)}</div>`
    ).join('') + `</div>`;
  });
  body.querySelectorAll('.font-swatch').forEach(sw => sw.addEventListener('click', () => {
    settings[sw.dataset.key] = sw.dataset.font;
    settings.preset = 'custom';
    saveSettings(); applySettingsToDOM(); renderSettingsScreen();
  }));

  // Textures
  const texGrid = document.getElementById('textureGrid');
  texGrid.innerHTML = TEXTURE_CHOICES.map(t => `
    <div class="texture-card${settings.texture === t.id ? ' active' : ''}" data-texture="${t.id}"
         style="background-image:${textureBackgroundImage(t.id)}; background-color:${settings.bg};">
      <span>${esc(t.label)}</span>
    </div>`).join('');
  texGrid.querySelectorAll('.texture-card').forEach(card => card.addEventListener('click', () => {
    settings.texture = card.dataset.texture; settings.preset = 'custom';
    saveSettings(); applySettingsToDOM(); renderSettingsScreen();
  }));

  if (settings.bgImage) {
    document.getElementById('bgPreview').style.backgroundImage = `url("${settings.bgImage}")`;
  }

  wireSettingsControls();
  renderSettingsPreview();
}

function wireSettingsControls() {
  const on = (id, ev, fn) => { const el = document.getElementById(id); if (el) el.addEventListener(ev, fn); };

  on('syncColor', 'change', e => { settings.liturgicalColorSync = e.target.checked; saveSettings(); applySettingsToDOM(); });

  on('fsMain', 'input', e => { settings.fontSizeMain = +e.target.value; document.getElementById('fsMainVal').textContent = e.target.value + 'px'; applySettingsToDOM(); });
  on('fsMain', 'change', () => saveSettings());
  on('fsRubric', 'input', e => { settings.fontSizeRubric = +e.target.value; document.getElementById('fsRubricVal').textContent = e.target.value + 'px'; applySettingsToDOM(); });
  on('fsRubric', 'change', () => saveSettings());
  on('fsLatin', 'input', e => { settings.fontSizeLatin = +e.target.value; document.getElementById('fsLatinVal').textContent = e.target.value + 'px'; applySettingsToDOM(); });
  on('fsLatin', 'change', () => saveSettings());
  on('lineHeight', 'input', e => { settings.lineHeight = +e.target.value; document.getElementById('lineHeightVal').textContent = e.target.value; applySettingsToDOM(); });
  on('lineHeight', 'change', () => saveSettings());
  on('paraSpacing', 'input', e => { settings.paraSpacing = +e.target.value; document.getElementById('paraSpacingVal').textContent = e.target.value + 'em'; applySettingsToDOM(); });
  on('paraSpacing', 'change', () => saveSettings());

  on('cBg', 'input', e => { settings.bg = e.target.value; settings.preset = 'custom'; applySettingsToDOM(); });
  on('cBg', 'change', () => saveSettings());
  on('cFg', 'input', e => { settings.fg = e.target.value; settings.preset = 'custom'; applySettingsToDOM(); });
  on('cFg', 'change', () => saveSettings());
  on('cAccent', 'input', e => { settings.accent = e.target.value; settings.accentSoft = e.target.value + '33'; settings.preset = 'custom'; applySettingsToDOM(); });
  on('cAccent', 'change', () => saveSettings());
  on('cPanel', 'input', e => { settings.panelBg = e.target.value; settings.preset = 'custom'; applySettingsToDOM(); });
  on('cPanel', 'change', () => saveSettings());

  on('readingMode', 'change', e => { settings.readingMode = e.target.value; saveSettings(); applySettingsToDOM(); applyPaging(); });
  on('bilingualMode', 'change', e => { settings.bilingualMode = e.target.value; saveSettings(); render(); renderSettingsPreview(); });
  on('showDividers', 'change', e => { settings.showDividers = e.target.checked; saveSettings(); applySettingsToDOM(); });
  on('showSymbols', 'change', e => { settings.showSymbols = e.target.checked; saveSettings(); applySettingsToDOM(); });
  on('dropCapStyle', 'change', e => { settings.dropCapStyle = e.target.value; saveSettings(); applySettingsToDOM(); });
  on('sunsetAware', 'change', e => { settings.sunsetAwareVespers = e.target.checked; saveSettings(); });
  on('showGloriaPatri', 'change', e => { settings.showGloriaPatri = e.target.checked; saveSettings(); render(); });
  on('sacredSilence', 'change', e => { settings.sacredSilence = e.target.checked; saveSettings(); render(); });
  on('marianAntiphonEnabled', 'change', e => { settings.marianAntiphonEnabled = e.target.checked; saveSettings(); render(); });
  on('useSecondaryFont', 'change', e => { settings.useSecondaryFont = e.target.checked; saveSettings(); applySettingsToDOM(); });

  on('bgUpload', 'change', e => {
    const file = e.target.files[0];
    if (!file) return;
    if (file.size > 4 * 1024 * 1024) {
      alert('Please choose an image under 4 MB (it is stored locally in your browser).');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      settings.bgImage = reader.result;
      settings.preset = 'custom';
      saveSettings(); applySettingsToDOM();
      document.getElementById('bgPreview').style.backgroundImage = `url("${settings.bgImage}")`;
      document.getElementById('bgPreview').textContent = '';
    };
    reader.readAsDataURL(file);
  });
  on('bgClear', 'click', () => {
    settings.bgImage = null; saveSettings(); applySettingsToDOM();
    const prev = document.getElementById('bgPreview');
    prev.style.backgroundImage = ''; prev.textContent = ui().bgNoImage;
  });
  on('bgOverlay', 'input', e => { settings.bgOverlayOpacity = +e.target.value; document.getElementById('bgOverlayVal').textContent = e.target.value; applySettingsToDOM(); });
  on('bgOverlay', 'change', () => saveSettings());
  on('bgBlur', 'input', e => { settings.bgBlur = +e.target.value; document.getElementById('bgBlurVal').textContent = e.target.value + 'px'; applySettingsToDOM(); });
  on('bgBlur', 'change', () => saveSettings());

  on('showLogo', 'change', e => { settings.showLogo = e.target.checked; saveSettings(); applySettingsToDOM(); });
  on('paterNosterBread', 'change', e => { settings.paterNosterBread = e.target.value; saveSettings(); render(); renderSettingsPreview(); });

  on('resetSettingsBtn', 'click', () => {
    if (!confirm(ui().resetConfirm)) return;
    const keepMenuLang = settings.menuLang;
    settings = defaultSettings();
    settings.menuLang = keepMenuLang; // resetting appearance shouldn't silently switch your menu language
    saveSettings(); applySettingsToDOM(); renderSettingsScreen(); render();
  });
}

/* ============================================================
   FIRST-VISIT DEVELOPMENT NOTICE
   ============================================================ */
const FIRSTVISIT_KEY = 'loth_firstvisit_seen_v1';
function maybeShowFirstVisitModal() {
  let seen = false;
  try { seen = localStorage.getItem(FIRSTVISIT_KEY) === '1'; } catch (e) { /* storage unavailable */ }
  if (seen) return;
  document.getElementById('firstVisitTitleEn').textContent = UI.en.firstVisitTitle;
  document.getElementById('firstVisitBodyEn').textContent = UI.en.firstVisitBody;
  document.getElementById('firstVisitTitleEs').textContent = UI.es.firstVisitTitle;
  document.getElementById('firstVisitBodyEs').textContent = UI.es.firstVisitBody;
  document.getElementById('firstVisitDismiss').textContent = UI.en.firstVisitDismiss + ' / ' + UI.es.firstVisitDismiss;
  document.getElementById('firstVisitModal').classList.remove('hidden');
}
document.getElementById('firstVisitDismiss').addEventListener('click', () => {
  document.getElementById('firstVisitModal').classList.add('hidden');
  try { localStorage.setItem(FIRSTVISIT_KEY, '1'); } catch (e) { /* storage unavailable */ }
});

/* ============================================================
   BETA MODE (English machine translation + debug menu)
   ============================================================ */
function showBetaWarning(callback) {
  const modal = document.getElementById('betaWarnModal');
  document.getElementById('betaWarnTitleEn').textContent = 'Beta feature: live English translation';
  document.getElementById('betaWarnBodyEn').textContent =
    'The Latin and Spanish texts in this app are the original, carefully sourced liturgical texts. ' +
    'English has not been implemented at all yet - what you will see instead is a live, unverified machine ' +
    'translation of the Spanish text, generated on the fly purely for the convenience of beta testers who only ' +
    'read English. It may contain errors, awkward phrasing, or outright mistakes, and nothing is saved or checked ' +
    'by anyone. Do not treat it as an accurate liturgical text.';
  document.getElementById('betaWarnTitleEs').textContent = 'Función beta: traducción automática al inglés en vivo';
  document.getElementById('betaWarnBodyEs').textContent =
    'Los textos en latín y español de esta aplicación son los textos litúrgicos originales, cuidadosamente ' +
    'investigados. El inglés todavía no se ha implementado en absoluto - lo que verá en su lugar es una ' +
    'traducción automática en vivo, sin verificar, del texto en español, generada al momento únicamente para la ' +
    'comodidad de los usuarios beta que solo leen inglés. Puede contener errores, frases torpes o equivocaciones, ' +
    'y nada se guarda ni se revisa. No lo considere un texto litúrgico preciso.';
  document.getElementById('betaWarnCancel').textContent = 'Cancel / Cancelar';
  document.getElementById('betaWarnAccept').textContent = 'I understand / Entiendo';
  modal.classList.remove('hidden');
  const acceptBtn = document.getElementById('betaWarnAccept');
  const cancelBtn = document.getElementById('betaWarnCancel');
  const cleanup = () => {
    modal.classList.add('hidden');
    acceptBtn.removeEventListener('click', onAccept);
    cancelBtn.removeEventListener('click', onCancel);
  };
  function onAccept() { cleanup(); callback(true); }
  function onCancel() { cleanup(); callback(false); }
  acceptBtn.addEventListener('click', onAccept);
  cancelBtn.addEventListener('click', onCancel);
}
function syncBetaCheckboxes() {
  document.getElementById('betaCheckboxA').checked = betaMode;
  document.getElementById('betaCheckboxB').checked = betaMode;
  document.getElementById('btnDebug').classList.toggle('hidden', !betaMode);
  document.getElementById('btnDebugFromHourSelect').classList.toggle('hidden', !betaMode);
}
function onBetaModeChanged() {
  populateLanguageSelectors();
  render();
}
function wireBetaCheckboxes() {
  ['betaCheckboxA', 'betaCheckboxB'].forEach(id => {
    document.getElementById(id).addEventListener('change', (e) => {
      if (e.target.checked) {
        e.target.checked = false; // only actually flips on if the warning is accepted
        showBetaWarning((accepted) => {
          if (accepted) { betaMode = true; syncBetaCheckboxes(); onBetaModeChanged(); }
        });
      } else {
        betaMode = false;
        syncBetaCheckboxes();
        onBetaModeChanged();
      }
    });
  });
}

// Not persisted anywhere and not saved server-side - purely an in-memory,
// per-page-load cache so flipping between hours/dates during one visit
// doesn't re-request identical text from the translation service repeatedly.
const translationCache = new Map();
let translationQuotaExhausted = false; // once MyMemory's free daily quota is hit, stop hammering it
// Generic live-translation helper, keyed by "source|target" MyMemory
// language pairs. Used both for beta-English page translation (es->en) and
// for auto-translating a user's own Personal Intentions into whichever
// language(s) the Preces are currently showing (en->es / en->la).
function translateText(text, sourcePair) {
  if (!text) return Promise.resolve(text);
  const cacheKey = sourcePair + '::' + text;
  if (translationQuotaExhausted) return Promise.resolve(text + ' [translation quota reached for today - try again later]');
  if (translationCache.has(cacheKey)) return translationCache.get(cacheKey);
  const url = 'https://api.mymemory.translated.net/get?q=' + encodeURIComponent(text) + '&langpair=' + sourcePair;
  const p = fetch(url)
    .then(r => r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)))
    .then(data => {
      // MyMemory always answers HTTP 200, even over quota - the real status
      // is embedded in the JSON body itself, not the HTTP status line, so a
      // truthy translatedText isn't proof of a real translation: over-quota
      // and other non-2xx cases put an all-caps warning string there instead.
      if (data && data.responseStatus && Number(data.responseStatus) !== 200) {
        if (Number(data.responseStatus) === 429) translationQuotaExhausted = true;
        throw new Error('MyMemory status ' + data.responseStatus);
      }
      return (data && data.responseData && data.responseData.translatedText) || text;
    })
    .catch(() => text + (translationQuotaExhausted
      ? ' [translation quota reached for today - try again later]'
      : ' [machine translation unavailable]'));
  translationCache.set(cacheKey, p);
  return p;
}
function translateSpanishToEnglish(text) { return translateText(text, 'es|en'); }
// Personal Intentions are typed in whatever language the person praying
// speaks - there's no way to detect that, so English is assumed as the
// source (matching the rest of this beta feature) and translated into
// whichever language a given column is actually showing (Latin included,
// on a best-effort basis - MyMemory's Latin quality is uneven, same caveat
// as everything else in this beta feature). A column already showing
// English gets the original text back untranslated.
function translateIntentionFor(text, targetLang) {
  if (targetLang === 'en') return Promise.resolve(text);
  return translateText(text, 'en|' + targetLang);
}
// Finds the nearest preceding "unit-header" row for a content row, to read
// its data-mt-skip marker (set by render() per-unit, based on whether that
// unit actually has genuine sourced English - see unitHasRealEnglish there).
function rowNeedsSkip(cell) {
  let row = cell.closest('tr');
  while (row) {
    if (row.classList.contains('unit-header')) return row.dataset.mtSkip === '1';
    row = row.previousElementSibling;
  }
  return false;
}

// Runs AFTER the table is already built with Spanish content standing in for
// 'en' wherever a unit has no real English of its own (see render()'s
// per-unit uLeft/uRight resolution) - reads each affected cell's own plain
// text (skipping the unit-label header and verse-number spans, which are
// already correctly labeled/numeric and shouldn't be sent through a
// translator), fetches a live translation, and swaps it in. Cells belonging
// to a unit that already has genuine sourced English (marked via
// data-mt-skip="1" on that unit's header row) are left completely alone.
function applyBetaEnglishTranslation(table, leftIsEnglish, rightIsEnglish) {
  const cells = [];
  if (leftIsEnglish) cells.push(...table.querySelectorAll('td.col-left, td.single'));
  if (rightIsEnglish) cells.push(...table.querySelectorAll('td.col-right'));
  cells.forEach(cell => {
    if (cell.querySelector('select')) return; // the hymn-choice picker row - nothing to translate
    if (rowNeedsSkip(cell)) return; // this unit already has real, sourced English
    const clone = cell.cloneNode(true);
    clone.querySelectorAll('.unit-label, .vn').forEach(n => n.remove());
    const plain = clone.textContent.trim();
    if (!plain) return;
    cell.classList.add('mt-pending');
    translateSpanishToEnglish(plain).then(translated => {
      cell.classList.remove('mt-pending');
      const labelDiv = cell.querySelector('.unit-label');
      cell.innerHTML = (labelDiv ? labelDiv.outerHTML : '') +
        '<span class="mt-badge" title="Machine-translated, beta only">MT</span>' +
        mdLite(esc(translated)).replace(/\n/g, '<br>');
    });
  });
}

/* ============================================================
   BETA DEBUG MENU (raw settings inspector, for bug hunting)
   ============================================================ */
function openDebugDrawer() {
  closeDrawers();
  const s = ui();
  const backdrop = document.createElement('div');
  backdrop.className = 'drawer-backdrop'; backdrop.id = 'drawerBackdrop';
  backdrop.addEventListener('click', closeDrawers);
  document.body.appendChild(backdrop);

  const drawer = document.createElement('div');
  drawer.className = 'drawer'; drawer.id = 'activeDrawer';
  drawer.innerHTML = `
    <div class="drawer-header"><h3>${esc(s.debugTitle)}</h3><button class="icon-btn" id="closeDrawerBtn">&times;</button></div>
    <div class="drawer-body">
      <p class="settings-hint">${esc(s.debugHint)}</p>
      <textarea id="debugJsonBox">${esc(JSON.stringify(settings, null, 2))}</textarea>
      <div class="add-intention-row">
        <button id="debugApplyBtn">${esc(s.debugApply)}</button>
      </div>
      <div class="debug-var-row"><span>currentPageIndex</span><code>${currentPageIndex} / ${currentPages.length}</code></div>
      <div class="debug-var-row"><span>betaMode</span><code>${betaMode}</code></div>
      <div class="debug-var-row"><span>translationCache size</span><code>${translationCache.size}</code></div>
      <div class="debug-var-row"><span>hourSelect</span><code>${esc(hourSel.value)}</code></div>
      <div class="debug-var-row"><span>dateSelect</span><code>${esc(dateSel.value)}</code></div>
      <div class="add-intention-row">
        <button id="debugClearStorageBtn">${esc(s.debugClearStorage)}</button>
        <button id="debugReloadBtn">${esc(s.debugReloadData)}</button>
      </div>
      <div class="add-intention-row">
        <button id="debugPhoneSimBtn">${esc(s.debugPhoneSim)}</button>
      </div>
    </div>`;
  document.body.appendChild(drawer);
  document.getElementById('closeDrawerBtn').addEventListener('click', closeDrawers);
  document.getElementById('debugApplyBtn').addEventListener('click', () => {
    try {
      const parsed = JSON.parse(document.getElementById('debugJsonBox').value);
      settings = Object.assign(defaultSettings(), parsed);
      saveSettings(); applySettingsToDOM(); syncMenuLangSelects(); refreshChromeText(); render();
      openDebugDrawer();
    } catch (e) { /* invalid JSON - silently ignored per the debug menu's own stated behavior */ }
  });
  document.getElementById('debugClearStorageBtn').addEventListener('click', () => {
    if (!confirm('Clear ALL local storage for this app (settings, intentions, diary)?')) return;
    try { localStorage.clear(); } catch (e) { /* storage unavailable */ }
    location.reload();
  });
  document.getElementById('debugReloadBtn').addEventListener('click', () => {
    for (const iso of DATA.date_order) {
      fetch('/api/day?date=' + encodeURIComponent(iso) + '&_=' + Date.now())
        .then(r => r.ok ? r.json() : Promise.reject(new Error('HTTP ' + r.status)))
        .then(fresh => { DATA.dates[iso] = fresh; render(); renderHero(); })
        .catch(() => { /* dev_server.py not running */ });
    }
  });
  document.getElementById('debugPhoneSimBtn').addEventListener('click', openPhoneSimulator);
}

// A real phone-sized <iframe> loading this same page fresh - lets a beta
// tester check the mobile layout without leaving their desktop browser or
// touching real device-emulation devtools. Cookies/localStorage inside the
// iframe are shared with the parent page (same origin), so settings picked
// there are the tester's own real settings, not a separate sandbox.
function openPhoneSimulator() {
  closeDrawers();
  const backdrop = document.createElement('div');
  backdrop.className = 'drawer-backdrop'; backdrop.id = 'phoneSimBackdrop';
  backdrop.addEventListener('click', closePhoneSimulator);
  document.body.appendChild(backdrop);

  const frame = document.createElement('div');
  frame.className = 'phone-sim-frame'; frame.id = 'phoneSimFrame';
  frame.innerHTML = `
    <div class="phone-sim-chrome">
      <span>375 × 812</span>
      <button class="icon-btn" id="closePhoneSimBtn">&times;</button>
    </div>
    <iframe class="phone-sim-viewport" src="${location.href}"></iframe>`;
  document.body.appendChild(frame);
  document.getElementById('closePhoneSimBtn').addEventListener('click', closePhoneSimulator);
}
function closePhoneSimulator() {
  const b = document.getElementById('phoneSimBackdrop'); if (b) b.remove();
  const f = document.getElementById('phoneSimFrame'); if (f) f.remove();
}

/* ============================================================
   INIT / WIRING
   ============================================================ */
document.getElementById('btnSettingsFromHourSelect').addEventListener('click', () => openSettings('hourSelectScreen'));
document.getElementById('btnSettings').addEventListener('click', () => openSettings('mainScreen'));
document.getElementById('btnInfoFromHourSelect').addEventListener('click', openInfoModal);
document.getElementById('btnInfo').addEventListener('click', openInfoModal);
document.getElementById('infoModalClose').addEventListener('click', closeInfoModal);
document.getElementById('infoModal').addEventListener('click', (e) => { if (e.target.id === 'infoModal') closeInfoModal(); });
document.getElementById('btnCloseSettings').addEventListener('click', closeSettings);
document.getElementById('btnBackToHourSelect').addEventListener('click', goToHourSelect);
document.getElementById('btnIntentions').addEventListener('click', openIntentionsDrawer);
document.getElementById('btnIntentionsFromHourSelect').addEventListener('click', openIntentionsDrawer);
document.getElementById('btnDiary').addEventListener('click', openDiaryDrawer);
document.getElementById('btnDiaryFromHourSelect').addEventListener('click', openDiaryDrawer);
document.getElementById('btnDebug').addEventListener('click', openDebugDrawer);
document.getElementById('btnDebugFromHourSelect').addEventListener('click', openDebugDrawer);
document.getElementById('btnHymnal').addEventListener('click', () => openHymnal('mainScreen'));
document.getElementById('btnHymnalFromHourSelect').addEventListener('click', () => openHymnal('hourSelectScreen'));
document.getElementById('btnCloseHymnal').addEventListener('click', closeHymnal);
wireBetaCheckboxes();

applyChrome();
dateSel.value = closestAvailableDate(isoDateInTimeZone(browserTz));
applySettingsToDOM();
renderLogo('logoHourSelect', false);
renderLogo('logoMain', true);
syncMenuLangSelects();
refreshChromeText();
render();
renderHero();
// The liturgical-color lookup in applySettingsToDOM() depends on
// currentDayData() actually resolving - on first paint that data isn't
// reliably bound yet, so the very first accent color could be the preset's
// default rather than today's liturgical color. render()/renderHero() above
// guarantee the day data is live by this point, so re-apply once more here.
applySettingsToDOM();
maybeShowFirstVisitModal();

// Land on the Hour Selection screen by default, unless there's a very
// recent remembered position (same browser session territory) - then jump
// straight back into that hour ("Where was I" resume).
const lastPos = loadLastPosition();
if (lastPos && lastPos.date && lastPos.hour && DATA.dates[lastPos.date] && (Date.now() - lastPos.ts) < 12 * 3600 * 1000) {
  dateSel.value = lastPos.date;
  hourSel.value = lastPos.hour;
  goToMainScreen();
} else {
  goToHourSelect();
}
