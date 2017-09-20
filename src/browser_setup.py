import os


debug = 0


def _choose_browser_paths(browser_name_or_path):
	path_crumbs = {'firefox': ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles'],
	               'chrome': ['~', 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default',
	                          'History'],
	               }
	# if browser_name is given, return apt path crumbs; if path is given (no key), return the path
	try:
		return os.path.join(path_crumbs.get(browser_name_or_path, browser_name_or_path))
	except TypeError:
		# if list of dirs given (breadcrumbs), create a path from that.
		return os.path.expanduser(
			os.path.join(*path_crumbs.get(browser_name_or_path, browser_name_or_path)))


def _profile_location(crumbs_or_path=None):
	"""
    (WIll be changed.)
    Accepts path and name for browser profile directory and creates the path to it.
    Currently, By default uses Firefox's profile path for win10 for a profile named default.
    :param crumbs_or_path:
    :type crumbs_or_path:
    :return:
    :rtype:
    """
	try:
		profile_loc = os.path.realpath(os.path.expanduser(crumbs_or_path))
	except TypeError:
		# path_dirs = ['~', 'AppData', 'Roaming', 'Mozilla', 'Firefox', 'Profiles']
		profile_loc = os.path.expanduser(os.path.join(*crumbs_or_path))
		profile_loc = os.path.realpath(profile_loc)
	return profile_loc


def _profile_dir(profile_loc, *, profiles):
	"""
    Finds the names of all profile directories (default) or for specified profile.
    :param profile_loc:
    :type profile_loc:
    :param profile_name:
    :type profile_name:
    :return:
    :rtype:
    """
	if not profiles:
		return [dir_.name for dir_ in os.scandir(profile_loc)]
	try:
		profile_dir_ = [dir_.name for dir_ in os.scandir(profile_loc) if
		                profiles.lower() in dir_.name.lower()]
		# profile_dir_ = [dir_.name for dir_ in os.scandir(profile_loc) if
		#                 dir_.name.lower().rfind(profiles.lower()) == len(dir_.name) - len(
		#                             profiles)]
	except (IndexError, FileNotFoundError):
		print(
					"\nERROR: Profile directory not found. \nCheck the profile directory path (given: {}) and"
					" profile name string (given: {}).".format(profile_loc, profiles))
	else:
		return profile_dir_


def _setup_profile_paths(profile_loc, profile_dir_names):
	if profile_dir_names == profile_loc:
		return profile_loc
	else:
		return [os.path.join(profile_loc, profile_dir_) for profile_dir_ in profile_dir_names]


def setup_profile_paths(*, browser_name_or_path, profiles):
	"""
    Sets up the directory path for sqlite database files.
    Returns path to sqlite file's copy stored in project directory.
    :return: root directory
    :rtype: str/path-like object
    """
	crumbs_or_path = _choose_browser_paths(browser_name_or_path=browser_name_or_path)
	profile_loc = _profile_location(crumbs_or_path)
	
	profile_dir_names = _profile_dir(profile_loc, profiles=profiles)
	profile_paths = _setup_profile_paths(profile_loc, profile_dir_names)
	return profile_paths


def _db_files(root, ext='.sqlite'):
	"""
    Returns a list of file in the specified directory (not subdirectories) with a specified (or no) extension.
    :param root: Path to directory with the files
    :type root: str/path-like object
    :param ext: Extension for the file. (Default: .sqlite)
    :type ext: str | None
    :return: list of files with the specified extension.
    :rtype: list[str]
    """
	if root is None or os.path.exists(root) is False:
		print("ERROR: Path was not found (given: {})".format(root))
		return
	try:
		for curr_dir, subdirs, files in os.walk(root):
			break
	except TypeError:
		print("ERROR: Path can not be None")
	else:
		ext = ext[1:] if ext[0] == '.' else ext
		return [file_ for file_ in files if file_.rfind(ext) == len(file_) - len(ext)]


def db_filepath(root, filenames=None, ext='sqlite'):
	"""
    Yields the path for the next database file.
    By default, these are sqlite file. (used by browsers to store history, bookmarks etc)

    Usage:
        filepath_generator = _filepath(root, filenames, ext)
        next_sqlite_databse_filepath = next(filepath_generator)

    :param root: Directory path containing the database files.
        Default: <project_root>/tinker/data/firefox_regular_surfing/
    :type root: str/path-like object
    :param filenames: List of database filenames in the root directory.
        Default: ['places', 'storage']
    :type filenames: list[str]
    :param ext: Extension of the databse file.
        Default: sqlite
    :type ext: str
        Default: sqlite
    :return: yields path of the database file.
    :rtype: str/path-like object
    """
	try:
		ext_joiner = '' if ext[0] in {os.extsep, '.'} else os.extsep
	except (TypeError, IndexError):
		ext_joiner = ''
		ext = ''
	if isinstance(filenames, str):
		filenames = [filenames]
	elif filenames is None:
		filenames = _db_files(root=root, ext=ext)
	file_names = [ext_joiner.join([file_, ext]) for file_ in filenames]
	try:
		return [os.path.join(root_, file_name_) for root_ in root for file_name_ in file_names]
	except TypeError as excep:
		print('Missing value: browser name or profile path', excep, sep='\n')
		if debug: raise excep
		os.sys.exit()