# jctl

This is a Python 3 utility for maintaining & automating Jamf Pro patch management via command-line. The idea behind it is to have a class that maps directly to the Jamf API (https://example.com:8443/api). The API class doesn't abstract anything or hide anything from you. It simply wraps the url requests, authentication, and converts between python dictionaries and xml. It also prints json.

## Under construction!

Note: we are currently (late 2020) splitting this project into 2 different repositories and adding it to pypi.org so that it can be easily installed with pip. Because we are in the middle of the move, we haven't finished updating this readme to reflect all of those changes. The last commit before we started making changes is  [9e8343eb10](https://github.com/univ-of-utah-marriott-library-apple/jctl/tree/9e8343eb10634ee74cd6024885e348672146181d).

## Requirements

The jctl project requires python3, the requests library, and python-jamf. Please make sure you have those by running the following commands.

```bash
python3
```

```python
import requests
```

macOS does not include python3. You can get python3 with anaconda or homebrew.


### Authentication Setup

Run the following command to setup or fix the authentication property list file.

```$ config.py config
JSS Hostname: [JAMF PRO HOSTNAME]
username: [USERNAME]
Password: [PASSWORD]
```

The username and password provided will have to be added and given the appropriate access rights.

To quickly test, run this.

```$ config.py test
```

It will print a list of accounts.

For more information on the authentication setup, see python-jamf.

### Updating policies en masse.

Scripts that do very similar things as the above two scripts are as follows:

* policy_categories.py, allows you to change all policy categories at once
* policy_packages.py, allows you to change all policy packages at once

Please see the headers of these scripts for instructions. They aren't exactly normal scripts. This is still 0.1.

## patch.py

### Getting Help

```
patch.py --help
patch.py list --help
patch.py upload --help
patch.py config --help
patch.py remove --help
patch.py info --help
patch.py update --help
```

### List all Patch Management Title Names
```patch.py list```

### List all uploaded packages
`patch.py list --pkgs`

### List all versions (and associated packages)
```
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

## Contributers

- Sam Forester
- James Reynolds
- Topher Nadauld
- Tony Williams