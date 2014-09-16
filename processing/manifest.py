from utils.axml import AXML
from utils.templates import Obfuscator
import os, logging
from utils.resourceid import RESOURCE_ID

class Manifest(Obfuscator):
	def __init__(self, path, config):
		Obfuscator.__init__(self, path, config)
		self.axml = AXML(os.path.join(path, 'AndroidManifest.xml'))

	def endianify(self, value):
		value = '%08x' % value
		charify = lambda x : chr(int(x, 16))
		return charify(value[6:8]) + charify(value[4:6]) + charify(value[2:4]) + charify(value[0:2])

	def littleEndian(self, text, off, size=4):
		h = int(''.join(['%02x' %ord(c) for c in text[off+size-1:off-1:-1]]), 16)
		return h

	def run(self):
		strings_index_table, strings = self.axml.parse_strings()
		axml = self.axml.content
		available = []
		resource_ids = []
		for i, string in enumerate(strings):
			if 'resource_id' in string:
				available.append(string['value'])
				resource_ids.append(string['resource_id'])
			if string['value'] in self.config and \
			 ('resource_id' in string or not self.config[string['value']].get('check_resource_id', True)):
				value = self.config[string['value']]['value']
				size = self.config[string['value']].get('size', len(value))
				diff = len(value) - string['size']
				if self.config[string['value']].get('add_null_bytes', True):
					diff += 2
					value = value + '\x00\x00'
				size = '%04x' % (size/2)
				size = chr(int(size[2:4], 16)) + chr(int(size[:2],16))
				axml = axml[:string['offset'] - 2] + size + \
					value + \
					axml[(string['size'] + string['offset']):]
				for j in xrange(i+1, len(strings_index_table)):
					axml = axml[:strings_index_table[j]['offset']] + \
						self.endianify(strings_index_table[j]['value'] + diff) + \
						axml[strings_index_table[j]['offset']+4:]
					strings[j]['offset'] += diff
					strings_index_table[j]['value'] += diff
				axml = axml[:4] + \
					self.endianify(self.littleEndian(axml, 4) + diff) + \
					axml[8:]
				axml = axml[:0xc] + \
					self.endianify(self.littleEndian(axml, 0xc) + diff) + \
					axml[0x10:]
		with open(os.path.join(self.path, 'AndroidManifest.xml'), 'wb') as f:
			f.write(axml)
		_, strings = self.axml.parse_strings()
		logging.debug('Strings with a resource ID: ' + str(available))
		logging.debug('Resource IDs: ' + str(['0x%08x' % x for x in resource_ids]))
		logging.debug('All strings: ' + str([s['value'] for s in strings]))
