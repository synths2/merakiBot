# A suite of functions to interact with the Meraki API
#
#
#

import requests, json, logging
from merakiConfig import apiKey,apiVersion


def getOrganisations(baseURL, headers):
    url = baseURL + "/organizations"
    response = requests.get(url=url, headers=headers, verify='./global-legal-root.crt.cer')
    if response.status_code == 200:
        return response.text
    elif response.status_code  in [302,307,308]:
        url = response.text.find(sub='https')
        print "redirecting to: " + url
        response = requests.get(url=url, headers=headers, verify='./global-legal-root.crt.cer')
        if response.status_code  == 200:
            return response.text
        else:
            print "There was an issue with your request. Here is the error text:\n" + response.text
    else:
        print "There was an issue with your request. Here is the error text:\n" + response.text


def getNetworks(baseURL, headers, orgID):
    url = baseURL + "/organizations/" + str(orgID) + "/networks"
    print url
    response = requests.get(url=url, headers=headers, verify='./global-legal-root.crt.cer')
    if response.status_code == 200:
        return response.text
    elif response.status_code in [302, 307, 308]:
        url = response.text.find(sub='https')
        print "redirecting to: " + url
        response = requests.get(url=url, headers=headers, verify='./global-legal-root.crt.cer')
        if response.status_code == 200:
            return response.text
        else:
            print "There was an issue with your request. Here is the error text:\n" + response.text
    else:
        print "There was an issue with your request. Here is the error text:\n" + response.text


def findClientDetails(baseURL, headers, clientIP):
    pass

if __name__ == "__main__":
    baseURL = "https://dashboard.meraki.com/api/v" + apiVersion
    headers = {"X-Cisco-Meraki-API-Key" : apiKey}
    organisations = json.loads(getOrganisations(baseURL, headers))
    organisationID = organisations[0]['id']
    print "organisationID = " + str(organisationID)
    networks = json.loads(getNetworks(baseURL, headers, organisationID))
    print json.dumps(networks)