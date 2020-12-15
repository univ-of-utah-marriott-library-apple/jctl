# jctl

This is a Python 3 utility that depends on [python-jamf](https://github.com/univ-of-utah-marriott-library-apple/python-jamf). You can not use this utility without python-jamf installed first.

## Requirements

This utility has been tested on macOS 10.14, macOS 11, and CentOS 7.

The jctl project requires python3 and python-jamf. Please make sure you have those by running the following commands.

```bash
python3
```

```python
import jamf
```

macOS does not include python3. You can get python3 with [Anaconda](https://www.anaconda.com/) or [Homerew](https://brew.sh/). For example, this is how you install python3 with Homebrew.

```bash
brew install python3
```

## Installation

Change the directory you would like it located in.

```bash
git clone https://github.com/univ-of-utah-marriott-library-apple/jctl.git
```

As you can see, we don't really have an install script yet...

## Config file

To create a config file, run this commmand

```bash
setconfig.py
```

	Hostname (don't forget https:// and :8443): https://example.com:8443
	username: james
	Password:

To print the settings (except password).

```bash
setconfig.py -P
```

	Using /Users/james/Library/Preferences/edu.utah.mlib.jamfutil.plist
	https://example.com:8443
	james
	Password is set

To test the settings

```bash
setconfig.py -t
```

	{'accounts': {'groups': None,
				'users': {'user': [{'id': '2', 'name': 'james'},
									{'id': '1', 'name': 'root'}]}}}

To specify any of the settings on the command line, use -H, -u, or -p

```bash
setconfig.py -H https://example.com -u james -p secret
```

## patch.py

This tool so far

### Getting Help

```bash
patch.py --help
patch.py list --help
patch.py upload --help
patch.py remove --help
patch.py info --help
patch.py update --help
```

### List all Patch Management Title Names

```bash
patch.py list
```

### List all uploaded packages

```bash
patch.py list --pkgs
```

### List all versions (and associated packages)

```bash
patch.py list --versions <Name of Patch Management Title>
patch.py list --patches <Name of Patch Management Title>
```

### Modify Patch settings

The following requires the user to have Jamf Admin Privileges

```
patch.py info /PATH/TO/PACKAGE
patch.py upload /PATH/TO/PACKAGE
patch.py remove <PACKAGE NAME>
```

## Other scripts

The following scripts are preliminary scripts to update polcies en masse. Because they are still 0.1, we aren't making docs yet. But here they are if you want to check them out.

* policy_categories.py, allows you to change all policy categories at once
* policy_packages.py, allows you to change all policy packages at once

Please see the headers of these scripts for instructions. They aren't exactly normal scripts. This is still 0.1.

## Contributers

- Sam Forester
- James Reynolds
- Topher Nadauld
- Tony Williams