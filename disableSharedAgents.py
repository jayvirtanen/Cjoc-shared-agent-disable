from email import header
from platform import release
from wsgiref import headers
import requests
import json
import sys
import getpass
import inquirer
from requests.auth import HTTPBasicAuth
from requests import get
from requests.exceptions import ConnectionError
import argparse

parser = argparse.ArgumentParser()
#Option for skipping Certificate validation
parser.add_argument('--insecure', default=True, action="store_false")
args= parser.parse_args()
jenkins_url = input("Enter jenkins url:")
username = input("Enter username:")
apiToken = getpass.getpass(prompt='API Token:')
questions = [inquirer.List('Action Type', message="What change would you like to carry out?",choices=['Nothing','Disable'])]
answers = inquirer.prompt(questions)
if (answers["Action Type"] == "Nothing"):
    print("Doing nothing, exiting")
    sys.exit()
if not(jenkins_url.startswith("http://") or jenkins_url.startswith("https://")):
    print ("Invalid url format")
    sys.exit()
try:
    response = requests.get(jenkins_url+'/cjoc/view/all/api/json',auth=HTTPBasicAuth(username, apiToken), verify=args.insecure)
    print(response.status_code)
    if (response.status_code == 200 and answers["Action Type"] == "Disable"):
        i=0
        crumb = requests.get(jenkins_url+'/cjoc/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)',auth=HTTPBasicAuth(username, apiToken), verify=args.insecure)
        jenkins_crumb= str(crumb.content).split(':')
        jenkins_crumb[1] = jenkins_crumb[1][:-1]
        header= {"Jenkins-Crumb": jenkins_crumb[1]}
        for jobs in response.json()['jobs']:
                if (response.json()['jobs'][i]['_class'] == "com.cloudbees.opscenter.server.model.SharedSlave"):
                        AgentName =  (response.json()['jobs'][i]['name'])
                        print("releasing " + AgentName)
                        releasePost = requests.post(jenkins_url + '/cjoc/job/' + AgentName + '/doForceRelease', headers= header, auth=HTTPBasicAuth(username, apiToken), verify=args.insecure)
                        if(releasePost.status_code == 200):
                            print(AgentName + " leases released successfully")
                        print("disabling " + AgentName)
                        disablePost = requests.post(jenkins_url + '/cjoc/job/' + AgentName + '/disable', headers= header , auth=HTTPBasicAuth(username, apiToken), verify=args.insecure)
                        if(disablePost.status_code == 200):
                            print(AgentName + " disabled successfully")
                i=i+1
    else:
        print ("Invalid credentials")
        sys.exit()
except ConnectionError:
    print ("Invalid Url")

