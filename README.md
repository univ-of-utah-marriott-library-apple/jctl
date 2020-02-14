# jctl

Utility for updating Patch Management in JSS
Python 3 experimentation

This is a util for maintaining Jamf Pro via command-line

# A work in progress

This library is nowhere near finished, I submitted it to allow a colleague to help with its development.

# Requirements

jamfutil requires python3 and requests library


# A Few Examples

The api can be interacted with via python3 shell

`> python3`

```python
import pprint
import jamf
import logging

fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)

# create an jamf.API object (requires requests lib)
logger.debug("creating api")
jss = jamf.API()

# get any information from your jss using the classic api endpoints

# print out all policies
all_policies = jss.get('policies')
pprint.pprint(all_policies)

# get all categories
import jamf.category
pprint.pprint([x.name for x in jamf.category.Categories()])


# all policies in a for first and second category
pprint.pprint(policies)
```

That's all I have currently

# Installation

```bash
# bash
$> cd scripts
$> sudo install.py
$> echo 'export PYTHONPATH=/Library/Python/3.6/site-packages' >> ~/.profile
```

In a new shell
```bash
# get help with `patch.py`
$> patch.py --help
$> patch.py list --help
$> patch.py upload --help
$> patch.py config --help
$> patch.py remove --help
$> patch.py info --help
$> patch.py update --help

# list information about patch
# list all Patch Management Title Names
$> patch.py list

# list all uploaded packages
$> patch.py list --pkgs

# list all versions (and associated package for <Name of Patch Management Title>
$> patch.py list --versions <Name of Patch Management Title>
$> patch.py list --patches <Name of Patch Management Title>

# requires user to have Jamf Admin Privileges
$> patch.py info /PATH/TO/PACKAGE
$> patch.py upload /PATH/TO/PACKAGE
$> patch.py remove <PACKAGE NAME>
```
