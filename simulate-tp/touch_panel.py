#!/usr/bin/python
# -*- coding: UTF-8 -*-

import io
import os
import sys
import re
import pygame
import xml.sax
from operator import eq
from sc import selected	as sc_selected
from sc import execute	as sc_execute
from sc import platform	as sc_platform
from sc import prop		as sc_prop
from sc import cap		as sc_cap
from subprocess import Popen, PIPE

class NodeParser(xml.sax.ContentHandler):
	"""parser ui node"""
	def __init__(self):
		self.hierarchy = []

	def startElement(self, tag, attributes):
		if tag == 'node':
			pass

	def endElement(self, tag):
		pass

	def characters(self, content):
		pass

	def endDocument(self):
		pass

	def dump_str_node(str):
		pass

	def dump_file_node(file):
		if os.path.isfile(file):
			parser = xml.sax.make_parser()
			parser.setFeature(xml.sax.handler.feature_namespaces, 0)

			node = NodeParser()
			parser.setContentHandler(node)
			parser.parse(file)
			return node.nodes
		return None


class Node(object):
	"""docstring for ui node"""
	def __init__(self, arg):
		self.NAF            = False
		self.bounds         = ((), ())
		self.checkable      = False
		self.checked        = False
		self.classs         = ''
		self.clickable      = False
		self.content-desc   = ''
		self.enabled        = False
		self.focusable      = False
		self.focused        = False
		self.index          = -1
		self.long-clickable = False
		self.package        = ''
		self.password       = False
		self.resource-id    = ''
		self.scrollable     = False
		self.selected       = False
		self.text           = ''
		


devices = ()
# (
# 	{'serial':%serial, 'platform':%platform, 'model':%model, 'size':($W, $H)},
# 	...
# )

display_w = 400

def execute(cmd, show=False):
	if cmd.startswith('adb') and sc_selected:
		for key in sc_selected.keys():
			if key == 2:
				device = sc_selected[key]
				cmd = cmd[0:3] + (' -s %s ' % device[0]) + cmd[4:]
			break
	if show:
		print('cmd: %s' % cmd)
	process = Popen(cmd, stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	return stdout.decode('utf-8'), stderr.decode('utf-8')

def isempty(obj):
    return True if not (obj and len(obj)) else False

def uiautomator_str():
	for i in range(5):
		out, err = execute('adb shell uiautomator dump /sdcard/ui.xml')
		if isempty(err.strip()):
			break
	out, err = execute('adb shell ls /sdcard/ui.xml')
	if isempty(err.strip()):
		out, err = execute('adb shell cat /sdcard/ui.xml')
		return out.strip()
	return None

def load_device_surface(screen, size=[360, 480], imgFile='device_surface.png'):
	img = pygame.transform.scale(pygame.image.load(imgFile), (size[0], size[1]))
	screen.blit(img, [0, 0])
	pygame.display.flip()

def load_uiautomator():
	# ui_xml = uiautomator_str()
	NodeParser.dump_file_node('ui.xml')

def run_uiautomator(size=[360, 480]):
	screen = pygame.display.set_mode((size[0], size[1]))
	pygame.display.set_caption('uiautomator')

	# 显示图片
	sc_cap(['-p', 'device_surface.png'])
	load_device_surface(screen, size)
	clock = pygame.time.Clock()

	# 加载布局
	load_uiautomator()

	point_down_pos = ()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				point_down_pos = event.pos
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
				if eq(event.pos, point_down_pos):
					print('click')
					# 加载布局
					load_uiautomator()

	pygame.display.flip()

def init_size(device_size=(360, 480)):
	display_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

	simulate_w = device_size[0]
	simulate_h = device_size[1]

	retract_w = int(display_size[0] * 0.9)
	retract_h = int(display_size[1] * 0.9)

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
	# run_TP(init_size(devices[0].get('size')))

	run_uiautomator(init_size(devices[0].get('size')))
