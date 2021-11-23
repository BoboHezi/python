#!/usr/bin/python
# -*- coding: UTF-8 -*-

import io
import os
import sys
import re
import pygame
from sc import selected	as sc_selected
from sc import execute	as sc_execute
from sc import platform	as sc_platform
from sc import prop		as sc_prop
from sc import cap		as sc_cap

devices = ()
# (
# 	{'serial':%serial, 'platform':%platform, 'model':%model, 'size':($W, $H)},
# 	...
# )
selected = 0

display_w = 400

def load_device_surface(screen, size=[360, 480], imgFile='device_surface.png'):
	img = pygame.transform.scale(pygame.image.load(imgFile), (size[0], size[1]))
	screen.blit(img, [0, 0])
	pygame.display.flip()

def run_TP(size=[360, 480]):
	screen = pygame.display.set_mode((size[0], size[1]))
	pygame.display.set_caption('simlate TP')

	# 显示图片
	load_device_surface(screen, size)
	clock = pygame.time.Clock()

	touch_down_flag = False
	touch_motion_flag = False

	last_pointer = ()

	while True:
		for event in pygame.event.get():
			# print(event)
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# TOUCH_DOWN
				last_pointer = event.pos
				touch_down_flag = True
			elif event.type == pygame.MOUSEBUTTONUP:
				# TOUCH_UP
				if touch_down_flag:
					if touch_motion_flag:
						x1 = int(last_pointer[0] * scale)
						y1 = int(last_pointer[1] * scale)
						x2 = int(event.pos[0] * scale)
						y2 = int(event.pos[1] * scale)
						print('swipe from (%d, %d) to (%d, %d)' % (x1, y1, x2, y2))
						sc_execute('adb shell input swipe %d %d %d %d' % (x1, y1, x2, y2), False)
					else:
						x = int(last_pointer[0] * scale)
						y = int(last_pointer[1] * scale)
						print('tab on (%d, %d)' % (x, y))
						sc_execute('adb shell input tap %d %d' % (x, y), False)
					last_pointer = event.pos if event.type == pygame.MOUSEBUTTONUP else last_pointer
					clock.tick(200)
					sc_cap(['-p', 'device_surface.png'])
					# 显示图片
					load_device_surface(screen, size)

				touch_down_flag = False
			elif event.type == pygame.MOUSEMOTION:
				# TOUCH_MOTION if touch_down_flag else HOVER
				touch_motion_flag = touch_down_flag
			elif event.type == pygame.WINDOWLEAVE:
				touch_down_flag = False
	pygame.display.flip()

def init_size(device_size=(360, 480)):
	display_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

	simulate_w = device_size[0]
	simulate_h = device_size[1]

	retract_w = int(display_size[0] * 0.8)
	retract_h = int(display_size[1] * 0.8)

	if simulate_w > retract_w:
		simulate_w = retract_w
		simulate_h = int(simulate_w * device_size[1] / device_size[0])
	if simulate_h > retract_h:
		simulate_h = retract_h
		simulate_w =  int(device_size[0] * simulate_h / device_size[1])

	simulate_size = (simulate_w, simulate_h)

	print('device_size: %s' % (device_size, ))
	print('display_size: %s' % (display_size, ))
	print('simulate_size: %s' % (simulate_size, ))

	global scale
	scale = device_size[0] / simulate_size[0]

	return simulate_size

def init_devices():
	devis = []
	for line in sc_execute('adb devices', False).split('\n'):
		if line.find('\t') > 0:
			serial = line.split('\t')[0]
			sc_selected = {2 : (serial, '')}
			plat = sc_platform()
			model = sc_prop(['ro.product.model'], False)
			size_str = sc_execute('adb shell wm size', False)
			obj = re.match('(?i)Physical size*: ([0-9]*)x([0-9]*)', size_str)
			size = (360, 480)
			if obj and len(obj.groups()) == 2:
				size = (int(obj.group(1)), int(obj.group(2)))

			devis.append({'serial':serial, 'platform':plat, 'model':model.strip(), 'size':size})
	return tuple(devis)

if ( __name__ == "__main__"):
	pygame.init()
	devices = init_devices()
	display_w = devices[0].get('size')[0] + 40
	print(devices)
	run_TP(init_size(devices[0].get('size')))
