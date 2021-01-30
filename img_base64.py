import base64
import os
import sys
import random

def img_2_base64(img_path):
	f = open(img_path, 'rb') #二进制方式打开图文件
	ls_f = base64.b64encode(f.read()) #读取文件内容，转换为base64编码
	f.close()
	ls_f = str(ls_f)[2:-1]
	return 'data:image/png;base64,%s' % ls_f

def base64_2_img_file(raw, dst):
	imgdata = base64.b64decode(raw)
	path = dst[0:dst.rfind('\\')]
	if not os.path.exists(path):
		os.makedirs(path)
	file = open(dst,'wb+')
	file.write(imgdata)
	file.close()

def genrate_str(length):
	rst = ''
	x = 0
	while x < length - 1:
		char = chr(random.randint(33, 126))
		if char in '\\/:*?"<>|':
			continue
		rst = rst + str(char)
		x += 1
	return rst

if len(sys.argv) > 1:
	arg = sys.argv[1]
	if os.path.isfile(arg):
		print('convert %s to base64 string: ' % arg)
		print(img_2_base64(arg))
	else:
		save_path = '%s\\imgs\\%s.png' % (os.getcwd(), genrate_str(10))
		print(save_path)
		base64_2_img_file(arg, save_path)

	