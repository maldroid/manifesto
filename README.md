manifesto
=========

PoC framework for APK obfuscation, used to demonstrate some of the obfuscation examples from http://maldr0id.blogspot.com. It supports plugins (located in `processing` directory) that can do different obfuscation techniques. Main gist is that you run manifesto on the APK file and it produces an obfuscated APK file.

# Starting

Since this is a PoC, there isn';t any fancy way to strat it. Just clone the repo and type up:

```
python manifesto.py -o output.apk input.apk
```

And you will have (well, almost) obfuscated `output.apk`. All of the command line options are available when you ask for help:

```
$ python manifesto.py -h
usage: manifesto.py [-h] [--outfile OUTFILE] [--keep_meta] [--force_overwrite]
                    [-v]
                    apk_file

(De)obfuscate AndroidManifest file

positional arguments:
  apk_file              APK file to (de)obfuscate

optional arguments:
  -h, --help            show this help message and exit
  --outfile OUTFILE, -o OUTFILE
                        Output APK file (defaults to obfuscated.apk)
  --keep_meta, -k       Keep the META-INF directory (signature)
  --force_overwrite, -f
                        Overwrite output file, if it exists
  -v, --verbose         increase output verbosity

```

In order to configure plugins you need to open up the `config.py` file. This file contains a `config` dictionary. Each key in this dictionary is the name of the plugin (e.g. `Manifest`). Each value is a dictionary of options (described below).

# Plugins

FOr now there is only one plugin [described here](http://maldr0id.blogspot.com/2014/09/having-fun-with-androidmanifestxml.html). It is able to substittue some of the string resources from the binary version of the `AndroidManifest.xml`. This plugin is called `Manifest`.

## Manifest

Options for this plugin are very simple. Each key in the options dictionary is a unicode string that needs to be replaced. Value is (again) a dictionary with the following keys:

* `value` - new value of the string, provided as a wide unicode string in ASCII caracters (see the included `config.py`)
* `size` (optional) - size of the string *as will be written in the `AndroidManifest.xml`*. If not presenet, the actual length will be taken (rounded down).
* `add_null_bytes` (optional) - wheter to add a null bytes and the end of the new string or not. Default: `True`
* `check_resource_id` (optional) - only substitute when the string to be replaced has a resource map entry defined. Default: `True`

# This is a Proof of Concept

It may not work perfectly or, in some cases, it may not work at all. I tested it on a couple of samples, but if you encounter any problems just let me know.
