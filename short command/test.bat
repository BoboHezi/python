@echo off
set type=%1

if "%type%"=="" goto:eof
if "%type%"=="dev" goto dev
if "%type%"=="mtklog" goto mtklog
if "%type%"=="pulllog" goto pulllog
if "%type%"=="topact" goto topact
if "%type%"=="focus" goto focus
if "%type%"=="fun" goto fun
if "%type%"=="brt" goto brt
if "%type%"=="density" goto density
if "%type%"=="size" goto size

echo wrong parameter
goto:eof

:dev
adb shell "am start -a android.settings.APPLICATION_DEVELOPMENT_SETTINGS"
goto:eof

:mtklog
adb shell "am start -n com.mediatek.mtklogger/.MainActivity"
goto:eof

:pulllog
if "%2"=="" (
		adb pull /sdcard/mtklog/
		goto:eof
	)
adb pull /sdcard/mtklog/ %2
goto:eof

:topact
if "%2"=="-f" (
		for /f "tokens=*" %%i in ('adb shell "dumpsys activity top | grep ACTIVITY"') do (
			set vars=%%i
		)
		echo %vars%
		goto:eof
	)
adb shell "dumpsys activity top | grep ACTIVITY"
goto:eof

:focus
adb shell "dumpsys activity | grep mFocusedActivity"
goto:eof

:brt
if "%2"=="" (
		adb shell "cat /sys/class/leds/lcd-backlight/brightness"
		goto:eof
	)
adb root
adb shell "settings put system screen_brightness %2"
goto:eof

:density
if "%2"=="" (
		adb shell wm density
		goto:eof
	)
adb root
adb shell wm density %2
goto:eof

:size
adb shell wm size
goto:eof

:fun
call:testFun rst 101
echo %rst%
goto:eof

:testFun
echo parameter %~2
set "%~1=%~2+100"
goto:eof
