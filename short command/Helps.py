
def main():
	"""
	This is a short command for adb, created by Eli.
	you can input below options.

	Options:
		dev		enable Developer Mode and launch Developer options

		log		launch log activity(Mtklogger/yLog)

		engmode		launch engineer mode

		pulllog		pull logs from sdcard

		topact		dump current top activities

		focus		dump current focus activity

		brt		set/get screen brightness

		density		set/get current screen density

		size		get screen size

		sf		set/get current screen off timeout

		start		launch specified activity

		settings	launch settings

		key		send key event

		back		send back key event

		home		send home key event

		menu		send menu key event

		power		send power key event

		shot		send shot(camera) key event

		+3/-3		send VOLUME_UP / VOLUME_DOWN

		cap		create screen capture

		record		create screen record

		mute		device mute(RING & MUSIC)

		db		set/get settings database

		kill		kill process by package name(if exist)

		pushs		push folder

		workspace	genrate workspace and pulling to local

		watermark	clear watermark

		uid		get uid of package(if exist)
	"""
	pass

def dev():
	"""
	enable Developer Mode and launch Developer options
	"""
	pass

def log():
	"""
	launch log activity(Mtklogger/yLog)
	"""
	pass

def engmode():
	"""
	launch engineer mode
	"""
	pass

def pulllog():
	"""
	pulllog [local]
	pull logs from stroage

	options:
		[local]: specified local path
	"""
	pass

def topact():
	"""
	topact [-p|-f]
	dump current top activities

	options:
		-p: output package installation path
		-f: output package file
	"""
	pass

def focus():
	"""
	dump current focus activity
	"""
	pass

def brt():
	"""
	brt [number](1-255)

	set brightness if [number] exist
	or get brightness
	"""
	pass

def density():
	"""
	density [number]

	set screen density if [number] exist
	or get density
	"""
	pass

def size():
	"""
	get screen size
	"""
	pass

def sf():
	"""
	sf [time]

	set screen off timeout if [time] exist
	or get screen off timeout

	[time] options:
		[number]  : [number] millies(30000)
		[number]s : [number] seconds(60s)
		[number]m : [number] minutes(5m)
	"""
	pass

def start():
	"""
	start [-a|-n] [action|component]
	launch specified activity

	options:
		-a:	launch by action
		-n:	launch by component
	"""
	pass

def settings():
	"""
	launch settings
	"""
	pass

def key():
	"""
	key [key_code]

	send specified key event
	"""
	pass

def back():
	"""
	send back key event
	"""
	pass

def home():
	"""
	send home key event
	"""
	pass

def menu():
	"""
	send menu key event
	"""
	pass

def power():
	"""
	send power key event
	"""
	pass

def shot():
	"""
	send shot(camera) key event
	"""
	pass

def volume():
	"""
	send VOLUME_UP / VOLUME_DOWN key event
	"""
	pass

def cap():
	"""
	cap [-p] [local]
	create screen capture

	options:
		-p:		pull file after capture
		[local]:	specified local path
	"""
	pass

def record():
	"""
	record [-b] [-p] [local]
	create screen record, CTRL+C to stop

	options:
		-b:		record with bugreport
		-p:		pull file after capture
		[local]:	specified local path
	"""
	pass

def mute():
	"""
	device mute(RING & MUSIC)
	"""
	pass

def db():
	"""
	db [table] [name] [value]
	set/get settings database

	options:
		[table]:	one of [system, secure, global]
		[name]:		name will operate(or create)
		[value]:	value will set to [name]
	"""
	pass

def kill():
	"""
	kill [package]

	kill process by package name(if exist)
	"""
	pass

def pushs():
	"""
	pushs [source] [target]
	push folder to device

	options:
		[source]:	folder push from
		[target]:	folder push to
	"""
	pass

def workspace():
	"""
	workspace [local]
	genrate workspace and pulling to local

	option:
		[local]:	specified local path
	"""
	pass

def watermark():
	"""
	clear watermark
	"""
	pass

def uid():
	"""
	uid [package]
	get uid of package(if exist)
	"""
	pass
