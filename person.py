class Person(object):
	"first class ever created in python"

	def __init__(self, name, gender, age):
		self.name = name
		self.gender = gender
		self.age = age

	def __str__(self):
		return "Name: %s, Gender: %s, Age: %d" % (self.name, self.gender, self.age)