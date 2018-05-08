import pytest
import sqlite3

from collections import namedtuple
from pathlib import Path

from united_states_of_browsers.db_merge.table import Table
from united_states_of_browsers.db_merge.custom_exceptions import InvalidFileError
project_root = Path(__file__).parents[2]


TableArgs = namedtuple('TableArgs', 'table path browser filename profile copies_subpath')
test_cases_exception_no_such_table = [
	TableArgs(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
	          browser='firefox',
	          filename='non_db_dummy_file_for_testing.txt',
	          profile='test_profile2',
	          copies_subpath=None,
	          ),
	# TableArgs(table='moz_places',
	#           path=Path(project_root,
	#                     'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	#                     'Firefox/Profiles/udd5sttq.test_profile2/moz_places.sqlite'),
	#           browser='firefox',
	#           filename='non_db_dummy_file_for_testing.txt',
	#           profile='test_profile2',
	#           copies_subpath=None,
	#           ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History_false_filename'),
	          browser='chrome',
	          filename='History_false_filename',
	          profile='Profile 1',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Vivaldi/User Data/Default/History_false_filename'),
	          browser='vivaldi',
	          filename='History',
	          profile='Default',
	          copies_subpath=None,
	          ),
	TableArgs(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Opera Software/Opera Stable/History_false_filename'),
	          browser='opera',
	          filename='History',
	          profile='Opera Stable',
	          copies_subpath=None,
	          ),
	]


@pytest.mark.parametrize('test_case', [test_case for test_case in test_cases_exception_no_such_table])
def test_suite_not_database(test_case):
	table_obj = Table(*test_case)
	with pytest.raises(InvalidFileError) as excep:
		table_obj.get_records()


def non_pytest_test_suite_not_database():
	for test_case in test_cases_exception_no_such_table:
		table_obj = Table(*test_case)
		try:
			table_obj.get_records()
		except InvalidFileError as excep:
			print('Expected exception raised: InvalidFileError', excep, '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
		else:
			print('Expected exception InvalidFileError NOT raised: .', '--', test_case.browser, test_case.profile, test_case.filename, test_case.table)
			raise Exception
		finally:
			print()
			# assert str(excep) == 'file is not a database'
		
def simply_run():
	for test_case in test_cases_exception_no_such_table:
		table_obj = Table(*test_case)
		table_obj.get_records()


if __name__ == '__main__':
	non_pytest_test_suite_not_database()
	quit()
	# simply_run()
	fx_false_file = Table(table='moz_places',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Roaming/Mozilla/'
	                    'Firefox/Profiles/udd5sttq.test_profile2/non_db_dummy_file_for_testing.txt'),
	          browser='firefox',
	          filename='non_db_dummy_file_for_testing.txt',
	          profile='test_profile2',
	          copies_subpath=None,
	          )
	
	# fx_false_file.get_records()
	
	chrome_false_file = Table(table='urls',
	          path=Path(project_root,
	                    'tests/data/browser_profiles_for_testing/AppData/Local/Google/Chrome/User Data/Profile 1/History_false_filename'),
	          browser='chrome',
	          filename='History_false_filename',
	          profile='Profile 1',
	          copies_subpath=None,
	          )
	chrome_false_file.get_records()
	print(list(chrome_false_file.records_yielder))