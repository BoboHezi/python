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

NODE_PARSER = None
FIND_NODE = []
SCALE = 1

class NodeParser(xml.sax.ContentHandler):
	"""parser ui node"""
	def __init__(self):
		self.hierarchy = Hierarchy()
		self.ele_layer = []

	def startElement(self, tag, attributes):
		if tag == 'hierarchy':
			if 'rotation' in attributes:
				self.hierarchy.rotation = attributes['rotation']
				self.ele_layer.append(self.hierarchy.children)
		elif tag == 'node':
			node = self.dump_node(attributes)
			last = self.ele_layer.pop()
			last.append(node)
			self.ele_layer.append(last)
			self.ele_layer.append(node.children)

	def endElement(self, tag):
		self.ele_layer.pop()

	def characters(self, content):
		pass

	def endDocument(self):
		pass

	def dump_str_node(str):
		node = NodeParser()
		xml.sax.parseString(str, node, None)
		return node.hierarchy

	def dump_file_node(file):
		if os.path.isfile(file):
			parser = xml.sax.make_parser()
			parser.setFeature(xml.sax.handler.feature_namespaces, 0)

			node = NodeParser()
			parser.setContentHandler(node)
			parser.parse(file)
			return node.hierarchy
		return None

	def dump_node(self, attributes):
		node = Node()
		if 'NAF' in attributes:
			node.NAF = bool(attributes['NAF'])
		if 'bounds' in attributes:
			bounds_str = attributes['bounds']
			mth = re.match('\[([\d]*),([\d]*)\]\[([\d]*),([\d]*)\]', bounds_str)
			if mth and len(mth.groups()) == 4:
				x1 = int(mth.group(1))
				y1 = int(mth.group(2))
				x2 = int(mth.group(3))
				y2 = int(mth.group(4))
				node.bounds = ((x1, y1), (x2, y2))
		if 'checkable' in attributes:
			node.checkable = bool(attributes['checkable'])
		if 'checked' in attributes:
			node.checked = bool(attributes['checked'])
		if 'class' in attributes:
			node.classs = attributes['class']
		if 'clickable' in attributes:
			node.clickable = bool(attributes['clickable'])
		if 'content-desc' in attributes:
			node.content_desc = attributes['content-desc']
		if 'enabled' in attributes:
			node.enabled = bool(attributes['enabled'])
		if 'focusable' in attributes:
			node.focusable = bool(attributes['focusable'])
		if 'focused' in attributes:
			node.focused = bool(attributes['focused'])
		if 'index' in attributes:
			node.index = int(attributes['index'])
		if 'long-clickable' in attributes:
			node.long_clickable = bool(attributes['long-clickable'])
		if 'package' in attributes:
			node.package = attributes['package']
		if 'password' in attributes:
			node.password = bool(attributes['password'])
		if 'resource-id' in attributes:
			node.resource_id = attributes['resource-id']
		if 'scrollable' in attributes:
			node.scrollable = bool(attributes['scrollable'])
		if 'selected' in attributes:
			node.selected = bool(attributes['selected'])
		if 'text' in attributes:
			node.text = attributes['text']
		return node


class Hierarchy(object):
	"""docstring for Hierarchy"""
	def __init__(self):
		self.rotation = 0
		self.children = []


class Node(object):
	"""docstring for ui node"""
	def __init__(self):
		self.NAF            = False
		self.bounds         = None
		self.checkable      = False
		self.checked        = False
		self.classs         = ''
		self.clickable      = False
		self.content_desc   = ''
		self.enabled        = False
		self.focusable      = False
		self.focused        = False
		self.index          = -1
		self.long_clickable = False
		self.package        = ''
		self.password       = False
		self.resource_id    = ''
		self.scrollable     = False
		self.selected       = False
		self.text           = ''
		self.children       = []

	def __str__(self) -> str:
		return f'Node[package: {self.package}, class: {self.classs}, id: {self.resource_id}, bounds: {self.bounds}, text: {self.text}, content-desc: {self.content_desc}]'


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

def uiautomator_pull(file):
	for i in range(5):
		out, err = execute('adb shell uiautomator dump /sdcard/%s' % file)
		if isempty(err.strip()):
			break
	out, err = execute('adb shell ls /sdcard/%s' % file)
	if isempty(err.strip()):
		execute('adb pull /sdcard/%s' % file)
		execute('adb shell rm -rf /sdcard/%s' % file)
		return True
	return False

def load_device_surface(screen, size=[360, 480], imgFile='device_surface.png'):
	img = pygame.transform.scale(pygame.image.load(imgFile), (size[0], size[1]))
	screen.blit(img, [0, 0])
	pygame.display.flip()

def load_uiautomator():
	if uiautomator_pull('ui.xml'):
		global NODE_PARSER
		NODE_PARSER = NodeParser.dump_file_node('ui.xml')
	# ui_xml = uiautomator_str()
	# global NODE_PARSER
	# NODE_PARSER = NodeParser.dump_str_node(ui_xml)

def run_uiautomator(size=[360, 480]):
	screen = pygame.display.set_mode((size[0] + 300, size[1]))
	screen.fill([193, 193, 193])
	pygame.display.set_caption('uiautomator')

	pygame.draw.line(screen, (0, 0, 0), [size[0], 0], [size[0], size[1]], 2)
	draw_msg(screen, [], size)

	# 显示图片
	sc_cap(['-p', 'device_surface.png'])
	load_device_surface(screen, size)

	# 加载布局
	load_uiautomator()

	point_down_pos = ()
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return
			elif event.type == pygame.MOUSEBUTTONDOWN:
				point_down_pos = event.pos
			elif event.type == pygame.MOUSEBUTTONUP:
				if eq(event.pos, point_down_pos):
					if event.button == 3:
						print('left click')
						# 加载布局
						sc_cap(['-p', 'device_surface.png'])
						load_device_surface(screen, size)
						load_uiautomator()
					elif event.button == 1:
						print(f'rignt click on {int(event.pos[0] * SCALE), int(event.pos[1] * SCALE)}')
						find_node(int(event.pos[0] * SCALE), int(event.pos[1] * SCALE), NODE_PARSER)
						print(FIND_NODE)
	pygame.display.flip()

def draw_msg(screen, node, size):
	# if not screen or not node:
	# 	return
	pygame.font.init()
	titleFont = pygame.font.SysFont("calibri", 17)
	title = titleFont.render("Ball Game", False, (0, 0, 0))
	screen.blit(title, (size[0] + 100, 35))
	pygame.display.update()

def find_node(x, y, node):
	if not node:
		return None
	if type(node) is Hierarchy:
		node = node.children[0]
	if node.bounds[0][0] < x < node.bounds[1][0] and node.bounds[0][1] < y < node.bounds[1][1]:
		global FIND_NODE
		FIND_NODE = node
		if len(node.children) > 0:
			for child in node.children:
				find_node(x, y, child)

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

	global SCALE
	SCALE = device_size[0] / simulate_size[0]

	return simulate_size

def init_devices():
	devis = []
	for line in sc_execute('adb devices', False).split('\n'):
		if line.find('\t') > 0:
			serial = line.split('\t')[0]
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
	print(devices)
	# run_TP(init_size(devices[0].get('size')))

	run_uiautomator(init_size(devices[0].get('size')))
