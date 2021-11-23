
# ADB 快捷指令

此脚本专注于将一些复杂的adb命令简洁化，将需要组合使用的命令统一，以方便日常调试。
但是为了依然可以记得原生的指令，脚本运行时依然会将原生指令输出，建议在使用时瞥一眼。

| 版本 | 日期 | 人员 | 内容 |
| :--- | ---------- | ---------- | ---------- |
|  V1.0.0 | * | Eli Chang | 初版 |
|  V1.1.0 | 2021.02.01 | Eli Chang | 完善 |

## 使用方法

1. python sc.py [cmd]

2. 将sc.py转化为可执行文件，在添加为系统变量

## 如何转为可执行文件？？？

1. 安装pyinstaller：```pip install pyinstaller```

> 若出现报错: error for loop initial declarations are only allowed in C99 mode，可在命令之前添加"CC='gcc -std=c99'"

2. 将sc.py和Helps.py存放某一路径（Windows下需要和python的安装路径在同一个分区）

3. cmd，并执行命令```pyinstaller -F [path\sc.py]```(Windows下，path为绝对路径)
	完成后，可执行文件将保存在dist文件夹下。

### 帮助

```shell
用法:
	dev			enable Developer Mode and launch `Developer options`

	log			launch log activity(Mtklogger/yLog)

	engmode		launch engineer mode

	pulllog		pull logs from sdcard
	pulllog [local]
	options:
		[local]: specified local path

	topact		dump current top activities
	topact [-p|-f]
	options:
		-p: output package installation path
		-f: output package file

	focus		dump current focus activity

	brt			set/get screen brightness
	brt [number](1-255)

	density		set/get current screen density
	density [number]

	size		get screen size

	sf			set/get current screen off timeout
	sf [time]
	options:
		[number]  : [number] millies(30000)
		[number]s : [number] seconds(60s)
		[number]m : [number] minutes(5m)

	start		launch specified activity
	start [-a|-n] [action|component]
	options:
		-a:	launch by action
		-n:	launch by component

	settings	launch settings

	key			send key event
	key [key_code]

	back		send back key event

	home		send home key event

	menu		send menu key event

	power		send power key event

	shot		send shot(camera) key event

	+3/-3		send VOLUME_UP / VOLUME_DOWN

	cap			create screen capture
	cap [-p] [local]
	options:
		-p:		 pull file after capture
		[local]: specified local path

	record		create screen record
	record [-b] [-p] [local]
	options:
		-b:		 record with bugreport
		-p:		 pull file after capture
		[local]: specified local path

	mute		device mute(RING & MUSIC)

	db			set/get settings database
	db [table] [name] [value]
	options:
		[table]: one of [system, secure, global]
		[name]:	 operand
		[value]: value will set to [name]

	kill		kill process by package name(if exist)
	kill [package]

	clear		clear data of package
	clear [package]

	prop		set/get an Android system property
	prop [name] [value]
	options:
		[name]:		operand
		[value]:	value will set to [name]

	pushs		push folder
	pushs [source] [target]
	options:
		[source]: folder push from
		[target]: folder push to

	workspace	genrate workspace and pulling to local
	workspace [local]
	option:
		[local]: specified local path

	watermark	clear watermark

	uid			get uid of package(if exist)
	uid [package]
```
