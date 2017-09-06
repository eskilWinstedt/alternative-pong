import cx_Freeze

executables = [cx_Freeze.Executable('Pong.py')]

cx_Freeze.setup(
	name = 'Pong',
	options = {'build_exe': {'packages':['pygame', 'os', 'math', 'time', 'random'],
	'include_files':["Icon.png", "design.txt", "Walkway_SemiBold.ttf"]}},
	executables = executables
	)