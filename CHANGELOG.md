# Changelog

All notable changes to this project (since the addition of this file) will be documented
in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/). This project will (try to) adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.23] -- 2024-02-05

### Fixed
- jctl: searchpath ignore JamfRecordInvalidPath errors

## [1.1.22] -- 2024-01-29

### Changed
- update_asset_tags.py: renamed jamf to python_jamf
- patch.py: renamed jamf to python_jamf
- setup.py: add py_modules key

## [1.1.21] -- 2024-01-03

- pkgctl updates multiple policies/groups at once

## [1.1.20] -- 2023-11-06

### Added
- Added CHANGELOG
- jctl and pkgctl: Load config file in a try block to catch errors
- jctl "-i -" will obtain id's from stdin

### Changed
- Requires python-jamf 0.9.0
- jctl import jamf.exceptions
- jctl Rename jamf to python_jamf
- jctl --create can now take a name or json
- jctl Changed how -update args are processed
- jctl Changed how path is printed using json
- jctl Changed where the hostname is confirmed
- jctl Split main function into multiple functions for clarity
- jctl Sped up deleting records
