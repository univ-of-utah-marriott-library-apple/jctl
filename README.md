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
