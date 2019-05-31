#!/usr/bin/python
# -*- coding: UTF-8 -*-

import io
import os
import Tkinter

def clicked():
	print 'clicked'

members = ['Eli Chang', 'Fei Wei', 'Morse Ma', 'Tsao yufeng', 'Gandalf Jiang', 'Hytt Hu']
window = Tkinter.Tk()

listbox = Tkinter.Listbox(window)
for item in members:
	listbox.insert(0, item)

listbox.pack()

btn = Tkinter.Button(window, text = 'click me', command = clicked)
btn.pack()

window.mainloop()