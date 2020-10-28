# jctl

This is a Python 3 utility for maintaining & automating Jamf Pro patch management via command-line. The idea behind it is to have a class that maps directly to the Jamf API (https://example.com:8443/api). The API class doesn't abstract anything or hide anything from you. It simply wraps the url requests, authentication, and converts between python dictionaries and xml. It also prints json.

## Under construction!

Note: we are currently (late 2020) splitting this project into 2 different repositories and adding it to pypi.org so that it can be easily installed with pip. Because we are in the middle of the move, we haven't updated this readme to reflect any of those changes. These instructions are accurate for commit [9e8343eb10](https://github.com/univ-of-utah-marriott-library-apple/jctl/tree/9e8343eb10634ee74cd6024885e348672146181d).

## Requirements

The jctl project requires python3, the requests library, and python-jamf. Please make sure you have those by running the following commands.

```bash
$> python3
```

```python
import requests
```

macOS does not include python3. You can get python3 with anaconda or homebrew.
