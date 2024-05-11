#==========================================================
# Russian language [RU]
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================

MENU_SC_REBUILD_MODES = [
	'Стандартный режим (Выбор ПО, остальное по-умолчанию / Все (12) типов)',
	'Минимальный набор (Выбор 2 первых типов и ПО / 3 типа)',
	'Эксперт (Настройка всех (12) типов)',
]

MENU_NVS_COPY = [
	'Заменить %s на значение из бекапа (%s <= %s)',
	'Заменить бекап на текущее значение %s (%s => %s)',
]

MENU_EAP_KEYS = [
	'Заменить A на B (key_a <= key_b)',
	'Заменить B на A (key_a => key_b)',
	'Исправить magic A *',
	'Исправить magic B *',
	'Сгененрировать новые ключи A,B (длина 0x60) *',
	'Сгененрировать новые ключи A,B (длина 0x40) *',
	'Очистить ключ B *',
]

MENU_FLASHER = [
	'Считать все',
	'Считать область',
	'Считать блок',
	'Записать всё',
	'Записать область',
	'Записать блок',
	'Проверить всё',
	'Проверить область',
	'Проверить блок',
	'Стереть всё',
	'Стереть область',
	'Стереть блок',
]

MENU_SERIAL_MONITOR = {
	'Ctrl+Q':'закрыть мониторинг',
	'Ctrl+R':'перезапустить',
	'Ctrl+E':'режим команд EMC',
	'Ctrl+B':'отображать байткоды < 0x20',
	'Ctrl+L':'вести лог в файл',
}

MENU_TOOL_SELECTION = [
	'Выбрать Файл',
	'Терминал (UART)',
	'sFlash r/w (SPIway by Judges)',
	'Syscon r/w (SCTool by Abkarino & EgyCnq)',
	'Syscon r/o (SCRead by DarkNESmonk)',
	'Syscon w/o (для стоковых Renesas RL78)',
	'Сменить Язык интерфейса',
	'Выход',
]

MENU_FILE_SELECTION = {
	'a':'Все файлы / Фильтр [bin,pup]',
	'f':'Собрать дамп sflash0',
	'b':'Собрать 2BLS/PUP',
	'r':'Пакетно переименовать (вынести инфо в название файла)',
	'c':'Сравнить файлы в текущей папке',
	'm':'Выйти / Назад',
}

MENU_EXTRA_FLASHER = {
	's':'Выбрать файл',
	'f':'Запустить утилиту для работы с файлом',
	'm':'Выйти / Назад',
}

MENU_EXTRA = {
	's':'Выбрать другой файл',
	'f':'Прошить файл (целоком/частично) обратно в чип',
	'r':'Переименовать (вынести инфо в название файла)',
	'm':'Выйти / Назад',
}

MENU_SFLASH_ACTIONS = [
	'Флаги (UART, RNG, Memtest, и т.д.)',
	'Частота памяти (GDDR5)',
	'Флаг загрузки SAMU',
	'Переключение слота CoreOS (Откат версии ПО)',
	'Переключение CoreOS через рекавери (legit patch)',
	'Замена ПО южного моста',
	'Замена ПО беспроводного модуля',
	'Дополнительные инструменты',
]

MENU_ADDTIONAL = [
	'Разобрать дамп sFlash0 на разделы',
	'Собрать дамп sFlash0 из файлов',
	'Просмотр / Восстановление NVS блоков (1C9, 1CA)',
	'Просмотр / Восстановление ключа EAP',
	'Получить ключи HDD = расшифровка EAP ключа = создание [keys.bin]',
	'Создать EMC cfw (для Fat 1xxx/11xx)',
	'Базовая валидация дампа',
	'Анализ и восстановление разделов',
]

MENU_SC_ACTIONS = [
	'Вкл/выкл режима Debug',
	'Автоматический патч SNVS',
	'Просмотр блоков SNVS',
	'Просмотр блоков NVS',
	'Ручной патч SNVS',
	'Дополнительные инструменты',
]

MENU_SC_ADV_ACTIONS = [
	'Сброс счетчиков SNVS',
	'Выбор режима (00-03)',
	'Выбор режима загрузки (04-07)',
	'Syscon Rebuilder - пересборка SNVS (Factory Reset)',
	'Восстановление прошивки Syscon',
	'Конвертировать для Renesas flasher (Motorolla S28)',
]

MENU_PATCHES = [
	'Метод A - последние 08-0B будут удалены (4 шт)',
	'Метод B - последние 08-0B и все что ниже будут удалены (%d шт)',
	'Метод C - очистить все ниже предыдущих 08-0B (%d шт)',
	'Метод D - очистить все ниже последних 08-0B (%d шт)',
	'Метод E - очистить предыдущие 08-0B и все что ниже (%d шт)',
]

MENU_SC_STATUSES = [
	'Слот CoreOs перезаписан',
	'Можно патчить',
	'Уже пропатчен или застрял на обновлении',
	'Вероятно можно патчить',
]

MENU_SPW_ACTS = {
	'read':		'Чтение',
	'write':	'Запсиь',
	'verify':	'Проверка',
	'erase':	'Стирание',
}

STR_LANGUAGE			= 'Язык'
STR_SECONDS				= '%0.0f секунд'
STR_NVS_AREAS			= 'Области NVS'
STR_PORTS_LIST			= 'Список портов'
STR_MAIN_MENU			= 'Главное меню'
STR_FILE_LIST			= 'Список файлов'
STR_SFLASH_INFO			= 'Информация о дампе sFlash0'
STR_ADDITIONAL			= 'Дополнительные инструменты'
STR_SYSCON_INFO			= 'Информация о дампе Syscon'
STR_COMPARE				= 'Сравнение'
STR_HELP				= 'Справка'
STR_ACTIONS				= 'Действия'
STR_COREOS_SWITCH		= 'Переключатель CoreOS'
STR_SWITCH_PATTERNS		= 'Шаблоны переключения'
STR_MEMCLOCK			= 'Частота памяти'
STR_SAMU_BOOT			= 'Загрузка SAMU'
STR_SYSFLAGS			= 'Системные флаги'
STR_NVS_ENTRIES			= 'Записи (%s) Syscon'
STR_APATCH_SVNS			= 'Авто патчи SNVS'
STR_MPATCH_SVNS			= 'Ручной патч SNVS'
STR_SFLASH_VALIDATOR	= 'Валидация дампа sFlash0'
STR_SFLASH_FLAGS		= 'Флаги sFlash0'
STR_SFLASH_EXTRACT		= 'Распаковка sFlash0'
STR_SFLASH_BUILD		= 'Сборка sFlash0'
STR_HDD_KEY				= 'Ключ HDD eap'
STR_2BLS_BUILDER		= 'Сборка 2BLS'
STR_UNPACK_2BLS			= 'Распаковка 2BLS'
STR_UNPACK_PUP			= 'Распаковка дешифрованных PUP(.dec)'
STR_EMC_CFW				= 'EMC CFW (Aeolia)'
STR_EAP_KEYS			= 'Ключи EAP'
STR_SC_BOOT_MODES		= 'Загрузочные записи'
STR_INFO				= 'Информация'
STR_SC_READER			= 'Syscon reader'
STR_SPIWAY				= 'SPIway by Judges & Abkarino'
STR_SCF					= 'Syscon Flasher by Abkarino'
STR_LEG_PATCH			= 'Переключение CoreOS через рекавери'
STR_PART_RECOVERY		= 'Восстановление раздела'
STR_PART_ANALYZE		= 'Анализ раздела'
STR_PART_LIST			= 'Список разделов'
STR_PARTS_INFO			= 'Информация о разделах'
STR_WIFI_PATCHER		= 'Замена ПО WiFi'
STR_SB_PATCHER			= 'Замена ПО южного моста'
STR_RL78FLASH			= 'RL78 Flasher'
STR_SC_REBUILDER		= 'Syscon Rebuilder'

STR_ALL					= 'Все'
STR_UNIQUE				= 'Уникальные'
STR_BACKUP				= 'Бэкап'
STR_EQUAL				= 'Одинаковые'
STR_NOT_EQUAL			= 'Не идиентичны'
STR_NO_INFO				= '- Нет информации -'
STR_OFF					= 'Выкл'
STR_ON					= 'Вкл'
STR_WARNING				= 'Внимание'
STR_HELP				= 'Помощь'
STR_UNKNOWN				= '- Неизвестно -'
STR_YES					= 'Да'
STR_NO					= 'Нет'
STR_PROBABLY			= 'Вероятно'
STR_NOT_SURE			= 'не точно'
STR_DIFF				= 'Различаются'
STR_NOT_FOUND			= 'не найден'
STR_BAD_SIZE			= 'не тот размер'
STR_OK					= 'OK'
STR_FAIL				= 'Сбой'
STR_CANCEL				= 'Отмена'
STR_IS_PART_VALID		= '[%s] %s FW %s'
STR_SNVS_ENTRIES		= '%d записей найдено по адресу 0x%05X'
STR_SERIAL_MONITOR		= 'Терминал'
STR_ELAPSEDTIME			= 'Затрачено времени'

STR_NO_PORT_CHOSEN		= ' Не выбран порт'
STR_NO_PORTS			= ' Не найден ни один последовательный порт'
STR_PORT_UNAVAILABLE	= ' Выбранный порт недоступен'
STR_PORT_CLOSED			= ' Порт закрыт'
STR_STOP_MONITORING		= ' Мониторинг был завершен пользователем'

STR_RESTART_APP			= ' Перезапустите приложение, чтобы применить настройки'
STR_GENERATE_ALL_PS		= ' Сгенерировать все патчи'
STR_ACTION_NA			= ' Действие недоступно - %s'
STR_EMC_CFW_WARN		= ' На данный момент EMC CFW доступно для 10xx/11xx PS4 Fat'
STR_EMC_NOT_FOUND		= ' EMC FW не найдено'
STR_DECRYPTING			= ' Расшифровка'
STR_ENCRYPTING			= ' Шифрование'
STR_PATCHING			= ' Исправление'
STR_EXPERIMENTAL		= ' * - эксперементальные функции'
STR_PERFORMED			= ' Выполнено действие: '

STR_EMPTY_FILE_LIST		= ' Список файлов пуст'
STR_NO_FOLDER			= ' Папка %s не существует'
STR_EXTRACTING			= ' Распаковка sflash0 в папку %s'
STR_FILES_CHECK			= ' Проверка файлов'
STR_BUILDING			= ' Сборка файла %s'

STR_DONE				= ' Готово'
STR_PROGRESS			= ' В процессе %02d%% '
STR_PROGRESS_KB			= ' Обработано: %dKB / %dKB'
STR_WAIT				= ' Подождите...'
STR_WAITING				= ' Ожидание...'
STR_SET_TO				= ' Для %s установлено значение [%s]'
STR_ABORT				= ' Действие отменено'
STR_FILENAME			= ' Имя файла: '

STR_VALIDATE_NVS_CHECK	= ' Проверка областей NVS'
STR_ACT_SLOT			= ' Активный слот: %s [0x%02X]'
STR_NIY					= ' Функция пока не разработана'
STR_CLEAN_FLAGS			= ' Очистить все системные флаги'
STR_UNK_FILE_TYPE		= ' Неизвестный тип файла'
STR_UNK_CONTENT			= ' Неизвестное содержимое'
STR_UART				= ' UART - '
STR_DEBUG				= ' Режим отладки Syscon (debug) - '

STR_DIFF_SLOT_VALUES	= ' Значения в слотах различаются!'
STR_SYSFLAGS_CLEAN		= ' Системные флаги были очищены. Совет: включите UART'
STR_SAMU_UPD			= ' Флаг SAMU - '
STR_DOWNGRADE_UPD		= ' Переключатель слота: '
STR_LAST_SC_ENTRIES		= ' Последние записи [%d/%d] активного блока [%d]'
STR_MEMCLOCK_SET		= ' Частота GDDR5 установлена в значение %dMHz [0x%02X]'

STR_RECOMMEND			= ' Рекомендуемый метод [%s]'
STR_PATCH_CANCELED		= ' Патч был отменён'
STR_PATCH_SUCCESS		= ' Записи удалены (%d шт.)'
STR_PATCH_SAVED			= ' Патч сохранён в %s'
STR_RENAMED				= ' Переименовано в %s'

STR_SC_BLOCK_SELECT		= ' Выберите блок [0-%d] | Показать Flat/Block [f] '
STR_MPATCH_INPUT		= ' Сколько записей очистить (с конца): '
STR_CHOICE				= ' Ваш выбор: '
STR_BACK				= ' Нажмите [ENTER] чтобы вернуться'
STR_MEMCLOCK_INPUT		= ' Выберите частоту [400 - 2000] / [0 по-умолчанию (0xFF)] MHz '
STR_SAMU_INPUT			= ' Настройте SAMU [0 - 255] / [по-умолчанию: 255 (0xFF)] '
STR_TOO_MUCH			= ' %d это много, максимум %d'
STR_SC_BLOCK_CLEANED	= ' Блок [%d] был полностью очищен'
STR_REBUILD_REQUIRED	= ' Сначала нужно пересобрать SNVS чтобы продолжить'
STR_SC_NO_BM			= ' Загрузочные режимы не были найдены!'

STR_UNPATCHABLE			= ' Невозможно пропатчить!'
STR_SYSCON_BLOCK		= ' Блок [%d/%d] имеет [%d/%d] запис(ей) | Активный - [%d]\n'
STR_PARTITIONS_CHECK	= ' Проверка разделов'
STR_ENTROPY				= ' Статистика по энтропии'
STR_MAGICS_CHECK		= ' Проверка сигнатур'
STR_DUPLICATES			= ' %d дубликатов найдено [%s]'
STR_SC_WARN_OVERWITTEN	= ' Внимание: CoreOS перезаписан - шанс на успех очень мал'

STR_SNVS_ENTRY_INFO		= 'Блок %d #%03d смещение 0x%04X'
STR_SC_TOGGLE_FLATDATA	= 'Переключить между Flat/Block'
STR_SH_DUPLICATES		= 'Показать / Скрыть дубли'
STR_NO_ENTRIES			= 'Записи не найдены'
STR_SKIPPED				= 'Пропущено'
STR_SKIP_ENTRY			= 'Пропустить этот тип записей'
STR_NO_FILE_SEL			= 'Файл не выбран'

STR_INCORRECT_SIZE		= ' %s неверный размер дампа!'
STR_FILE_NOT_EXISTS		= ' Файл %s не существует!'
STR_FILE_EXISTS			= ' Такой файл уже существует!'
STR_ERROR_FILE_REQ		= ' Сначала нужно выбрать файл'
STR_SAVED_TO			= ' Сохранено в %s'
STR_ERROR_INPUT			= ' Некорректный ввод'
STR_ERROR_DEF_VAL		= ' Сброс до значений по-умолчанию'
STR_ERROR_CHOICE		= ' Неправильный выбор'
STR_ERROR_INFO_READ		= ' Ошибка при чтении данных'
STR_OUT_OF_RANGE		= ' Значение вне диапазона!'
STR_FILES_MATCH			= ' Файлы одинаковые'
STR_FILES_MISMATCH		= ' Файлы отличаются'
STR_SIZES_MISMATCH		= ' Размеры отличаются!'
STR_RENAMED_COUNT		= ' %d файлов было переименовано'
STR_FW_RECORDS			= ' FW versions - from Current(1) to Initial(%d)'

STR_SELECT_MODEL		= ' Выберите модель:'
STR_SHOW_DETAILS		= ' Показать подробности?'
STR_Y_OR_CANCEL			= ' [y - да, * - отмена] '
STR_CHOOSE_AREA			= ' Выберите область: '
STR_INPUT_SEL_DUMP		= ' Выбрать второй дамп?'
STR_INPUT_DESTROY_PREV	= ' Стереть все предудыщие записи FW (08-0B)?'
STR_INPUT_BLOCK			= ' Введите начальный Блок [Количество]: '
STR_INPUT_SAVE_IM		= ' Сохранить все промежуточные файлы?'
STR_INPUT_USE_SLOTB		= ' Использовать слот B (активен)?'
STR_USE_NEWBLOBS		= ' Использовать новые ключи?'
STR_CONFIRM_SEPARATE	= ' Сохранить отдельно?'
STR_CONFIRM				= ' Введите [y] для подтверждения: '
STR_CURRENT				= ' Текущий: '
STR_GO_BACK				= ' Назад'
STR_SC_BM_SELECT		= ' Выберите режим загрузки [1-%d] '
STR_OPEN_IN_SC_TOOL		= ' Открыть файл в утилите для Syscon?'
STR_FLASH_FILE			= ' Записать файл обратно в чип?'

STR_READING_DUMP_N		= ' Считывание дампа %d'
STR_CHIP_NOT_RESPOND	= ' Чип не отвечает, проверьте провода и нажмите сброс'
STR_HOW_MUCH_DUMPS		= ' Сколько дампов считать? [максимум 10] '

STR_EMC_CMD_MODE		= 'Режим команд EMC: [%s]'
STR_SHOW_BYTECODES		= 'Показывать байткоды < 0x20: [%s]'
STR_MONITOR_STATUS		= 'RX/TX: %d/%d (байт) Прошло: %d (секунд)'

STR_CHIP_CONFIG			= ' Конфигурация чипа'
STR_FILE_INFO			= ' Информация о файле'
STR_VERIFY				= ' Верификация'

STR_SPW_PROGRESS		= 'Блок %03d [%d KB / %d KB] %d%% %s '
STR_SPW_ERROR_CHIP		= 'Неподдерживаемый чип!'
STR_SPW_ERROR_VERSION	= 'Неподдерживаемая версия! (требуется v%d.%02d)'
STR_SPW_ERROR_ERASE		= 'Ошибка при очистке чипа!'
STR_SPW_ERROR_ERASE_BLK	= 'Блок %d - ошибка очистки'
STR_SPW_ERROR_DATA_SIZE	= 'Неверный размер данных %d'
STR_SPW_ERROR_LENGTH	= 'Неверная длина данных %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Ошибка при проверке блока (block=%d)'
STR_SPW_ERROR_WRITE		= 'Ошибка при записи!'
STR_SPW_ERROR_READ		= 'Teensy превышена задержка приема! Переподключите Teensy!'
STR_SPW_ERROR_VERIFY	= 'Ошибка при проверке!'
STR_SPW_ERROR_PROTECTED	= 'Устройство защищено от записи!'
STR_SPW_ERROR_UNKNOWN	= 'Произошла неизвестная ошибка!'
STR_SPW_ERROR_UNK_STATUS= 'Неизвестный код статуса!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Размер файла должен быть кратен размеру блока: %d'
STR_SPW_ERR_DATA_SIZE	= 'Длина данных %d байт (ожидалось %d)!'
STR_SPW_ERR_OVERFLOW	= 'Чип содержит %d блоков. Невозможно записать более!'

STR_SCF_ERROR_VERSION	= 'Неподдерживаемая версия! (требуется v%d.%02d)'
STR_SCF_ERROR_WRITE_BLK	= 'Ошибка записи блока %d'
STR_SCF_ERROR_ERASE_BLK	= 'Ошибка очистки блока %d'
STR_SCF_ERROR_READ_BLK	= 'Ошибка чтения блока %d'
STR_SCF_ERROR_ERASE_CHIP= 'Ошибка при очистке чипа'

STR_SCF_ERR_INT			= 'Ошибка инициализации'
STR_SCF_ERR_READ		= 'Ошибка чтения'
STR_SCF_ERR_ERASE		= 'ошибка стирания'
STR_SCF_ERR_WRITE		= 'Ошибка записи'
STR_SCF_ERR_CMD_LEN		= 'Неверная длина команды'
STR_SCF_ERR_CMD_EXEC	= 'Ошибка исполнения команды'
STR_SCF_ERR_UNKNOWN		= 'Произошла неизвестная ошибка!'
STR_SCF_ERR_UNK_STATUS	= 'Неизвестный код статуса!'
STR_SCF_SAFE_ERASE		= ' Безопасная очистка с блока #%03d'

STR_CANT_USE			= 'Невозможно использовать'
STR_DIFF_SN				= 'Серийные номера отличаются!'
STR_SSP_EQUAL			= 'Шаблоны переключения одинаковые!'
STR_LP_FIRST_DUMP		= 'Первый дамп'
STR_LP_SECOND_DUMP		= 'Второй дамп'

STR_CONVERTING_S28		= ' Конвертирование в формат S28'
STR_S28_ALREADY			= ' Формат файла S28'

STR_USE_EXPERT_M		= ' Выберите другую модель или используйте режим эксперта!'
STR_ERR_NO_FW_FOUND		= ' Ошибка: Невозможно найти %s для FW %s в базе данных'
STR_EXPERT_MODE			= ' Режим эксперта?'
STR_SELECT_FW_VER		= ' Выберите версию FW'
STR_MODEL				= ' Модель'
STR_FW_VER				= ' FW: %s / Слот: %s'
STR_SELECT_MOST_FILE	= ' Выберите самый подходящий файл: '
STR_NO_FW_FILES			= ' Файлы не найдены! Загрузите файлы в папку fws:\n [%s]'

STR_ABOUT_SC_REBUILDER = 'Об утилите Syscon Rebuilder'
STR_INFO_SC_REBUILDER = ''\
' Утилита для создания кастомной сборки Syscon.\n'\
' В режиме эксперта можно настроить все типы записей.\n'\
' Записи отсортированы от текущей до первоначальной.\n'\
' * Чтобы выбрать предыдущее ПО введите "2" или больше.\n'\
' * Минимальный набор состоит из 3 типов (00-03 + 04-07 + 08-0B)'

STR_ABOUT_RL78FLASH = 'О стоковом Syscon'
STR_INFO_RL78FLASH = ''\
' Позволяет прошить новый чистый чип (Renesas RL78G10)\n'\
' Требуется адаптер USB2TTL, провода и пара диодов.\n'\
' Схема подключения в папке assets/hw/l78flash'\

STR_ABOUT_NVS = 'О восстановлении NVS'
STR_INFO_NVS = ''\
' Замена поврежденного блока на бекап (отсутствует в 10xx/11xx)\n'\
' Внимание - UART и прочие флаги могут быть перезаписаны.\n'\
' Если требется установить флаги, делать после восстановления NVS!\n'\

STR_ABOUT_TORUS_PATCH = 'О замене ПО WiFi'
STR_INFO_TORUS_PATCH = ''\
' Будет полезно в следующих случаях:\n'\
' - поверждение ПО Torus-а (WiFi+BT)\n'\
' - переход на другой чип'\

STR_ABOUT_SB_PATCH = 'О замене ПО Южного Моста'
STR_INFO_SB_PATCH = ''\
' Будет полезно в следующих случаях:\n'\
' - поврежденное ПО ЮМ или ошибки "EMC VERSION DOWN"\n'\
' - переход на другой чип (CXD90046 => CXD90036)\n'\
' - замена процессорной связки (21xx => 22xx, 71xx => 72xx)'

STR_INFO_FLASH_TOOLS = ''\
' Утилиты spiway & syscon flasher экспериментальные! Будьте осторожны.'\

STR_ABOUT_PART_RECOVERY = 'Анализ и восстановление разделов'
STR_INFO_PART_A_R = ''\
' По-байтово сравнивает данныые раздела с рабочими файлами\n'\
' и показывает процент схожести.\n'\
' Самый похожий файл будет в верху списка.\n'\
' Имейте ввиду прошивка ЮМ состоит из emc + eap'

STR_INFO_FW_LINK = ''\
' Рабочие файлы emc/eap/torus положите в папку /fws/\n'\
' Скачать можно из данного репозитория:\n '

STR_ABOUT_LEG_PATCH = 'Об официальном (legit) патче CoreOS'
STR_INFO_LEG_PATCH = ''\
' Подходит только для рабочих консолей!\n'\
' Т.к. нужно обновиться через Безопасный режим PS4\n'\
'\n'\
' 1) Считываем первый дамп (если еще не сделали)\n'\
' 2) Обновляем через безопасный режим на эту же версию ПО\n'\
' 3) Считываем второй лдамп (в обоих слотах одинаковое ПО)\n'\
'\n'\
' Теперь можно пропатчить первый дамп данными из второго\n'\
' Можно просто перенести 2 дампа на ярлык WeeTools'

STR_ABOUT_SCF = 'О программаторе Syscon'
STR_INFO_SCF = ''\
' Позволяет считывать/записывать оригинальный чип сискон\n'\
' Поддерживаются только модели A0x-COLx - (RL78/G13)\n'\
' В роли программатора используются платы Teensy (2.0++/4.0/4.1)\n'\
' Диаграмы подключения и прошивки в папке </assets/hw/syscon_flasher>\n'\
' Подробнее: '

STR_ABOUT_SPIWAY = 'О программаторе SPIway'
STR_INFO_SPIWAY = ''\
' SPIway - ч/з sflash с доступом к рандомному блоку (Teensy++ 2.0)\n'\
' Диаграмы подключения и прошивки в папке </assets/hw/spiway>\n'\
' Подробнее на PSDevWiki: '

STR_ABOUT_SC_GLITCH = 'О глитче Syscon'
STR_INFO_SC_GLITCH = ''\
' Считывание через (Arduino Nano V3 CH340) автор - DarkNESmonk\n'\
' Диаграмы подключения и прошивки в папке </assets/hw/syscon_reader>'

STR_ABOUT_SC_BOOTMODES = 'О режимах загрузки'
STR_INFO_SC_BOOTMODES = ''\
' Т.к. записи защифрованы невозможно определить что в них хранится\n'\
' Вам придется попробывать все по-очереди, чтобы найти нужную\n'\
' Некоторые записи могут иметь дубли (помечены цветом)'

STR_OVERCLOCKING = ''\
' Внимание - Опасная операция!\n\n'\
' Частота GDDR5 - 6000-8000 MHz. Множитель - [x4]\n'\
' GDDR5 8000 MHz технически работает на 2000 MHz\n'\
' Если есть проблемы устанавливайте 1000 MHz\n'\
'\n'\
' Эффективная частота GDDR5 - 1350 MHz\n'\
' Частоту подбираем эксперементально\n'\
' - Слишком высокая приведет к ошибкам LOADBIOS -8 или DCT [*]\n'\
' - Слишком низкая приведет к ошибке AMDINIT'

STR_ABOUT_EAPKEYS = 'О ключах EAP'
STR_INFO_EAPKEYS = ''\
' Ключ EAP бывает длиной 0x40 и 0x60 байт\n'\
' В моделях PS4 10xx/11xx нет бекапа NVS\n'\
' В 12xx/Slim/PRO есть бекап, в том числе и ключа\n'\

STR_IMMEDIATLY = ''\
' Осторожно: Все изменения применяются сразу к файлу!'

STR_PATCHES = STR_IMMEDIATLY + '\n'\
' Переключает значение выбранной опции среди доступных'

STR_DOWNGRADE = ''\
' Опасная операция!\n\n'\
' Переключение слота возвращает предыдущую версию ПО.\n'+\
' Также откат помогает вылечить ошибки "LOADBIOS".\n'\
' Обязательно сохраните первоначальные дампы sFlash и Syscon.\n'\
' После переключения нужно патчить Syscon! Заранее убедитесь что сможете.\n'\
' Без этого консоль не загрузится!'

STR_ABOUT_MPATCH = 'О ручном патчинге'
STR_INFO_SC_MPATCH = ''\
' Каждая запись состоит из 16 байт. Первый всегда "A5"\n'\
' Второй байт отвечает за "тип" обычно в диапазоне [0x00-0x30]\n'\
' Каждые 4 записи формируют 1 структуру, например для ПО это %s\n'\
' Для удаления нужно затереть структуру (4 записи) символами 0xFF\n'\
' Если есть структуры (%s,%s) после ПО (%s), то откат невозможен\n'\
' слот с бекапом уже перезаписан, получите ошибку checkUpdVersion'

STR_ABOUT_EAP = 'О ключах EAP'
STR_INFO_HDD_EAP = ''\
' С помощью данных ключей можно открыть PS4 HDD на ПК\n'\
' Дополнительная информация по ссылке:\n '\

STR_ABOUT_EMC_CFW = 'О кастомной прошивке EMC'
STR_INFO_EMC_CFW = ''\
' Используйте на свой страх и риск!\n'\
' Подходит только для Aeolia (PS4 Fat 10xx/11xx)\n'\
' Предоставлет неограниченный доступ к ЮМ и syscon\n\n'\
' Дополнительная информация:\n '

STR_APP_HELP = ''\
' Пример: ps4-wee-tools [параметры] \n'\
'\n'\
' Параметры: \n\n'\
'  <file>              : откроет нужную утилиту для данного файла\n'\
'  <folder>            : собрать дамп sFlash из файлов в этой папке\n'\
'  <file1> <file2> ... : сравнение файлов (с хешами MD5)\n'\
'  --help              : открыть эту справку\n'\
'\n'\
' Домашняя страница: '
