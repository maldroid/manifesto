from zipfile import ZipFile
import zipfile
from utils.templates import Obfuscator


class AXML:
	def __init__(self, path):
		self.is_apk = zipfile.is_zipfile(path)
		self.path = path

	def littleEndian(self, off, size=4):
		h = int(''.join(['%02x' %ord(c) for c in self.content[off+size-1:off-1:-1]]), 16)
		return h

	def read_file(self):
		if self.is_apk:
			apk = ZipFile(self.path, 'r')
			self.content = apk.read('AndroidManifest.xml')
		else:
			self.content = open(self.path, 'r').read()

#	def fill_zeros(self, off, size):
#		self.content = self.content[:off] + '\x10' * size + self.content[off+size:]

#	def dump(self, path):
#		with open(path, 'w') as f:
#			f.write(self.content)

	def parse_strings(self):
		self.read_file()
		numberOfStrings = self.littleEndian(4*4)
		stringIndexTableOffset = 0x24
		stringTableOffset = 0x24 + numberOfStrings * 4
		i = 0
		strings = []
		strings_index_table = []
		off = 0
		while i < numberOfStrings:
			off = self.littleEndian(stringIndexTableOffset+i*4)
			strings_index_table.append({'offset': stringIndexTableOffset+i*4, 'value': off})
			size = self.littleEndian(stringTableOffset+off, 2)
			strings.append({'offset': stringTableOffset+off+2, 'size': 2*size, 'value': self.content[stringTableOffset+off+2:stringTableOffset+off+2*size+2].decode(('utf16'))})
			i += 1
		off = stringTableOffset+off+2*size+4
		off += 4
		size = ord(self.content[off])
		i = 0
		j = 0
		off += 4 
		resources = []
		while i < size-8:
			strings[j]['resource_id'] = (self.littleEndian(off+i))
			i += 4
			j += 1
#		for i in xrange(1):
#			self.fill_zeros(strings[i][0], strings[i][1])
		return strings_index_table, strings
#			if i < len(resources):
#				print '%d (0x%08x): %s' % (i, resources[i], strings[i])
#			else:
#				print '%d (): %s' % (i, strings[i])
