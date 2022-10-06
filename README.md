# DisableSharedAgents

This script does the following:
1. Releases all leases on CJOC shared agents
2. Disables all CJOC shared agents

## Prerequisite :
### Python3 with packages - json, sys, getpass, inquirer, requests

## Usage:
Run the python script "disableSharedAgents.py" in this repo.

### python3 disableSharedAgents.py
This will ask for user inputs such as :
1) Enter jenkins url: example url - "http://example.jenkinshost"
2) Enter username:
3) API Key:
4) A prompt to confirm the disable action

## Options:
--insecure
Disables certificate validation on https requests
