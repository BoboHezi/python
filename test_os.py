import os
import time
from student import Student
from person import Person
from eli.py.coord import Coordinate
from sort.Sort import Sort

cwd = os.getcwd();

def isFile(file):
	return os.path.isfile(file)

def timeStampToTime(timeStamp):
	timeStruct = time.localtime(timeStamp)
	return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def sortByTime(file):
	return os.path.getctime(os.path.dirname(file))

def getFiles(path):
	files = os.listdir(path)
	af = []
	for file in files:
		isfile = isFile(path + "\\" + file)
		if isfile:
			af.append(path + "\\" + file)
		else:
			af += getFiles(path + "\\" + file)
	return af

def listFiles(files):
	msg = ""
	for file in files:
		msg = msg + file;
		msg = msg + '  ' + timeStampToTime(os.path.getctime(file)) + '\n'
	return msg

allfiles = getFiles(cwd)
print(allfiles)
allfiles.sort(key=sortByTime)
print('\n')

file = open('C:\\Users\\zhangzhanbo\\Desktop\\msg.txt', "w")
file.write(listFiles(allfiles))
file.close()

per = Person('Eli Chang', 'male', 19)
print(per)

stu1 = Student('Leo Wei', 'male', 21, 'MIT', 20384740)
stu2 = Student('Eli Chang', 'male', 19, 'MIT', 20384739)

stu1.display()
print(stu2)

coord1 = Coordinate(8, 0)
print(coord1)

origin = [5,3,0,6,-3,1,2]
print('origin: ', origin)
sorted = Sort().abacus_sort(origin)
print('sorted: ', sorted)