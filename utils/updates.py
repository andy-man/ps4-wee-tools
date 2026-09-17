#==========================================================
# Firmware repo auto-update (andy-man/ps4-ic-fw)
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================
import datetime
import os
import shutil
import tempfile
import zipfile

from utils.utils import APP_CONFIG, ROOT_PATH

try:
	import requests
except ImportError:
	requests = None

FW_REPO = 'andy-man/ps4-ic-fw'
FW_API_URL = f'https://api.github.com/repos/{FW_REPO}/commits/main'
FW_ZIP_URL = f'https://codeload.github.com/{FW_REPO}/zip/refs/heads/main'
FW_PATH = os.path.join(ROOT_PATH, 'fws')

TIMEOUT = 30
CHUNK_SIZE = 64 * 1024


def should_check():
	try:
		interval = int(APP_CONFIG.get('fw_update_check', '0') or '0')
	except ValueError:
		return False

	if interval <= 0:
		return False

	last = APP_CONFIG.get('fw_update_last', '')
	if not last:
		return True

	try:
		last_date = datetime.datetime.strptime(last, '%Y-%m-%d').date()
	except ValueError:
		return True

	return (datetime.date.today() - last_date).days >= interval


def get_remote_sha():
	r = requests.get(FW_API_URL, timeout=TIMEOUT, headers={'Accept': 'application/vnd.github+json'})
	r.raise_for_status()
	return r.json()['sha']


def _save_check_state(sha=None):
	APP_CONFIG.set('fw_update_last', datetime.date.today().isoformat())
	if sha:
		APP_CONFIG.set('fw_update_sha', sha)
	APP_CONFIG.save()


def download_with_progress(url, dest_path):
	import lang.lang as Lang

	r = requests.get(url, stream=True, timeout=TIMEOUT)
	r.raise_for_status()

	total = int(r.headers.get('Content-Length') or 0)
	done = 0

	with open(dest_path, 'wb') as f:
		for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
			if not chunk:
				continue
			f.write(chunk)
			done += len(chunk)
			if total:
				print('\r' + Lang.STR_PROGRESS_KB % (done // 1024, total // 1024), end='')
			else:
				# No Content-Length — show downloaded size only (avoid "/ 0KB")
				print('\r Downloading FW update: %dKB ' % (done // 1024), end='')

	print()


def _zip_strip_prefix(names):
	"""Return common single top-level folder prefix (e.g. 'repo-main/'), or ''."""
	roots = set()
	for name in names:
		name = name.replace('\\', '/').lstrip('/')
		if not name:
			continue
		roots.add(name.split('/', 1)[0])
		if len(roots) > 1:
			return ''
	if len(roots) != 1:
		return ''
	root = roots.pop()
	# Only strip if it looks like a directory prefix used by members
	prefix = root + '/'
	for name in names:
		name = name.replace('\\', '/').lstrip('/')
		if name and name != root and not name.startswith(prefix) and name != root + '/':
			return ''
	return prefix


def _clean_folder(folder):
	if os.path.isdir(folder):
		shutil.rmtree(folder)
	os.makedirs(folder, exist_ok=True)


def extract_zip_to_folder(zip_path, output_folder):
	_clean_folder(output_folder)
	out_root = os.path.normpath(output_folder)

	with zipfile.ZipFile(zip_path, 'r') as zf:
		names = zf.namelist()
		strip_prefix = _zip_strip_prefix(names)

		for info in zf.infolist():
			name = info.filename.replace('\\', '/')
			if strip_prefix:
				if not name.startswith(strip_prefix):
					continue
				rel = name[len(strip_prefix):]
			else:
				rel = name.lstrip('/')

			if not rel or rel.endswith('/'):
				continue

			# Root of zip: keep only README.md, skip LICENSE/.gitignore/etc
			if '/' not in rel and rel.lower() != 'readme.md':
				continue

			# Skip nested .git from archive if present
			if rel == '.git' or rel.startswith('.git/'):
				continue

			target = os.path.normpath(os.path.join(out_root, rel))
			if not target.startswith(out_root + os.sep) and target != out_root:
				continue

			os.makedirs(os.path.dirname(target), exist_ok=True)
			with zf.open(info) as src, open(target, 'wb') as dst:
				dst.write(src.read())


def check_fw_update():
	if not should_check() or requests is None:
		return

	tmp_path = None
	try:
		remote_sha = get_remote_sha()
		local_sha = APP_CONFIG.get('fw_update_sha', '')

		if local_sha and local_sha == remote_sha:
			_save_check_state()
			return

		fd, tmp_path = tempfile.mkstemp(suffix='.zip')
		os.close(fd)

		download_with_progress(FW_ZIP_URL, tmp_path)
		extract_zip_to_folder(tmp_path, FW_PATH)
		_save_check_state(remote_sha)
	except Exception:
		pass
	finally:
		if tmp_path and os.path.isfile(tmp_path):
			try:
				os.remove(tmp_path)
			except OSError:
				pass
