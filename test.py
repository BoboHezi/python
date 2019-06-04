#!/usr/bin/python
# -*- coding: UTF-8 -*-

import io
import os
import sys
import Tkinter

def clicked():
	print 'clicked'

def calculat():
	x = 50
	while x < 80:
		x += 1
		y = 170
		while y > 130:
			y -= 1
			value = ((x ** 2) + (y ** 2)) ** 0.5
			diff = abs(value - 161.29)
			if diff < 0.1:
				print "%d * %d * %lf" % (x, y, value)

def createfile(name, size):
    with open(name, 'wb') as f:
            f.write(os.urandom(size))

members = ['Eli Chang', 'Fei Wei', 'Morse Ma', 'Tsao yufeng', 'Gandalf Jiang', 'Hytt Hu']
window = Tkinter.Tk()

listbox = Tkinter.Listbox(window)
for item in members:
	listbox.insert(0, item)

listbox.pack()

btn = Tkinter.Button(window, text = 'click me', command = clicked)
btn.pack()

window.mainloop()
