import json
import requests
from datetime import datetime
import os
import sys
import subprocess
import socket
import urllib.parse
import time

def isOpen(ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()

def checkHost(ip, port):
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup

elasticUrl = os.environ.get('ES_URL')
elasticUser = os.environ.get('ES_USER')
elasticPW = os.environ.get('ES_PW')

inspecUser = os.environ.get('INSPEC_USER')
inspecPass = os.environ.get('INSPEC_PW')
inspectGitRepo = os.environ.get('INSPEC_GIT')

freeIpaURL = os.environ.get('FREEIPA_URL')

###
### Let's get all the hosts from the FreeIPA server
###


### Authentification
url = "https://" + urllib.parse.quote(freeIpaURL) + '/ipa/session/login_password'
data = "user=" + urllib.parse.quote(inspecUser) + "&password=" + urllib.parse.quote(inspecPass)
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "text/plain",
    'Referer': "https://" + urllib.parse.quote(freeIpaURL) + "/ipa"
    }

r = requests.post(url,data=data, headers=headers)

### Fetching all the hosts
url = "https://" + urllib.parse.quote(freeIpaURL) + '/ipa/session/json'
headers = {
    'Content-Type':'application/json',
    'Accept':'text/plain',
    'Referer':"https://" + urllib.parse.quote(freeIpaURL) + "/ipa"
    }
hosts = {
        "method": "host_find", 
        "params": [
            [""],
            {
                "all": "true",
                "version": "2.231"
            }
            ],
            "id": 0
        }
r = requests.post(url,json=hosts,cookies=r.cookies,headers=headers)
ipaData = r.json()

###
### Once we got them, let's call Inspec to scan those hosts.
### Be sure to have a valid user that scan all of them.
### This can be done using a valid RBAC and SUDO rules
###

for ipaItem in ipaData['result']['result']:
    retry = 5
    delay = 10
    timeout = 3

    if checkHost(ipaItem['fqdn'][0], 22):
        subprocess.call(['inspec','exec', '-t','ssh://' + inspecUser + ':' + inspecPass + '@' + ipaItem['fqdn'][0],inspectGitRepo,'--reporter','json-min:/share/' + ipaItem['fqdn'][0]])
        if os.path.isfile('/share/' + ipaItem['fqdn'][0]):
            inspecFile = open('/share/' + ipaItem['fqdn'][0])
            inspecData = json.load(inspecFile)
            inspecFile.close()

            ###
            ### Let's put the Inspec results in an ElasticSearch service
            ###
            for inspecItem in inspecData['controls']:
                dateAct =  datetime.now()
                dateFormat = dateAct.strftime("%d/%m/%Y %H:%M:%S")
                inspecItem['host'] = ipaItem['fqdn'][0]
                inspecItem['date'] = dateFormat
                url = 'https://' + urllib.parse.quote(elasticUrl) + '/inspec/_doc'
                headers = {'Content-Type': 'application/json'}
                r = requests.post(url,json=inspecItem,headers=headers,auth=(elasticUser,elasticPW))
            os.remove('/share/' + ipaItem['fqdn'][0])