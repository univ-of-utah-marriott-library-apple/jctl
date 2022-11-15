# jctl

## Introduction

`jctl` is a command line tool that performs CRUD (Create/Read/Update/Delete) operations on a [Jamf Pro or Jamf Cloud](https://www.jamf.com/) server. It can automate repetitive tasks and provide options not available in the web GUI. It uses and is the primary driver of [`python-jamf`](https://github.com/univ-of-utah-marriott-library-apple/python-jamf), which is a Python 3 module for the [Jamf Pro Classic API](https://www.jamf.com/resources/videos/an-introduction-to-the-classic-api/). 

There are a few other tools that are part of this project. `pkgctl` is automates various operations with packages, such as promotion and creating patch definitions. `patch.py` is a deprecated script designed to automate the patching process. It is still part of the project because it can do a few things that `jctl` can't. However, it is not being tested. `update_asset_tags.py` was demoed at the 2021 JNUC presentation [_Turn 1000 clicks into 1 with python-jamf and jctl_](https://www.youtube.com/watch?v=2YLriNwyP3s). We decided to include it here. It is not being tested either.

`jctl` only supports 56 Jamf Pro record types. `python-jamf` can access all record types.  `python-jamf` stores the Jamf Pro credentials in the keychain using [keyring](https://github.com/jaraco/keyring) (instead of cleartext, like all other Jamf API projects that we know of).

## Quick Start

If you don't have Python installed, you need to read about [Installing Python](https://github.com/univ-of-utah-marriott-library-apple/jctl/wiki/Installing-Python) on the wiki.

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

See the [releases](https://github.com/univ-of-utah-marriott-library-apple/jctl/releases) page for details.

See `jctl` [upgrade](https://github.com/univ-of-utah-marriott-library-apple/jctl/wiki/Installing#upgrading) documentation to upgrade to latest release.
