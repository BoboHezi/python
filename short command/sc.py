import os
import sys
import re
import time
import Helps
from pydoc import help
from sys import exit

selected = None
# {%count : (%serial_id, %platform)}

def execute(cmd, show):
	if cmd.startswith('adb') and selected:
		for key in selected.keys():
			if key == 2:
				device = selected[key]
				cmd = cmd[0:3] + (' -s %s ' % device[0]) + cmd[4:]
			break
	if show:
		print('cmd: %s' % cmd)
	f = os.popen(cmd, 'r')
	rst = f.read()
	f.close()
	return rst;

def numberic(value):
	rst = re.match('[0-9]{1,}', value, flags=0)
	return False if not rst else (True if rst.group() == value else False)

def root():
	execute('adb root', False)

def remount():
	execute('adb remount', False)

def dev():
	database(['global', 'development_settings_enabled', '1'])
	start(['-n', 'com.android.settings/.Settings'])
	start(['-a', 'android.settings.APPLICATION_DEVELOPMENT_SETTINGS'])

def log():
	plat = 'mtk'
	if selected and len(selected) == 1:
		for value in selected.values():
			plat = value[1]
			break
	if plat == 'mtk':
		start(['-n', 'com.mediatek.mtklogger/.MainActivity'])
	elif plat == 'sprd':
		start(['-n', 'com.sprd.logmanager/.logui.LogMainActivity'])
	elif plat == 'qcom':
		pass

def engmode():
	plat = 'mtk'
	if selected and len(selected) == 1:
		for value in selected.values():
			plat = value[1]
			break
	database(['global', 'development_settings_enabled', '1'])
	if plat == 'mtk':
		start(['-n', 'com.mediatek.engineermode/.EngineerMode'])
	elif plat == 'sprd':
		start(['-n', 'com.sprd.engineermode/.EngineerModeActivity'])
	elif plat == 'qcom':
		pass

def platform():
	cpu_info = execute('adb shell \"cat /proc/cpuinfo\"', False)
	hardware = None
	for line in cpu_info.split('\n'):
		matchObj = re.match('(?i)Hardware\t*: (.*)', line)
		if matchObj:
			hardware = matchObj.group(1)
			break

	if 'MT' in hardware:
		return 'mtk'
	elif 'Unisoc' in hardware:
		return 'sprd'
	elif 'Qualcomm' in hardware:
		return 'qcom'

	# mtk_flag = execute('adb shell \"getprop | grep mtk\"', False)
	# if len(mtk_flag) > 0:
	# 	return 'mtk'
	# else :
	# 	sprd_flag = execute('adb shell \"getprop | grep sprd\"', False)
	# 	if len(sprd_flag) > 0:
	# 		return 'sprd'
	# 	else :
	# 		qcom_flag = execute('adb shell \"getprop | grep qcom\"', False)
	# 		if len(qcom_flag) > 0:
	# 			return 'qcom'
	return 'unknown'

def pulllog(argv=sys.argv[2:]):
	plat = 'mtk'
	if selected and len(selected) == 1:
		for value in selected.values():
			plat = value[1]
			break
	source = None
	if plat == 'mtk':
		source = '/sdcard/mtklog/'
	elif plat == 'sprd':
		source = '/sdcard/ylog/'
	elif plat == 'qcom':
		pass

	dst = argv[0] if len(argv) else ''

	if source:
		print(execute('adb pull %s %s' % (source, dst), True))

def database(argv=sys.argv[2:], prt=False):
	if len(argv) >= 1:
		table = argv[0]
		if table in ('system', 'secure', 'global') and len(argv) >= 2:
			name = argv[1]
			value = argv[2] if len(argv) >= 3 else None
			if value:
				execute('adb shell settings put %s %s %s' % (table, name, value), True)
			result = execute('adb shell settings get %s %s' % (table, name), True)
			if prt:
				print(result)
			return result
	return '-h'

def prop(argv=sys.argv[2:], prt=False):
	if len(argv) >= 1:
		root()
		key = argv[0]
		value = argv[1] if len(argv) >= 2 else None
		if value:
			execute('adb shell setprop %s %s' % (key, value), True)
		result = execute('adb shell getprop %s' % key, True)
		if prt:
			print(result)
		return result
	return '-h'

def topact(argv=sys.argv[2:]):
	rst = execute('adb shell \"dumpsys activity top | grep ACTIVITY\"', True)
	array = rst.split('\n')
	help_flag = False
	for item in array:
		item = item.lstrip().rstrip()
		if len(item) == 0:
			continue
		print(item)
		if len(argv) >= 1:
			matchObj = re.match('ACTIVITY (.*)/(.*) ([0-9a-fA-F].*) pid=(.*)', item)
			if not matchObj or len(matchObj.groups()) < 4:
				continue
			pkg = matchObj.group(1)
			if argv[0] == '-p':
				print(execute('adb shell pm path %s' % (pkg), True))
			elif argv[0] == '-f':
				print(execute('adb shell pm list packages -f %s' % (pkg), True))
			else :
				help_flag = True
	if help_flag:
		return '-h'

def focus():
	print(execute('adb shell \"dumpsys activity | grep mFocusedActivity\"', True))

def brt(argv=sys.argv[2:]):
	db_arg = ['system', 'screen_brightness']
	if len(argv) >= 1:
		if numberic(argv[0]) and int(argv[0]) >= 0:
			db_arg.append(int(argv[0]))
		else :
			return '-h'
	database(db_arg, True)

def density(argv=sys.argv[2:]):
	if len(argv) >= 1:
		if numberic(argv[0]) and int(argv[0]) >= 0:
			print(execute('adb shell wm density %d' % (int(argv[0])), True))
		else :
			return '-h'
	print(execute('adb shell wm density', True))

def size():
	print(execute('adb shell wm size', True))

def sf(argv=sys.argv[2:]):
	db_arg = ['system', 'screen_off_timeout']
	if len(argv) >= 1:
		parm = argv[0]
		last = parm[-1:]
		if last == 's' and numberic(parm[:-1]):
			time = int(parm[:-1]) * 1000
		elif last == 'm' and numberic(parm[:-1]):
			time = int(parm[:-1]) * 60 * 1000
		elif numberic(parm):
			time = int(parm)
		else:
			return '-h'
		db_arg.append(time)
	time = int(database(db_arg))
	time_format = ('%dms' % time)
	if time >= 1000 and time < (60 * 1000) :
		time_format = ('%ds' % (time / 1000))
	elif time >= (60 * 1000) and time < (60 * 60 * 1000) :
		time_format = ('%dm' % (time / 1000 / 60))
	print(time_format)

def start(argv=sys.argv[2:]):
	if len(argv) >= 2 and argv[0] in ('-a', '-n'):
		print(execute('adb shell am start %s %s' % (argv[0], argv[1]), True))
	else :
		return '-h'

def send_key(argv=sys.argv[2:]):
	if len(argv) >= 1:
		print(execute('adb shell input keyevent %s' % (argv[0]), True))
	else :
		return '-h'

def volume(argv=sys.argv[2:]):
	times = int(argv[1:]) if numberic(argv[1:]) else 1
	first = argv[0]
	key = 'KEYCODE_VOLUME_UP' if first == '+' else ('KEYCODE_VOLUME_DOWN' if first == '-' else '')
	if key:
		index = 0
		while index < times:
			index += 1
			send_key([key])

def cap(argv=sys.argv[2:]):
	path = 'sdcard/caps/'
	execute('adb shell mkdir -p %s' % (path), False)
	name = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.png'
	dst = path + name
	print(execute('adb shell screencap -p %s' % (dst), True))
	if len(argv) >= 1 :
		if argv[0] != '-p':
			return '-h'
		local = argv[1] if len(argv) >= 2 else ''
		if local.endswith(os.sep):
			local = local + name
		print(execute('adb pull %s %s' % (dst, local), True))

def record(argv=sys.argv[2:]):
	path = 'sdcard/caps/'
	execute('adb shell mkdir -p %s' % (path), False)
	name = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + '.mp4'
	dst = path + name
	try:
		cmd = ('adb shell screenrecord %s' % (dst))
		if len(argv) >= 1 :
			for item in argv:
				if item == '-b':
					cmd = cmd + ' --bugreport'
					break
		execute(cmd, True)
	except KeyboardInterrupt as e:
		print('\n')
	if len(argv) >= 1 :
		for item in argv:
				if item == '-p':
					local = ''
					if len(argv) >= argv.index('-p') + 2 :
						local = argv[argv.index('-p') + 1]
					local = '' if local == '-b' else local
					if local.endswith(os.sep):
						local = local + name
					time.sleep(1)
					print(execute('adb pull %s %s' % (dst, local), True))
					break

def kill(argv=sys.argv[2:]):
	if len(argv) > 0:
		pkg = argv[0]
		rst = execute('adb shell ps', True)
		root()
		for line in rst.split('\n'):
			# if line.endswith(pkg):
			if pkg in line:
				# Splits a string separated by an unquantified amount of space
				obj = re.findall('[\S.]+', line)
				if obj and len(obj) > 1:
					pid = obj[1]
					if numberic(pid):
						execute('adb shell kill %s' % pid, True)
	else :
		return '-h'

def clear(argv=sys.argv[2:]):
	if len(argv) > 0:
		pkg = argv[0]
		rst = execute('adb shell pm clear %s' % pkg, True)
	else :
		return '-h'

def pushs(argv=sys.argv[2:]):
	source = argv[0] if len(argv) > 0 else None
	target = argv[1] if len(argv) > 1 else None

	if not source or len(source) == 0 or not os.path.exists(source) or os.path.isfile(source):
		return '-h'

	# find 'anchor' as we wanted
	available = ('system', 'vendor')
	# print(source.split(os.sep))
	anchor = None
	for item in available:
		if item in source.split(os.sep):
			anchor = item
			break
	if not anchor and target:
		for item in available:
			if item in target.split('/'):
				anchor = item
				break
	# print('anchor = %s' % anchor)

	if not anchor:
		return '-h'

	if not target:
		if not anchor:
			return '-h'
		else:
			# find target from source
			target = source[source.find(anchor):]

	root()
	remount()

	target = target.replace('\\', '/')
	# print('push %s -> %s' % (source, target))

	files = getFiles(source)
	# print(files)
	if files:
		push_items = {}
		for source_file in files:
			target_file = None
			if anchor in source_file:
				target_file = source_file[source_file.find(anchor):]
			else:
				target_file = (target if target.endswith('/') else target + '/') + source_file
			target_file = target_file.replace('\\', '/')
			push_items[source_file] = target_file
			# print('push %s -> %s' % (source_file, target_file))

		if len(push_items) > 0:
			for key, value in push_items.items():
				print('%s -> %s' % (key, value))
			confirm = compatible_input('push above items, do you confirm?(y/n)')
			if confirm == 'y':
				for key, value in push_items.items():
					print(execute('adb push %s %s' % (key, value), False))

def getFiles(path):
	if not os.path.exists(path):
		return None
	if os.path.isfile(path):
		return path
	if path.endswith(os.sep):
		path = path[:-1]
	files = os.listdir(path)
	af = []
	for file in files:
		isfile = os.path.isfile(path + os.sep + file)
		if isfile:
			af.append(path + os.sep + file)
		else:
			af += getFiles(path + os.sep + file)
	return af

def workspace(argv=sys.argv[2:]):
	action = 'com.freeme.workspace.ACTION_DEBUG'
	comp1 = 'com.freeme.freemelite.odm/com.freeme.launcher.WorkspaceReceiver'
	comp2 = 'com.freeme.biglauncher/com.freeme.biglauncher.launcher.component.WorkspaceReceiver'
	execute('adb shell am broadcast -a %s -n %s' % (action, comp1), True)
	execute('adb shell am broadcast -a %s -n %s' % (action, comp2), True)
	local = argv[0] if (len(argv) > 0) else ''
	execute('adb pull /sdcard/launcher/ %s' % local, True)

def mute():
	print(execute('adb shell media volume --show --stream 2 --set 0', True))
	print(execute('adb shell media volume --show --stream 3 --set 0', True))

def watermark():
	execute('adb shell am broadcast -a android.droi.watermark.SECRET_CODE', True)

def uid(argv=sys.argv[2:]):
	pkg = argv[0] if (len(argv) > 0) else None
	if not pkg:
		return '-h'

	packages_list = execute('adb shell cat /data/system/packages.list', True)
	pattern = '(^%s )([0-9]*)' % pkg
	uid = None
	for line in packages_list.split('\n'):
		obj = re.match(pattern, line)
		if obj:
			uid = obj.group(2)
			break
	print('%s uid %s' % (pkg, uid if uid else 'not found'))

def compatible_input(prompt):
	if sys.version_info.major == 2:
		return raw_input(prompt)
	else:
		return input(prompt)

if ( __name__ == "__main__"):

	# dump cmd
	cmd = sys.argv[1] if len(sys.argv) > 1 else ''

	# help child first
	help_flag = ('-h', '--help')
	if set(help_flag) & set(sys.argv[2:]):
		help('Helps.%s' % cmd)
		exit()

	# first, find all the devices
	devices = []
	for line in execute('adb devices', False).split('\n'):
		if line.find('\t') > 0:
			# find platform and put to %devices
			id = line.split('\t')[0]
			selected = {2 : (id, None)}
			selected = {2 : (id, platform())}
			devices.append(selected)

	if selected:
		for key in selected.keys():
			selected = {1 : selected[key]}

	if len(devices) == 0:
		print('no devices/emulators found!!!')
		exit()
	elif len(devices) >= 2:
		# show selection
		for device in devices:
			for key in device.keys():
				devi = device[key]
				print('%d - %s - %s' % (devices.index(device) + 1, devi[0], devi[1]))
				break
		ipt = int(compatible_input('\nmore than one device/emulator, please choose one: '))
		ipt = 1 if ipt > len(devices) or ipt < 1 else ipt
		selected = devices[ipt - 1]

	cmd_process = {
	'dev'		:	[dev],
	'log'		:	[log],
	'engmode'	:	[engmode],
	'pulllog'	:	[pulllog],
	'topact'	:	[topact],
	'focus'		:	[focus],
	'brt'		:	[brt],
	'density'	:	[density],
	'size'		:	[size],
	'sf'		:	[sf],
	'start'		:	[start],
	'settings'	:	[start, [['-n', 'com.android.settings/.Settings']]],
	'key'		:	[send_key],
	'back'		:	[send_key, [['KEYCODE_BACK']]],
	'home'		:	[send_key, [['KEYCODE_HOME']]],
	'menu'		:	[send_key, [['KEYCODE_MENU']]],
	'power'		:	[send_key, [['KEYCODE_POWER']]],
	'shot'		:	[send_key, [['KEYCODE_CAMERA']]],
	'cap'		:	[cap],
	'record'	:	[record],
	'mute'		:	[mute],
	'db'		:	[database, [sys.argv[2:], True]],
	'prop'	:	[prop, [sys.argv[2:], True]],
	'kill'		:	[kill],
	'clear'		:	[clear],
	'pushs'		:	[pushs],
	'workspace'	:	[workspace],
	'watermark'	:	[watermark],
	'uid'		:	[uid],
	'[+-][0-9]'	:	[volume, cmd],
	'^(-h)$|^(--help)$'	:	[help, 'Helps.main'],
	}

	# find implementation
	implementation = cmd_process.get(cmd)
	if not implementation:
		for key, impl in cmd_process.items():
			obj = re.match(key, cmd)
			if obj and obj.group() == cmd:
				implementation = impl
				break

	# implementation
	if implementation and len(implementation) > 0:
		func = implementation[0]
		argv = implementation[1] if len(implementation) > 1 else None
		rtn = func(*argv) if argv else func()
		if rtn in help_flag:
			help('Helps.%s' % cmd)
		exit()

	print('wrong parameter, try \'sc --help\' to get more information')
