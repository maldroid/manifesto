class Obfuscator(object):
	def __init__(self, path, config):
		self.path = path
		self.config = config

	def run(self):
		raise NotImplementedError('You have to implement run method of <%s> class!' % self.__class__.__name__)
