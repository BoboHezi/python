#!/usr/bin/python
# -*- coding: UTF-8 -*-

# import io
# import os
# import sys

import matplotlib.pyplot as plt
import numpy as np

def draw_rect(plt, rect, show_extra):
	x_min = rect[0] / WIDTH
	x_max = rect[2] / WIDTH
	y_min = 1 - rect[1] / HEIGHT
	y_max = 1 - rect[3] / HEIGHT
	plt.axvline(x=rect[0],ls="-",c=rect[4],ymin=y_min,ymax=y_max)
	if show_extra:
		plt.axvline(x=rect[0],ls="--",c=rect[4])

	plt.axhline(y=rect[1],ls="-",c=rect[4],xmin=x_min,xmax=x_max)
	if show_extra:
		plt.axhline(y=rect[1],ls="--",c=rect[4])

	plt.axvline(x=rect[2],ls="-",c=rect[4],ymin=y_min,ymax=y_max)
	if show_extra:
		plt.axvline(x=rect[2],ls="--",c=rect[4])

	plt.axhline(y=rect[3],ls="-",c=rect[4],xmin=x_min,xmax=x_max)
	if show_extra:
		plt.axhline(y=rect[3],ls="--",c=rect[4])

	pass

WIDTH = 10
HEIGHT = 10

plt.plot()
plt.title('ViewGroup')
plt.xlabel("width")
plt.ylabel("height")
plt.xlim(0, WIDTH) # X轴范围
plt.ylim(0, HEIGHT) # Y轴范围
#plt.grid(ls=":",c='b',) #打开坐标网格

ax = plt.gca()
ax.xaxis.set_ticks_position('top') # X 轴置顶
ax.invert_yaxis() # Y 轴反向

rects = [
	[2, 2, 4, 5, 'black'],
	[1, 1, 2, 2, 'green'],
	[3, 4, 5, 7, '#3e67f3']
]

l = rects[0][0]
t = rects[0][1]
r = rects[0][2]
b = rects[0][3]

for rect in rects:
	l = rect[0] if rect[0] < l else l
	t = rect[1] if rect[1] < t else t
	r = rect[2] if rect[2] > r else r
	b = rect[3] if rect[3] > b else b

max_rect = [l, t, r, b, 'red']
# draw_rect(plt, max_rect, True)

for rect in rects:
	draw_rect(plt, rect, False)

plt.show()
