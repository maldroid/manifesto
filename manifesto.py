import argparse
from utils.axml import AXML
import tempfile, shutil
from zipfile import ZipFile
import os
from utils.templates import Obfuscator
from config import config
import logging

def import_plugins():
	for name in os.listdir("processing"):
		if name.endswith(".py"):
			name = name[:-3]
			globals()[name] = __import__("processing." + name)

def zipdir(dirpath, zippath, keep_meta = False):
	archive = ZipFile(zippath, 'w')
	for root, dirs, files in os.walk(dirpath):
		for filepath in files:
			if keep_meta or not 'META-INF' in root:
				archive.write(os.path.join(root, filepath), os.path.join(root, filepath)[len(dirpath):])
	archive.close()

def main(args):
	tmpdir = tempfile.mkdtemp()
	zipfile = ZipFile(args.apk_file)
	zipfile.extractall(tmpdir)
	import_plugins()
	processing_modules = Obfuscator.__subclasses__()
	try:
		for module in processing_modules:
			module(tmpdir, config.get(module.__name__, {})).run()
	except Exception as ex:
		logging.error('Exception encountered: %s' % str(ex))
		shutil.rmtree(tmpdir)
		return
	if args.force_overwrite or not os.path.isfile(args.outfile):
		zipdir(tmpdir, args.outfile, args.keep_meta)
	else:
		logging.error('Output file already exists (use -f to overwrite)!')
	shutil.rmtree(tmpdir)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='(De)obfuscate AndroidManifest file')
	parser.add_argument('apk_file',
				help='APK file to (de)obfuscate')
	parser.add_argument('--outfile', '-o', default='obfuscated.apk', help = 'Output APK file (defaults to obfuscated.apk)')
	parser.add_argument('--keep_meta', '-k', action='store_true', help = 'Keep the META-INF directory (signature)')
	parser.add_argument('--force_overwrite', '-f', action='store_true', help = 'Overwrite output file, if it exists')
	parser.add_argument("-v", "--verbose", help="increase output verbosity",
                    action="store_true")
	
	args = parser.parse_args()
	if args.verbose:
		logging.basicConfig(format='%(message)s', level=logging.DEBUG)
	else:
		logging.basicConfig(format='%(message)s', level=logging.INFO)
	main(args)

