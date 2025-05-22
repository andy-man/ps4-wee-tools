#==========================================================
# Polish language [PL]
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================

MENU_SC_REBUILD_MODES = [
	'Tryb normalny (Wybierz FW, domyślne wartości dla reszty / Wszystkie (12) typy)',
	'Minimalna konfiguracja (Wybierz pierwsze dwa typy i FW / 3 typy)',
	'Tryb eksperta (Dostosuj wszystkie (12) typy)',
]

MENU_NVS_COPY = [
	'Zastąp %s kopią zapasową (%s <= %s)',
	'Zastąp kopię zapasową %s (%s => %s)',
]

MENU_EAP_KEYS = [
	'Zastąp A przez B (key_a <= key_b)',
	'Zastąp B przez A (key_a => key_b)',
	'Napraw magic A *',
	'Napraw magic B *',
	'Wygeneruj nowe klucze A, B (długość 0x60) *',
	'Wygeneruj nowe klucze A, B (długość 0x40) *',
	'Wyczyść klucz B *',
]

MENU_FLASHER = [
	'Odczytaj wszystko',
	'Odczytaj obszar',
	'Odczytaj blok',
	'Zapisz wszystko',
	'Zapisz obszar',
	'Zapisz blok',
	'Zweryfikuj wszystko',
	'Zweryfikuj obszar',
	'Zweryfikuj blok',
	'Wymaż wszystko',
	'Wymaż obszar',
	'Wymaż blok',
]

MENU_SERIAL_MONITOR = {
	'Ctrl+Q':'Wyjdź z monitora',
	'Ctrl+R':'Zrestartuj monitor',
	'Ctrl+E':'Przełącz tryb EMC cmd',
	'Ctrl+B':'Pokaż bajtkody < 0x20',
	'Ctrl+L':'Zapisuj log do pliku',
}

MENU_TOOL_SELECTION = [
	'Przeglądarka plików',
	'Terminal (UART)',
	'sFlash r/w (SPIway by Judges)',
	'Syscon r/w (SCTool by Abkarino & EgyCnq)',
	'Syscon r/o (SCRead by DarkNESmonk)',
	'Syscon w/o (Dla oryginalnego Renesas RL78)',
	'Zmień język aplikacji',
	'Wyjdź',
]

MENU_FILE_SELECTION = {
	'a':'Pokaż wszystkie pliki / Przełącz filtry [bin,pup]',
	'f':'Zbuduj zrzut sflash0',
	'b':'Zbuduj 2BLS/PUP',
	'r':'Zbiorcza zmiana nazw (Wyciągnij informacje ze zrzutu do nazwy pliku)',
	'c':'Porównaj pliki w bieżącym folderze',
	'q':'Wyjdź / Wróć',
}

MENU_EXTRA_FLASHER = {
	's':'Wybierz plik',
	'f':'Uruchom narzędzie dla tego pliku',
	'q':'Wyjdź / Wróć',
}

MENU_EXTRA = {
	's':'Wybierz inny plik',
	'f':'Zaflashuj ten plik (cały/częściowo) z powrotem do IC',
	'r':'Zmień nazwę pliku na nazwę kanoniczną',
	'q':'Wyjdź / Wróć',
}

MENU_SFLASH_ACTIONS = [
	'Flagi (UART, RNG, Memtest, itp.)',
	'Zegar pamięci (GDDR5)',
	'Flaga rozruchu SAMU',
	'Przełącz CoreOS slot (przywrócenie FW)',
	'Legalny patch CoreOS',
	'Patch Southbridge',
	'Patch Torus (WiFi+BT)',
	'Dodatkowe narzędzia',
]

MENU_SFLASH_ADV_ACTIONS = [
	'Wyodrębnij partycje z sFlash0',
	'Zbuduj sFlash0 z wyodrębnionych plików',
	'Wyświetl / Odzyskaj obszary NVS (1C9, 1CA)',
	'Wyświetl / Odzyskaj klucz EAP',
	'Pobierz klucze HDD = odszyfruj klucz EAP = utwórz [keys.bin]',
	'Utwórz EMC cfw (tylko dla Fat 1xxx/11xx)',
	'Walidacja bazowa i statystyki entropii',
	'Analiza i odzyskiwanie uszkodzonej partycji',
]

MENU_SC_ACTIONS = [
	'Przełącz tryb debugowania',
	'Automatyczny patch SNVS',
	'Podgląd bloku SNVS',
	'Podgląd bloku NVS',
	'Ręczny patch SNVS',
	'Dodatkowe narzędzia',
]

MENU_SC_ADV_ACTIONS = [
	'Zresetuj liczniki SNVS',
	'Wybór trybu (00-03)',
	'Tryby rozruchu (04-07)',
	'Odbuduj SNVS Syscona (Przywracanie fabryczne)',
	'Odzyskaj FW Syscona',
	'Konwertuj na flasher Renesas (Motorola S28)',
]

MENU_PATCHES = [
	'Metoda A - ostatnie 08-0B zostaną usunięte (4 rekordy)',
	'Metoda B - ostatnie 08-0B i poniżej zostaną wyczyszczone (%d rekordów)',
	'Metoda C - wyczyść wszystko poniżej poprzedniego 08-0B (%d rekordów)',
	'Metoda D - wyczyść wszystko poniżej ostatniego 08-0B (%d rekordów)',
	'Metoda E - wyczyść poprzednie 08-0B i poniżej (%d rekordów)',
]

MENU_SC_STATUSES = [
	'Nadpisany slot CoreOs',
	'Możliwy do patchowania',
	'Już spatchowany lub utknął na aktualizacji',
	'Prawdopodobnie możliwy do patchowania',
]

MENU_SPW_ACTS = {
	'read':		'Odczytywanie',
	'write':	'Zapis',
	'verify':	'Weryfikacja',
	'erase':	'Wymazywanie',
}

STR_LANGUAGE			= 'Język'
STR_SECONDS				= '%0.0f sekund'
STR_NVS_AREAS			= 'Obszary NVS'
STR_PORTS_LIST			= 'Lista portów szeregowych'
STR_MAIN_MENU			= 'Główne menu'
STR_FILE_LIST			= 'Lista plików'
STR_SFLASH_INFO			= 'Informacje o zrzucie sFlash'
STR_ADDITIONAL			= 'Dodatkowe narzędzia'
STR_SYSCON_INFO			= 'Informacje o zrzucie Syscona'
STR_COMPARE				= 'Porównaj'
STR_HELP				= 'Pomoc'
STR_ACTIONS				= 'Akcje'
STR_COREOS_SWITCH		= 'Przełączanie slotu CoreOS'
STR_SWITCH_PATTERNS		= 'Wzorce przełączania'
STR_MEMCLOCK			= 'Zegar pamięci'
STR_SAMU_BOOT			= 'Rozruch SAMU'
STR_SYSFLAGS			= 'Flagi systemowe'
STR_NVS_ENTRIES			= 'Wpisy Syscona %s'
STR_APATCH_SVNS			= 'Automatyczne patchowanie SNVS'
STR_MPATCH_SVNS			= 'Ręczny patch SNVS'
STR_SFLASH_VALIDATOR	= 'Walidator sFlash'
STR_SFLASH_FLAGS		= 'Flagi sFlash'
STR_SFLASH_EXTRACT		= 'Wyciąganie sFlash'
STR_SFLASH_BUILD		= 'Budowanie sFlash'
STR_HDD_KEY				= 'Klucz EAP HDD'
STR_2BLS_BUILDER		= 'Budowanie 2BLS'
STR_UNPACK_2BLS			= 'Rozpakowywanie 2BLS'
STR_UNPACK_PUP			= 'Rozpakowywanie odszyfrowanego PUP'
STR_EMC_CFW				= 'EMC CFW (Aeolia)'
STR_EAP_KEYS			= 'Klucze EAP'
STR_SC_BOOT_MODES		= 'Rekordy trybów rozruchu'
STR_INFO				= 'Informacje'
STR_SC_READER			= 'Czytnik Syscona'
STR_SPIWAY                = 'SPIway autorstwa Judges & Abkarino'
STR_SCF                   = 'Syscon Flasher autorstwa Abkarino & EgyCnq'
STR_LEG_PATCH             = 'Legalny patch CoreOS'
STR_PART_RECOVERY         = 'Odzyskiwanie partycji'
STR_PART_ANALYZE          = 'Analiza partycji'
STR_PART_LIST             = 'Lista partycji'
STR_PARTS_INFO            = 'Informacje o partycjach'
STR_WIFI_PATCHER          = 'Patch WiFi'
STR_SB_PATCHER            = 'Patch Southbridge'
STR_RL78FLASH             = 'Programator RL78'
STR_SC_REBUILDER          = 'Odbudowa Syscon'

STR_ALL                   = 'Wszystko'
STR_UNIQUE                = 'Unikalny'
STR_BACKUP                = 'Kopia zapasowa'
STR_EQUAL                 = 'Równy'
STR_NOT_EQUAL             = 'Nie równy'
STR_NO_INFO               = '- Brak informacji -'
STR_OFF                   = 'Wyłączony'
STR_ON                    = 'Włączony'
STR_WARNING               = 'Ostrzeżenie'
STR_HELP                  = 'Pomoc'
STR_UNKNOWN               = '- Nieznany -'
STR_YES                   = 'Tak'
STR_NO                    = 'Nie'
STR_PROBABLY              = 'Prawdopodobnie'
STR_NOT_SURE              = 'Niepewny'
STR_DIFF                  = 'Różny'
STR_NOT_FOUND             = 'Nie znaleziono'
STR_BAD_SIZE              = 'Niepoprawny rozmiar'
STR_OK                    = 'OK'
STR_FAIL                  = 'Niepowodzenie'
STR_CANCEL                = 'Anuluj'
STR_IS_PART_VALID         = '[%s] %s FW %s'
STR_SNVS_ENTRIES          = 'Znaleziono %d wpisów pod adresem 0x%05X'
STR_SERIAL_MONITOR        = 'Terminal'
STR_ELAPSEDTIME           = 'Czas trwania'

STR_NO_PORT_CHOSEN        = ' Nie wybrano portu'
STR_NO_PORTS              = ' Nie znaleziono żadnego portu szeregowego'
STR_PORT_UNAVAILABLE      = ' Wybrany port jest niedostępny'
STR_PORT_CLOSED           = ' Port jest zamknięty'
STR_STOP_MONITORING       = ' Monitorowanie zostało zatrzymane przez użytkownika'

STR_RESTART_APP           = ' Uruchom ponownie aplikację, aby zastosować zmiany'
STR_GENERATE_ALL_PS       = ' Generuj wszystkie patche'
STR_ACTION_NA             = ' Brak dostępnej akcji %s'
STR_EMC_CFW_WARN          = ' Obecnie EMC CFW jest tylko dla PS4 Fat 10xx/11xx'
STR_EMC_NOT_FOUND         = ' Nie znaleziono oprogramowania EMC'
STR_DECRYPTING            = ' Odszyfrowywanie'
STR_ENCRYPTING            = ' Szyfrowanie'
STR_PATCHING              = ' Patchowanie'
STR_EXPERIMENTAL          = ' * - funkcje eksperymentalne'
STR_PERFORMED             = ' Wykonano akcję: '

STR_EMPTY_FILE_LIST       = ' Lista plików jest pusta'
STR_NO_FOLDER             = ' Folder %s nie istnieje'
STR_EXTRACTING            = ' Rozpakowywanie sflash0 do folderu %s'
STR_FILES_CHECK           = ' Sprawdzanie plików'
STR_BUILDING              = ' Tworzenie pliku %s'

STR_DONE                  = ' Wszystko gotowe'
STR_PROGRESS              = ' Postęp %02d%% '
STR_PROGRESS_KB           = ' Postęp: %dKB / %dKB'
STR_WAIT                  = ' Proszę czekać...'
STR_WAITING               = ' Oczekiwanie...'
STR_SET_TO                = ' %s został ustawiony na [%s]'
STR_ABORT                 = ' Akcja została przerwana'
STR_FILENAME              = ' Nazwa pliku: '

STR_VALIDATE_NVS_CHECK    = ' Sprawdzanie obszarów NVS'
STR_ACT_SLOT              = ' Aktywny slot: %s [0x%02X]'
STR_NIY                   = ' Ta funkcja jest dostępna tylko w wersji PRO'
STR_CLEAN_FLAGS           = ' Wyczyść wszystkie flagi systemowe'
STR_UNK_FILE_TYPE         = ' Nieznany typ pliku'
STR_UNK_CONTENT           = ' Nieznana zawartość'
STR_UART                  = ' UART został ustawiony na '
STR_DEBUG                 = ' Debugowanie Syscon ustawione na '

STR_DIFF_SLOT_VALUES      = ' Wartości w slotach są różne!'
STR_SYSFLAGS_CLEAN        = ' Flagi systemowe zostały wyczyszczone. Wskazówka: włącz UART'
STR_SAMU_UPD              = ' Flaga SAMU została ustawiona na '
STR_DOWNGRADE_UPD         = ' Przełącznik slotów został ustawiony na: '
STR_LAST_SC_ENTRIES       = ' Wyświetlanie ostatnich [%d/%d] wpisów z aktywnego bloku [%d]'
STR_MEMCLOCK_SET          = ' Częstotliwość GDDR5 została ustawiona na %dMHz [0x%02X]'

STR_RECOMMEND             = ' Zalecana metoda [%s]'
STR_PATCH_CANCELED        = ' Patch został anulowany'
STR_PATCH_SUCCESS         = ' Pomyślnie usunięto %d wpisów'
STR_PATCH_SAVED           = ' Patch zapisany do %s'
STR_RENAMED               = ' Zmieniono nazwę na %s'

STR_SC_BLOCK_SELECT       = ' Wybierz blok danych [0-%d] | Widok Płaski/Blok [f] '
STR_MPATCH_INPUT          = ' Ile wpisów wyczyścić (od końca): '
STR_CHOICE                = ' Dokonaj wyboru: '
STR_BACK                  = ' Naciśnij [ENTER], aby wrócić'
STR_MEMCLOCK_INPUT        = ' Ustaw częstotliwość [400 - 2000] / [0 ustaw domyślną (0xFF)] MHz '
STR_SAMU_INPUT            = ' Ustaw SAMU [0 - 255] / [domyślna to 255 (0xFF)] '
STR_TOO_MUCH              = ' %d to za dużo, maksymalna wartość to %d'
STR_SC_BLOCK_CLEANED      = ' Blok [%d] został całkowicie wyczyszczony'
STR_OWC_RESET_REQUIRED    = ' Najpierw musisz zresetować liczniki SNVS, aby wykonać tę akcję'
STR_SC_NO_BM              = ' Nie znaleziono zapisów trybu rozruchu!'

STR_UNPATCHABLE           = ' Nie można patchować!'
STR_SYSCON_BLOCK          = ' Blok [%d/%d] zawiera [%d/%d] wpisów | Aktywny blok to [%d]\n'
STR_PARTITIONS_CHECK      = ' Sprawdzanie partycji'
STR_ENTROPY               = ' Statystyki entropii'
STR_MAGICS_CHECK          = ' Sprawdzanie magii'
STR_DUPLICATES            = ' Znaleziono %d duplikat(ów) [%s]'
STR_SC_WARN_OVERWITTEN    = ' Ostrzeżenie: CoreOS prawdopodobnie został nadpisany'

STR_SNVS_ENTRY_INFO       = 'Blok %d #%03d Offset 0x%04X'
STR_SC_TOGGLE_FLATDATA    = 'Przełącz między Płaskim/Blokowym'
STR_SH_DUPLICATES         = 'Pokaż / Ukryj duplikaty'
STR_NO_ENTRIES            = 'Nie znaleziono wpisów'
STR_SKIPPED               = 'Pominięte'
STR_SKIP_ENTRY            = 'Pomiń ten typ wpisu'
STR_NO_FILE_SEL           = 'Nie wybrano pliku'

STR_INCORRECT_SIZE		= ' %s ma niepoprawny rozmiar dumpa!'
STR_FILE_NOT_EXISTS		= ' Plik %s nie istnieje!'
STR_FILE_EXISTS			= ' Nazwa pliku już istnieje!'
STR_ERROR_FILE_REQ		= ' Najpierw musisz wybrać plik'
STR_SAVED_TO			= ' Zapisano do %s'
STR_ERROR_INPUT			= ' Niepoprawne dane wejściowe'
STR_ERROR_DEF_VAL		= ' Ustawianie wartości domyślnych'
STR_ERROR_CHOICE		= ' Nieprawidłowy wybór'
STR_ERROR_INFO_READ		= ' Błąd podczas odczytu danych z pliku'
STR_OUT_OF_RANGE		= ' Wartość jest poza zakresem!'
STR_FILES_MATCH			= ' Pliki są identyczne'
STR_FILES_MISMATCH		= ' Pliki się różnią'
STR_SIZES_MISMATCH		= ' Rozmiary się różnią!'
STR_RENAMED_COUNT		= ' %d plików zostało przemianowanych'
STR_FW_RECORDS			= ' Wersje FW - od bieżącej(1) do początkowej(%d)'

STR_SELECT_MODEL		= ' Wybierz model:'
STR_SHOW_DETAILS		= ' Pokaż szczegóły?'
STR_Y_OR_CANCEL			= ' [y - tak, * - anuluj]'
STR_CHOOSE_AREA			= ' Wybierz obszar: '
STR_INPUT_SEL_DUMP		= ' Wybrać drugi dump?'
STR_INPUT_DESTROY_PREV	= ' Zniszczyć wszystkie wcześniejsze rekordy FW (08-0B)?'
STR_INPUT_BLOCK			= ' Podaj blok startowy [ilość]: '
STR_INPUT_SAVE_IM		= ' Zapisz wszystkie pliki pośrednie?'
STR_INPUT_USE_SLOTB		= ' Użyć slotu B (aktywnego)?'
STR_USE_NEWBLOBS		= ' Użyć nowych kluczy blob?'
STR_CONFIRM_SEPARATE	= ' Zapisz jako osobny plik?'
STR_CONFIRM				= ' Wprowadź [y], aby kontynuować:'
STR_CURRENT				= ' Bieżący:'
STR_GO_BACK				= ' Wróć'
STR_SC_BM_SELECT		= ' Wybierz wariant trybu rozruchu [1-%d]'
STR_OPEN_IN_SC_TOOL		= ' Otworzyć plik w narzędziu Syscon?'
STR_FLASH_FILE			= ' Wgrać ten plik na IC?'

STR_READING_DUMP_N		= ' Odczytywanie dumpa %d'
STR_CHIP_NOT_RESPOND	= ' Chip nie odpowiada, sprawdź okablowanie i naciśnij przycisk reset'
STR_HOW_MUCH_DUMPS		= ' Ile dumpów odczytać? [maks. 10]'

STR_EMC_CMD_MODE		= 'Włączanie trybu EMC cmd: [%s]'
STR_SHOW_BYTECODES		= 'Pokaż kody bajtowe < 0x20: [%s]'
STR_MONITOR_STATUS		= 'RX/TX: %d/%d (bajtów) Czas: %d (sek)'

STR_CHIP_CONFIG			= ' Konfiguracja chipa'
STR_FILE_INFO			= ' Informacje o pliku'
STR_VERIFY				= ' Weryfikuj'

STR_SPW_PROGRESS		= 'Blok %03d [%d KB / %d KB] %d%% %s'
STR_SPW_ERROR_CHIP		= 'Nieobsługiwany chip!'
STR_SPW_ERROR_VERSION	= 'Nieobsługiwana wersja! (wymagana v%d.%02d)'
STR_SPW_ERROR_ERASE		= 'Błąd podczas wymazywania chipa!'
STR_SPW_ERROR_ERASE_BLK	= 'Blok %d - błąd wymazywania'
STR_SPW_ERROR_DATA_SIZE	= 'Niepoprawny rozmiar danych %d'
STR_SPW_ERROR_LENGTH	= 'Niepoprawna długość %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Błąd! Weryfikacja bloku nie powiodła się (blok=%d)'
STR_SPW_ERROR_WRITE		= 'Błąd podczas zapisu!'
STR_SPW_ERROR_READ		= 'Przekroczony czas odbioru Teensy! Odłącz i ponownie podłącz Teensy!'
STR_SPW_ERROR_VERIFY	= 'Błąd weryfikacji!'
STR_SPW_ERROR_PROTECTED	= 'Urządzenie jest chronione przed zapisem!'
STR_SPW_ERROR_UNKNOWN	= 'Odebrano nieznany błąd!'
STR_SPW_ERROR_UNK_STATUS= 'Nieznany kod statusu!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Oczekiwano, że rozmiar pliku będzie wielokrotnością rozmiaru bloku: %d'
STR_SPW_ERR_DATA_SIZE	= 'Dane mają długość %d bajtów (oczekiwano %d)!'
STR_SPW_ERR_OVERFLOW	= 'Chip ma %d bloków. Zapis wykracza poza pojemność chipa!'

STR_SCF_ERROR_VERSION	= 'Nieobsługiwana wersja! (wymagana v%d.%02d)'
STR_SCF_ERROR_WRITE_BLK	= 'Błąd zapisu bloku %d'
STR_SCF_ERROR_ERASE_BLK	= 'Błąd wymazywania bloku %d'
STR_SCF_ERROR_READ_BLK	= 'Błąd odczytu bloku %d'
STR_SCF_ERROR_ERASE_CHIP= 'Błąd podczas wymazywania chipa'

STR_SCF_ERR_INT			= 'Błąd podczas inicjalizacji'
STR_SCF_ERR_READ		= 'Błąd odczytu'
STR_SCF_ERR_ERASE		= 'Błąd wymazywania'
STR_SCF_ERR_WRITE		= 'Błąd zapisu'
STR_SCF_ERR_CMD_LEN		= 'Niepoprawna długość polecenia'
STR_SCF_ERR_CMD_EXEC	= 'Błąd podczas wykonywania polecenia'
STR_SCF_ERR_UNKNOWN		= 'Otrzymano nieznany błąd!'
STR_SCF_ERR_UNK_STATUS	= 'Nieznany kod statusu!'
STR_SCF_SAFE_ERASE		= ' Bezpieczne wymazywanie rozpoczyna się od bloku #%03d'

STR_CANT_USE			= 'Nie można tego użyć'
STR_DIFF_SN				= 'Numery seryjne są różne!'
STR_SSP_EQUAL			= 'Wzory przełączania slotów są identyczne!'
STR_LP_FIRST_DUMP		= 'Pierwszy dump'
STR_LP_SECOND_DUMP		= 'Drugi dump'

STR_CONVERTING_S28		= ' Konwertowanie do formatu S28'
STR_S28_ALREADY			= ' Format pliku to już S28'

STR_USE_EXPERT_M		= ' Wybierz inny model lub użyj trybu eksperckiego!'
STR_ERR_NO_FW_FOUND		= ' Błąd: Nie można znaleźć %s dla FW %s w DB'
STR_EXPERT_MODE			= ' Tryb ekspercki?'
STR_SELECT_FW_VER		= ' Wybierz wersję FW'
STR_MODEL				= ' Model'
STR_FW_VER				= ' FW: %s / Slot: %s'
STR_SELECT_MOST_FILE	= ' Wybierz najbardziej odpowiedni plik:'
STR_NO_FW_FILES			= ' Pliki nie zostały znalezione! Pobierz pliki do folderu fws:\n [%s]'

STR_ABOUT_SC_REBUILDER = 'O programie Syscon Rebuilder'
STR_INFO_SC_REBUILDER = ''\
' To narzędzie pomoże Ci stworzyć niestandardową wersję Syscon.\n'\
' Możesz dostosować każdy typ rekordów w trybie eksperckim.\n'\
' Wpisy są posortowane od bieżących do przeszłych.\n'\
' * Aby wybrać wcześniejsze FW, musisz wprowadzić "2" lub więcej.\n'\
' * Minimalna konfiguracja składa się z 3 typów (00-03 + 04-07 + 08-0B)'

STR_ABOUT_RL78FLASH = 'O programie Stock Syscon'
STR_INFO_RL78FLASH = ''\
' Aby zaprogramować nowy, pusty chip syscon (Renesas RL78G10)\n'\
' potrzebujesz adaptera USB na TTL, przewodów i kilku diod.\n'\
' Schemat okablowania znajduje się w folderze assets/hw/l78flash'

STR_ABOUT_NVS = 'O odzyskiwaniu NVS'
STR_INFO_NVS = ''\
' Zamienia uszkodzony blok na dane kopii zapasowej (nie dotyczy modeli 10xx/11xx)\n'\
' Ostrzeżenie - UART i inne flagi mogą zostać nadpisane.\n'\
' Jeśli potrzebujesz ustawić jakieś flagi, zrób to po przywróceniu NVS!\n'\

STR_ABOUT_TORUS_PATCH = 'O patcherze WiFi'
STR_INFO_TORUS_PATCH = ''\
' Przydatne w przypadku:\n'\
' - uszkodzonego FW Torus (WiFi+BT)\n'\
' - przełączania na inny moduł IC'\

STR_ABOUT_SB_PATCH = 'O patcherze Southbridge'
STR_INFO_SB_PATCH = ''\
' Przydatne w przypadku:\n'\
' - uszkodzonego FW Southbridge lub błędów "EMC VERSION DOWN"\n'\
' - przełączania na inny moduł IC (CXD90046 => CXD90036)\n'\
' - wymiany zestawów APU (21xx => 22xx, 71xx => 72xx)'

STR_INFO_FLASH_TOOLS = ''\
' Narzędzia do flashowania (spiway & syscon flasher) są eksperymentalne! Bądź ostrożny.'\

STR_ABOUT_PART_RECOVERY = 'O analizie i odzyskiwaniu partycji'
STR_INFO_PART_A_R = ''\
' Porównuje każdy bajt partycji (SFlash/Syscon) z prawidłowymi plikami\n'\
' i pokazuje procent podobieństwa.\n'\
' Najbardziej podobne pliki będą na górze listy.\n'\
' Pamiętaj, że FW Southbridge składa się z emc + eap'

STR_INFO_FW_LINK = ''\
' Umieść prawidłowe pliki emc/eap/torus/syscon w folderze /fws/\n'\
' Możesz je pobrać z tego repozytorium:\n '

STR_ABOUT_LEG_PATCH = 'O Patchu Legitimate CoreOS'
STR_INFO_LEG_PATCH = ''\
' Ta metoda jest odpowiednia tylko dla działających konsol!\n'\
' Wymaga aktualizacji przez tryb bezpieczny PS4\n'\
'\n'\
' 1) Odczytaj pierwszy zrzut (jeśli jeszcze tego nie zrobiłeś)\n'\
' 2) Zaktualizuj konsolę do TEJ SAMEJ wersji przez tryb bezpieczny\n'\
' 3) Odczytaj drugi zrzut (oba sloty mają równą wersję FW)\n'\
'\n'\
' Teraz możesz zaaplikować łatkę do pierwszego zrzutu przy użyciu danych z drugiego\n'\
' Możesz przeciągnąć i upuścić 2 zrzuty na skrót narzędzia wee-tools, aby przyspieszyć'

STR_ABOUT_SCF = 'O Syscon Flasher'
STR_INFO_SCF = ''\
' Syscon Flasher umożliwia odczyt/zapis oryginalnego chipa PS4 syscon (RL78/G13)\n'\
' Flasher obsługuje tylko modele syscon A0x-COLx\n'\
' Część sprzętowa opiera się na płytkach Teensy (2.0++/4.0/4.1)\n'\
' Diagramy i FW dla Teensy znajdziesz w </assets/hw/syscon_flasher>\n'\
' Więcej informacji tutaj: '

STR_ABOUT_SPIWAY = 'O SPIway'
STR_INFO_SPIWAY = ''\
' SPIway - odczyt/zapis sflash z obsługą losowego dostępu do bloków (Teensy++ 2.0)\n'\
' Diagramy i FW dla Teensy znajdziesz w folderze </assets/hw/spiway>\n'\
' Więcej informacji na PSDevWiki: '

STR_ABOUT_SC_GLITCH = 'O Syscon Glitch'
STR_INFO_SC_GLITCH = ''\
' Czytnik Syscon autorstwa DarkNESmonk (Arduino Nano V3 CH340)\n'\
' Więcej informacji znajdziesz w folderze </assets/hw/syscon_reader>'

STR_ABOUT_SC_BOOTMODES = 'O trybach bootowania'
STR_INFO_SC_BOOTMODES = ''\
' Rekordy trybu bootowania są zaszyfrowane, więc nie możemy wykryć ich przeznaczenia\n'\
' Powinieneś wypróbować każdy z nich samodzielnie, aby określić, do czego służy\n'\
' Pamiętaj: niektóre rekordy mogą się powtarzać (oznaczone kolorem)'

STR_OVERCLOCKING = ''\
' Niebezpieczna operacja!\n\n'\
' Większość pamięci GDDR5 działa na 6000-8000 MHz. GDDR5 jest czterokrotnie pompowane [x4]\n'\
' GDDR5 przy 8000 MHz technicznie działa na 2000 MHz\n'\
' Jeśli masz problemy, zmniejsz częstotliwość do 1000 MHz\n'\
'\n'\
' Efektywna częstotliwość GDDR5 to 1350 MHz\n'\
' Częstotliwość jest ustalana eksperymentalnie\n'\
' - Zbyt wysoka wartość może prowadzić do błędu LOADBIOS -8 lub DCT [*]\n'\
' - Zbyt niska wartość prowadzi do błędu AMDINIT'

STR_ABOUT_EAPKEYS = 'O kluczach EAP'
STR_INFO_EAPKEYS = ''\
' Klucz EAP może mieć długość 0x40 i 0x60 bajtów\n'\
' Modele PS4 10xx/11xx zazwyczaj mają tylko jeden klucz\n'\
' A modele 12xx/Slim/PRO mają klucz zapasowy\n'\

STR_IMMEDIATLY = ''\
' Uwaga: Wszystkie łatki są natychmiast stosowane do pliku!'

STR_PATCHES = STR_IMMEDIATLY + '\n'\
' Przełączy wartość między dostępnymi wartościami dla wybranej opcji'

STR_DOWNGRADE = ''\
' Niebezpieczna operacja!\n\n'\
' Przełączanie slotów jest używane do przywracania wersji FW (downgrade).\n'+\
' Naprawia również błąd "loadbios".\n'\
' Upewnij się, że masz kopię zapasową oryginalnego zrzutu sFlash i SYSCON.\n'\
' Wymagane jest patchowanie Syscon! W przeciwnym razie otrzymasz błąd "loadbios".\n'\
' Konsola nie uruchomi się normalnie.'

STR_ABOUT_MPATCH = 'Instrukcje dotyczące ręcznego patchowania'
STR_INFO_SC_MPATCH = ''\
' Każdy rekord ma długość 16 bajtów. Pierwszy bajt to zawsze "A5"\n'\
' Drugi bajt to "typ" rekordu, zazwyczaj w zakresie [0x00-0x30]\n'\
' Aktualizacja oprogramowania obejmuje 4 rekordy o typach %s\n'\
' Aby anulować ostatnią aktualizację FW, musimy wyczyścić te 4 rekordy (wypełniając je 0xFF)\n'\
' Jeśli po %s występują typy %s,%s, patchowanie jest niemożliwe\n'\
' slot zapasowy został już nadpisany, otrzymasz błąd checkUpdVersion'

STR_ABOUT_EAP = 'O kluczach EAP'
STR_INFO_HDD_EAP = ''\
' Te klucze pozwalają na eksplorację plików HDD PS4 na PC\n'\
' Dodatkowe informacje znajdziesz odwiedzając:\n '\

STR_ABOUT_EMC_CFW = 'O EMC CFW'
STR_INFO_EMC_CFW = ''\
' Używaj na własne ryzyko!\n'\
' Tylko dla Aeolia (PS4 Fat 10xx/11xx)\n'\
' Zapewnia kontrolę nad Southbridge i Syscon\n\n'\
' Dodatkowe informacje:\n '

STR_APP_HELP = ''\
' Użycie: ps4-wee-tools [parametry] \n'\
'\n'\
' Parametry: \n\n'\
'  <plik>              : załaduj odpowiednie narzędzie dla podanego pliku\n'\
'  <folder>            : zbuduj zrzut przy użyciu plików z podanego folderu\n'\
'  <plik1> <plik2> ... : porównaj pliki (z informacjami MD5)\n'\
'  --help              : wyświetl tę pomoc\n'\
'\n'\
' Strona główna: '
