# jctl


## Introduction

`jctl` is a command line based tool to make using `python-jamf`, a Python 3 module to access Jamf Pro Classic API, easier to use. `jctl` uses `python-jamf` to select objects to create, delete, print and update. It allows performing Jamf Pro repetitive tasks quickly and provides options not available in the web GUI. It is similar to SQL statements, but far less complex.

Along with `jctl` there are a few other tools that utilize `jctl` and `python-jamf`.

`patch.py` is a script designed to automate the patching process.

`pkgctl` is similar to `patch.py` but with a command line interface.

For more information on how [python-jamf](https://github.com/univ-of-utah-marriott-library-apple/python-jamf) works, please visit the Github page.


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

### Virtual JNUC 2021 Presentation

We presented on `python-jamf` and `jctl` at the the Virtual JNUC 2021 on Thursday, Oct 21 at 1:00 PM - 1:30 PM MDT, titled [Turn 1000 clicks into 1 with python-jamf and jctl](https://reg.jamf.com/flow/jamf/jnuc2021/sessioncatalog/page/sessioncatalog/session/1620431676367001smXi). The presentation [video](https://reg.jamf.com/flow/jamf/jnuc2021/sessioncatalog/page/sessioncatalog/session/1620431676367001smXi) & [slides](https://github.com/univ-of-utah-marriott-library-apple/python-jamf/wiki/images/virtual_jnuc_2021-turn_1000_clicks_into_1_with_python-jamf_and_jctl.pdf) are available.

Since 2010, Apple IT, users, and InfoSec leaders from around the world have rallied at the Jamf Nation User Conference (JNUC) for community presentations, deep-dive education sessions, and expert product insights. Focusing on new and better ways to connect, manage and protect Apple devices that simplify workflows for IT and InfoSec and keep users productive. The Virtual JNUC 2021 experience will be October 19 - October 21, 2021, and there will be no cost to attend the online keynote and sessions.

Anyone and everyone is invited to register for the [virtual experience](https://reg.jamf.com/flow/jamf/jnuc2021/reg/login).

#### What are `python-jamf` and `jctl`?

Originally, it was a "patch" project that was focused on patch management including installer package management, patch management, including assigning package to patch definition, updating versions, version release branching (i.e. development, testing, production), and scripting and automation. Later, it was split into two projects, `python-jamf`, which is a python library that connects to a Jamf Pro server using Jamf Pro Classic API, including keychain support for Jamf Pro credentials via [keyring](https://github.com/jaraco/keyring) python project, support for [PyPi](https://pypi.org/project/python-jamf/) to support pip installation and currently supports 56 Jamf Pro record types which will expand in number as the project continues.

Our presentation will cover how it works internally as a simple alternative to the usual cURL usage; usage example of workflows comparing using Jamf Pro web interface vs `jctl`; and lastly advanced usage and package management including example os subcommands for specific object types, filtering making interacting with the API simple & easy.
