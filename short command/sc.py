import os
import sys
import re

def execute(cmd):
	f = os.popen(cmd, "r")
	rst = f.read()
	f.close()
	return rst;

def numberic(value):
	rst = re.match('[0-9]{1,}', value, flags=0)
	result = False if rst == None else (True if rst.group() == value else False)
	return result

def root():
	execute("adb root")

def remount():
	execute("adb remount")

def dev():
	print(execute("adb shell am start -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS"))

def mtklog():
	print(execute("adb shell am start -n com.mediatek.mtklogger/.MainActivity"))

def pulllog():
	dst = ""
	if len(sys.argv) >= 3:
		dst = sys.argv[2]
	print(execute("adb pull /sdcard/mtklog/ %s" % (dst)))

def topact():
	rst = execute("adb shell \"dumpsys activity top | grep ACTIVITY\"")
	array = rst.split('\n')
	for item in array:
		item = item.lstrip().rstrip()
		if len(item) == 0:
			continue
		print(item)
		if len(sys.argv) >= 3 and sys.argv[2] == '-f':
			componet = item.split(' ')[1]
			pkg = componet.split('/')[0]
			apkinfo = execute("adb shell \"pm path %s\"" % (pkg))
			print(apkinfo)

def focus():
	print(execute("adb shell \"dumpsys activity | grep mFocusedActivity\""))

def brt():
	if len(sys.argv) >= 3:
		if numberic(sys.argv[2]) and int(sys.argv[2]) >= 0:
			print(execute("adb shell \"settings put system screen_brightness %d\"" % (int(sys.argv[2]))))
			return
	print(execute("adb shell \"cat /sys/class/leds/lcd-backlight/brightness\""))

def density():
	if len(sys.argv) >= 3:
		if numberic(sys.argv[2]) and int(sys.argv[2]) >= 0:
			print(execute("adb shell wm density %d" % (int(sys.argv[2]))))
	print(execute("adb shell wm density"))

def size():
	print(execute("adb shell wm size"))

def sf():
	if len(sys.argv) >= 3:
		parm = sys.argv[2]
		time = execute("adb shell settings get system screen_off_timeout")
		last = parm[len(parm) - 1 :]
		if last == 's' and numberic(parm[: len(parm) - 1]):
			time = int(parm[: len(parm) - 1]) * 1000
		elif last == 'm' and numberic(parm[: len(parm) - 1]):
			time = int(parm[: len(parm) - 1]) * 60 * 1000
		elif numberic(parm):
			time = int(parm)
		else:
			time = int(time)
		print(execute("adb shell settings put system screen_off_timeout %d" % (time)))
	print(execute("adb shell settings get system screen_off_timeout"))

cmd = ""
if len(sys.argv) > 1:
	cmd = sys.argv[1]

if cmd == "dev":
	dev()
elif cmd == "mtklog":
	mtklog()
elif cmd == "pulllog":
	pulllog()
elif cmd == "topact":
	topact()
elif cmd == "focus":
	focus()
elif cmd == "brt":
	brt()
elif cmd == "density":
	density()
elif cmd == "size":
	size()
elif cmd == "sf":
	sf()
else:
	print("wrong parameter")
