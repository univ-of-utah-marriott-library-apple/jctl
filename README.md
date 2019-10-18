# jamfutil

Utility for updating Patch Management in JSS
Python 3 experimentation

This is a util for maintaining Jamf Pro via command-line

# authentication

Run the following command from inside the repo ('private/' is in .gitignore)
```bash
$ mkdir private
$ cat <<EOT > private/jss.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>login</key>
	<string>username:passwd</string>
	<key>address</key>
	<string>jamf.server.url</string>
</dict>
</plist>
EOT
```

# API access 

The api can be interacted with via python3 shell

```python3
import pprint
import jamf

# create an jamf.API object
api = jamf.API(config='private/jss.plist')

# get any information from your jss using the classic api endpoints

policy = api.get('policies/id/1')
pprint.pprint(policy)
```