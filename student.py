import person

class Student(person.Person):
	"first class ever created in python"

	__degree = ''

	def __init__(self, name, gender, age, school, id):
		super(Student, self).__init__(name, gender, age)
		self.school = school
		self.id = id

	def display(self):
		print self

	def __str__(self):
		return super(Student, self).__str__() + ", School: %s, ID: %ld" % (self.school, self.id)

	def setdegree(self, degree):
		self.__degree = degree

	def getdegree(self):
		return self.__degree
