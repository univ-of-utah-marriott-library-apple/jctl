# jamfutil

Utility for updating Patch Management in JSS
Python 3 experimentation

This is a utility for maintaining & automating Jamf Pro patch manage via command-line

# A work in progress

This library is nowhere near finished, I submitted it to allow a colleague to help with its development.

# Requirements

jamfutil requires python3 and requests library

# Authentication

## Authentication Setup

Run the following command to setup or fix the authentication property list file.

```$ patch.py config
JSS Hostname: [JAMF PRO HOSTNAME]
username: [USERNAME]
Password: [PASSWORD]
```

The username and password provided will have to be added and given the appropriate access rights.

## Troubleshooting Authentication Setup

The above command should reset the authorization property list, but if you have issues with it not working properly delete the property list file and run the command above again.

`rm ~/Library/Preferences/edu.utah.mlib.jamfutil.plist`


## Authenication File Obfuscation

The authorization property list is obfuscated and encrypted based upon the hostname of the Jamf Pro server and user credentials.

## View Authentication File

To view what is stored in this property list, you could use a command-line tool like `cat`, `less`, etc.

For example...

```
$ cat ~/Library/Preferences/edu.utah.mlib.jamfutil.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Credentials</key>
	<data>
	YnBsaXN0MDSRAQRfEBNjYXNwZXIuc2NsLnV0YWguZWR1TxBCH/k+SqHI7doBuB0l/GIS
	4onl2JLjVwjkMFax1+6YgrEUaYlSI9K83euiuR99iVIj0r/d6qO5H32JUiPSvN3qo7kA
	CAshAAAAAAAAAQEAAAAAAAAAAwAAAAAAAAAAAAAAACAAAGY=
	</data>
	<key>JSSHostname</key>
	<string>jamf.domain.edu</string>
</dict>
</plist>
```

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
jss = jamf.API(config='private/jss.plist')

# get any information from your jss using the classic api endpoints

# print out all policies
all_policies = jss.get('policies')
pprint.pprint(all_policies)

# get all categories
categories = jamf.policy.categories(jss)

category_names = [x['name'] for x in categories]

print(f"first category: {category_names[0]}")

# all policies in a for first and second category
policies = jamf.policy.policies_in_categories(jss, categories[0:2])
pprint.pprint(policies)
```

# Installation

In a new shell:

```
$> cd scripts
$> sudo install.py
$> echo 'export PYTHONPATH=/Library/Python/3.6/site-packages' >> ~/.profile
```

## Getting Help
```
$> patch.py --help
$> patch.py list --help
$> patch.py upload --help
$> patch.py config --help
$> patch.py remove --help
$> patch.py info --help
$> patch.py update --help
```

## List all Patch Management Title Names
```$> patch.py list```

## List all uploaded packages
`$> patch.py list --pkgs`

## List all versions (and associated packages)
```
$> patch.py list --versions <Name of Patch Management Title>
$> patch.py list --patches <Name of Patch Management Title>
```

## Requires user to have Jamf Admin Privileges

```
$> patch.py info /PATH/TO/PACKAGE
$> patch.py upload /PATH/TO/PACKAGE
$> patch.py remove <PACKAGE NAME>
```
	</data>
	<key>JSSHostname</key>
	<string>jamf.domain.edu</string>
</dict>
</plist>
```


# Installation

In a new shell:

```
$> cd scripts
$> sudo install.py
$> echo 'export PYTHONPATH=/Library/Python/3.6/site-packages' >> ~/.profile
```

## Getting Help
```
$> patch.py --help
$> patch.py list --help
$> patch.py upload --help
$> patch.py config --help
$> patch.py remove --help
$> patch.py info --help
$> patch.py update --help
```

## List all Patch Management Title Names
`$> patch.py list`

## List all uploaded packages
`$> patch.py list --pkgs`

## List all versions (and associated packags)
```
$> patch.py list --versions <Name of Patch Management Title>
$> patch.py list --patches <Name of Patch Management Title>
```

## Requires user to have Jamf Admin Privileges
```
$> patch.py info /PATH/TO/PACKAGE
$> patch.py upload /PATH/TO/PACKAGE
$> patch.py remove <PACKAGE NAME>
```
