# jctl


## Introduction

`jctl` is a command line based tool to make using `python-jamf`, a Python 3 module to access Jamf Pro Classic API, easier to use. `jctl` uses `python-jamf` to select objects to create, delete, print and update. It allows performing Jamf Pro repetitive tasks quickly and provides options not available in the web GUI. It is similar to SQL statements, but far less complex.

Along with `jctl` there are a few other tools that utilize `jctl` and `python-jamf`.

`patch.py` is a script designed to automate the patching process.

`pkgctl` is similar to `patch.py` but with a command line interface.

#### What are `python-jamf` and `jctl`?

Originally, it was a "patch" project that was focused on patch management including installer package management, patch management, including assigning package to patch definition, updating versions, version release branching (i.e. development, testing, production), and scripting and automation. Later, it was split into two projects, `python-jamf`, which is a python library that connects to a Jamf Pro server using Jamf Pro Classic API, including keychain support for Jamf Pro credentials via [keyring](https://github.com/jaraco/keyring) python project, support for [PyPi](https://pypi.org/project/python-jamf/) to support pip installation and currently supports 56 Jamf Pro record types which will expand in number as the project continues.

For more information on how [python-jamf](https://github.com/univ-of-utah-marriott-library-apple/python-jamf) works, please visit the Github page.

## Quick Start

### Installing

 - Install Module & Requirements: `sudo pip3 install jctl`
 - On your Jamf Pro server create a Jamf Pro API User
 - Config: `conf-python-jamf`
 - Enter hostname, username, and password
 - Test: `conf-python-jamf -t`

### Uninstalling

Uninstalling `jctl` is easy if you installed it via `pip`. `pip` is the **P**ackage **I**nstaller for **P**ython.

To uninstall `jctl` run the following command:

```bash
sudo pip3 uninstall jctl
```

### Upgrading

Upgrading `jctl` is easy if you installed it via `pip`. `pip` is the **P**ackage **I**nstaller for **P**ython.

To upgrade `jctl` run the following command:

```bash
sudo pip3 install --upgrade jctl
```

## Getting Help

### Wiki

#### More Documentation

For further in-depth details please check out [the wiki](https://github.com/univ-of-utah-marriott-library-apple/jctl/wiki).

#### Searching the wiki

To search this wiki use the "Search" field in the GitHub navigation bar above. Then on the search results page select the "Wiki" option or [click here](https://github.com/univ-of-utah-marriott-library-apple/jctl/search?q=&type=Wikis&utf8=✓) and search.

### MacAdmin Slack Channel

If you have additional questions, or need more help getting started, post a question on the MacAdmin's Slack [jctl](https://macadmins.slack.com/archives/C01C8KVV2UD) channel.

<p align="center">
<img src="https://github.com/univ-of-utah-marriott-library-apple/python-jamf/wiki/images/MacAdmins_Slack_logo.png" alt="MacAdmin's Slack Logo">
</p>

## Latest Status

### Releases

#### :new: [jctl - 1.1.17](https://github.com/univ-of-utah-marriott-library-apple/jctl/releases/tag/1.1.17)

- jctl: Changed the json output so it's much easier to parse (with something like [jq](https://stedolan.github.io/jq/))
- jctl: Non-json output prints record name first when printing paths
- jctl: Added --print-id (when you need to capture the id of a record to use in another command)
- jctl: Added --debug
- jctl: `-s` now can do `!=~`
- jctl: `-s` `~=` is deprecated, switching it to `=~`
- pre-commit updated to 4.3.0
- GitHub action updated action names

Example of the new features.

Getting the ID of the Zoom patch software title using `jq`:

	zoomid=`jctl patchsoftwaretitles -r "Zoom Client for Meetings" -p id -j | jq '.[].id | .[] | tonumber'`

Getting the ID of the Zoom patch software title using --print_id:

	zoomid=`jctl patchsoftwaretitles -r "Zoom Client for Meetings" -I`

Using the ID

	jctl packages -c "Zoom-5.11.11 (10514).pkg"
	jctl patchpolicies -c "Zoom 1" $zoomid "5.11.11 (10514)"

Formatting the json output with `jq`:

```
jctl computergroups -i 2 -j -l | jq
[
  {
    "id": "2",
    "name": "All Managed Servers",
    "is_smart": "true",
    "site": {
      "id": "-1",
      "name": "None"
    },
    "criteria": {
      "size": "2",
      "criterion": [
        {
          "name": "Operating System",
          "priority": "0",
          "and_or": "and",
          "search_type": "like",
          "value": "server",
          "opening_paren": "false",
          "closing_paren": "false"
        },
        {
          "name": "Application Title",
          "priority": "1",
          "and_or": "or",
          "search_type": "is",
          "value": "Server.app",
          "opening_paren": "false",
          "closing_paren": "false"
        }
      ]
    },
    "computers": {
      "size": "0"
    }
  }
]
```

Here's what it looks like when you specify paths.

```
jctl policies -n "Install Zoom" -p package_configuration -p general/name -j | jq
[
  {
    "package_configuration": {
      "packages": {
        "size": "2",
        "package": [
          {
            "id": "1",
            "name": "Zoom-5.11.11 (10514).pkg",
            "action": "Install",
            "fut": "false",
            "feu": "false"
          }
        ]
      }
    },
    "general/name": "Install Zoom"
  }
]
```

Non-json output shows the record name first (the output is still generated by pprint):

```
jctl computergroups -i 2 -l
{'All Managed Servers': {'computers': {'size': '0'},
                         'criteria': {'criterion': [{'and_or': 'and',
                                                     'closing_paren': 'false',
                                                     'name': 'Operating System',
                                                     'opening_paren': 'false',
                                                     'priority': '0',
                                                     'search_type': 'like',
                                                     'value': 'server'},
                                                    {'and_or': 'or',
                                                     'closing_paren': 'false',
                                                     'name': 'Application '
                                                             'Title',
                                                     'opening_paren': 'false',
                                                     'priority': '1',
                                                     'search_type': 'is',
                                                     'value': 'Server.app'}],
                                      'size': '2'},
                         'id': '2',
                         'is_smart': 'true',
                         'name': 'All Managed Servers',
                         'site': {'id': '-1', 'name': 'None'}}}
```

Showing the record name first is very helpful when printing paths:

```
jctl computergroups -p is_smart
{'All Managed Clients': {'is_smart': 'true'}}
{'All Managed Servers': {'is_smart': 'true'}}
Count: 2
```

Comparing `=~` with `!=~`:

```
jctl computergroups -s name=~Cl
All Managed Clients
jctl computergroups -s name!=~Cl
All Managed Servers
```

Debugging output (yes, this shows the bearer token for my localhost server):

```
jctl computergroups --debug
2022-10-02 16:55:36,447:    DEBUG: __main__ - main(): Warning, debugging output may contain passwords, tokens, or other sensitive information!
2022-10-02 16:55:36,447:    DEBUG: __main__ - main(): args: Namespace(record='computergroups', create=None, update=None, delete=False, sub_command=None, id=None, name=None, regex=None, searchpath=None, print_id=False, long=False, path=None, json=False, quiet_as_a_mouse=False, config=None, version=False, use_the_force_luke=False, andele_andele=False, debug=True)
2022-10-02 16:55:36,494:    DEBUG: jamf.api.API - _submit_request(): post: http://localhost/api/v1/auth/keep-alive
2022-10-02 16:55:36,759:    DEBUG: jamf.api.API - _submit_request(): response.text: {
  "token" : "eyJhbGciOiJIUzI1NiJ9.eyJhdXRoZW50aWNhdGVkLWFwcCI6IkdFTkVSSUMiLCJhdXRoZW50aWNhdGlvbi10eXBlIjoiSlNTIiwiZ3JvdXBzIjpbXSwic3ViamVjdC10eXBlIjoiSlNTX1VTRVJfSUQiLCJ0b2tlbi11dWlkIjoiNGE0OGEyNzItZjFiZi00NjkwLWE5YjQtYTU4NjZkNDI2MGJlIiwibGRhcC1zZXJ2ZXItaWQiOi0xLCJzdWIiOiIxIiwiZXhwIjoxNjY0NzUzMTM2fQ.FEOy4rUenvZm3Gc_mrXk3qUnpcFmCtzneKKKs_hW-hk",
  "expires" : "2022-10-02T23:25:36.754Z"
}
2022-10-02 16:55:36,832:    DEBUG: jamf.api.API - _submit_request(): get: http://localhost/api/v1/jamf-pro-version
2022-10-02 16:55:36,860:    DEBUG: jamf.api.API - _submit_request(): response.text: {
  "version" : "10.41.0-t1661887915"
}
2022-10-02 16:55:36,861:    DEBUG: jamf.api.API - _submit_request(): get: http://localhost/JSSResource/computergroups
2022-10-02 16:55:36,904:    DEBUG: jamf.api.API - _submit_request(): response.text: <?xml version="1.0" encoding="UTF-8"?><computer_groups><size>2</size><computer_group><id>1</id><name>All Managed Clients</name><is_smart>true</is_smart></computer_group><computer_group><id>2</id><name>All Managed Servers</name><is_smart>true</is_smart></computer_group></computer_groups>
All Managed Clients
All Managed Servers
Count: 2
2022-10-02 16:55:36,922:    DEBUG: jamf.api.API - __del__(): closing session
```

#### [jctl - 1.1.16](https://github.com/univ-of-utah-marriott-library-apple/jctl/releases/tag/1.1.16)

- This release includes the xml array fix described [here](https://github.com/univ-of-utah-marriott-library-apple/python-jamf/blob/07378f0397744f52af54dbadb798e057d5e0c6cf/README.md#known-breaking-changes-on-the-roadmap).
- Fixed `pkgctl --config` arg
- Fixed `pkgctl --version`
- Formatting changes

#### [jctl - 1.1.15](https://github.com/univ-of-utah-marriott-library-apple/jctl/releases/tag/1.1.15-a6bb5795)

- Added update_asset_tags.py to project as standalone script
- pkgctl prints warning if it gets an error trying to update data

See `jctl` [upgrade](https://github.com/univ-of-utah-marriott-library-apple/jctl/wiki/Installing#upgrading) documentation to upgrade to latest release.
