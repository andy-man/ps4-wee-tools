#==========================================================
# UI internationalization
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================
import copy
import json
import locale
import os
import sys

from utils.utils import UI, Clr, APP_CONFIG, ROOT_PATH

APP_VERSION = '1.0.5'

# Common strings (used in lang files)

STR_080B = Clr.fg.cyan+'"08-0B"'+Clr.reset
STR_0C0F = Clr.fg.orange+'"0C-0F"'+Clr.reset
STR_2023 = Clr.fg.red+'"20-23"'+Clr.reset

I18N_PATH = os.path.join(ROOT_PATH, 'i18n')

LANG_DATA = {}
LANG_CODE = 'en'
EN_BASE = {}

def load_i18n_json(lang_code):
	path = os.path.join(I18N_PATH, f'{lang_code}.json')
	if not os.path.isfile(path):
		return None
	try:
		with open(path, 'r', encoding='utf-8') as f:
			data = json.load(f)
	except (OSError, json.JSONDecodeError):
		return None
	return data if isinstance(data, dict) else None

def check_i18n(lang_code):
	"""Validate i18n/<lang>.json against English base and return cleaned data.
	Menus are kept only when value counts match. Missing keys are dropped.
	"""
	if not lang_code:
		return None

	data = load_i18n_json(lang_code)
	if not data:
		return None

	title = data.get('LANGUAGE')
	if not isinstance(title, str) or not title.strip():
		return None

	g = globals()
	checked = {'LANGUAGE': title.strip()}

	for key, value in data.items():
		if key == 'LANGUAGE' or key not in g:
			continue

		base = g[key]

		if key.startswith('MENU_'):
			if isinstance(base, list) and isinstance(value, list):
				if len(value) == len(base):
					checked[key] = value
			elif isinstance(base, dict) and isinstance(value, dict):
				if len(value) == len(base):
					merged = dict(base)
					for k, v in value.items():
						if k in merged and isinstance(v, str):
							merged[k] = v
					checked[key] = merged
		elif key.startswith('STR_') and isinstance(value, str):
			checked[key] = value

	return checked

def load_languages():
	"""Load all i18n/*.json into LANG_DATA (keyed by code) via check_i18n."""
	if not os.path.isdir(I18N_PATH):
		return
	for name in sorted(os.listdir(I18N_PATH)):
		if not name.endswith('.json'):
			continue
		code = name[:-5].lower()
		if not code or code in LANG_DATA:
			continue
		checked = check_i18n(code)
		if not checked:
			continue
		LANG_DATA[code] = checked

def apply_i18n(lang_code):
	"""Overlay validated LANG_DATA[lang_code] onto current (English) defaults."""
	if not lang_code:
		return

	data = LANG_DATA.get(lang_code)
	if not data:
		return

	g = globals()
	for key, value in data.items():
		if key != 'LANGUAGE' and key in g:
			g[key] = copy.deepcopy(value)

def _reset_english():
	"""Restore raw English strings/menus from startup snapshot."""
	g = globals()
	for key, value in EN_BASE.items():
		g[key] = copy.deepcopy(value)

def _decorate_strings():
	"""Apply dividers, links and colors to selected strings."""
	global APP_NAME, TITLE
	g = globals()

	APP_NAME = UI.sp(g['STR_APP_NAME'] + ' v' + APP_VERSION)
	TITLE = UI.DIVIDER_BOLD + APP_NAME + 'by Andy_maN'.rjust(UI.LINE_WIDTH - len(APP_NAME) - 1) + '\n' + UI.DIVIDER_BOLD

	g['STR_MPATCH_INPUT']	= UI.DIVIDER + g['STR_MPATCH_INPUT']
	g['STR_CHOICE']			= UI.DIVIDER + g['STR_CHOICE']
	g['STR_BACK']			= UI.DIVIDER + g['STR_BACK']
	g['STR_MEMCLOCK_INPUT']	= UI.DIVIDER + g['STR_MEMCLOCK_INPUT']
	g['STR_SAMU_INPUT']		= UI.DIVIDER + g['STR_SAMU_INPUT']
	g['STR_CONFIRM']		= UI.DIVIDER + g['STR_CONFIRM']

	g['STR_APP_HELP']		= g['STR_APP_HELP'] + UI.link('https://github.com/andy-man/ps4-wee-tools')
	g['STR_INFO_HDD_EAP']	= g['STR_INFO_HDD_EAP'] + UI.link('https://www.psdevwiki.com/ps4/Mounting_HDD_in_Linux')
	g['STR_INFO_EMC_CFW']	= g['STR_INFO_EMC_CFW'] + UI.link('https://www.psdevwiki.com/ps4/Southbridge')
	g['STR_INFO_SPIWAY']	= g['STR_INFO_SPIWAY'] + UI.link('https://www.psdevwiki.com/ps4/SPIway')
	g['STR_INFO_SCF']		= g['STR_INFO_SCF'] + UI.link('https://github.com/AbkarinoMHM/PS4SysconTools')
	g['STR_INFO_FW_LINK']	= g['STR_INFO_FW_LINK'] + UI.link('https://github.com/andy-man/ps4-ic-fw')

	g['STR_INFO_SC_MPATCH']	= g['STR_INFO_SC_MPATCH']%(STR_080B, STR_0C0F, STR_2023, STR_080B)

	g['STR_DONE']			= Clr.fg.yellow + g['STR_DONE'] + Clr.reset
	g['STR_NOT_FOUND']		= Clr.fg.red + g['STR_NOT_FOUND'] + Clr.reset
	g['STR_BAD_SIZE']		= Clr.fg.orange + g['STR_BAD_SIZE'] + Clr.reset
	g['STR_DIFF']			= Clr.fg.orange + g['STR_DIFF'] + Clr.reset
	g['STR_FAIL']			= Clr.fg.red + g['STR_FAIL'] + Clr.reset
	g['STR_OK']				= Clr.fg.green + g['STR_OK'] + Clr.reset
	g['STR_ABORT']			= Clr.fg.red + g['STR_ABORT'] + Clr.reset

def _sync_lang_modules():
	"""Push updated lang symbols into modules that used `from lang.lang import *`."""
	g = globals()
	keys = [k for k in g if k.startswith(('STR_', 'MENU_')) or k in ('TITLE', 'APP_NAME', 'LANG_CODE')]
	skip = {sys.modules.get('lang.en'), sys.modules.get('lang.lang')}
	for mod in list(sys.modules.values()):
		if mod is None or mod in skip:
			continue
		md = getattr(mod, '__dict__', None)
		if md is None or md is g:
			continue
		if 'STR_CHOICE' not in md and 'MENU_TOOL_SELECTION' not in md:
			continue
		for key in keys:
			if key in md:
				md[key] = g[key]

def set_language(lang_code):
	"""Apply language immediately (no app restart)."""
	global LANG_CODE
	if not lang_code or lang_code not in LANG_DATA:
		return False

	_reset_english()
	if lang_code != 'en':
		apply_i18n(lang_code)
	_decorate_strings()
	LANG_CODE = lang_code
	_sync_lang_modules()
	return True

def get_system_lang_code():
	"""Pick i18n code from PC locale; fall back to English."""
	try:
		raw = ''
		# Windows: getlocale() may return 'Russian_Russia' — use LCID instead
		if sys.platform[:3] == 'win':
			import ctypes
			lcid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
			raw = locale.windows_locale.get(lcid, '') or ''
		if not raw:
			locale.setlocale(locale.LC_ALL, '')
			raw, _encoding = locale.getlocale()
		if not raw:
			return 'en'
		# e.g. 'ru_RU' / 'en_US.cp1252' -> 'ru' / 'en'
		tag = locale.normalize(raw).split('.')[0].replace('-', '_')
		code = tag.split('_')[0].lower()
		if len(code) <= 3 and code in LANG_DATA:
			return code
	except (locale.Error, TypeError, ValueError, AttributeError, OSError):
		pass
	return 'en'

# Base language (English)
from lang.en import *

# Snapshot raw English before overlays/decoration
EN_BASE.update({
	k: copy.deepcopy(v) for k, v in list(globals().items())
	if k.startswith(('STR_', 'MENU_'))
})

load_languages()

LANG_CODE = (APP_CONFIG.get('lang') or '').strip().lower()
if not LANG_CODE or LANG_CODE not in LANG_DATA:
	LANG_CODE = get_system_lang_code()

if LANG_CODE != 'en':
	apply_i18n(LANG_CODE)

_decorate_strings()
