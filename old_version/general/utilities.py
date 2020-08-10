
class Opponents:
	def __init__(self, obj1, obj2):
		self.obj1 = obj1
		self.obj2 = obj2

	def opposal(self, obj):
		if obj is self.obj1:
			return self.obj2

		if obj is self.obj2:
			return self.obj1