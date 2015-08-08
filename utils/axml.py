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
			self.content = open(self.path, 'rb').read()

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
		off = stringTableOffset+off+2*size + 1
		while (self.content[off] != '\x80'):
			off += 1
		off += 4
		i = 0
		j = 0
		off += 4 
		resources = []
		while i < size-8:
			strings[j]['resource_id'] = (self.littleEndian(off+i))
			i += 4
			j += 1
		return strings_index_table, strings
