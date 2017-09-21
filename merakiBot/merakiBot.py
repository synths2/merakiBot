# A suite of functions to interact with the Meraki API
#
#
#

import requests, json, logging
from merakiConfig import apiKey,apiVersion


def getOrganisations(baseURL, headers):
    url = baseURL + "/organizations"
    response = requests.get(url=url, headers=headers, verify= False)
    if response.status_code == 200:
        return response.text
    elif response.status_code  in [302,307,308]:
        url = response.text.find(sub='https')
        print "redirecting to: " + url
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code  == 200:
            return response.text
        else:
            print "There was an issue with your request. Here is the error text:\n" + response.text
    else:
        print "There was an issue with your request. Here is the error text:\n" + response.text


def getNetworkIDs(baseURL, headers, orgID):
    print "Getting networks..."
    url = baseURL + "/organizations/" + str(orgID) + "/networks"
    response = requests.get(url=url, headers=headers, verify=False)
    networkIDs = json.loads(response.text)
    if response.status_code == 200:
        nlist = []
        for net in networkIDs:
            emptynet = {}
            emptynet['name'] = net['name']
            emptynet['id'] = net['id']
            nlist.append(emptynet)
        return nlist

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


def getDevices(baseURL, headers, networkID):
    print "Getting devices..."
    print "number of networks:" + str(len(networkID))
    dlist = []
    for net in networkID:
        netID = net['id']
        url = baseURL + "/networks/" + str(netID) + "/devices"
        response = requests.get(url=url, headers=headers, verify=False)
        if response.status_code == 200:
            deviceIDs = json.loads(response.text)

            for dev in deviceIDs:
                emptydev = {}
                emptydev['name'] = dev['name']
                emptydev['serial'] = dev['serial']
                dlist.append(emptydev)

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
    return dlist


def findClientDetails(baseURL, headers, deviceID, timespan="86400"):
    url = baseURL + "/devices/" + str(deviceID) + "/clients" + "?timespan=" + timespan
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


if __name__ == "__main__":
    baseURL = "https://dashboard.meraki.com/api/v" + apiVersion
    headers = {"X-Cisco-Meraki-API-Key" : apiKey}
    organisations = json.loads(getOrganisations(baseURL, headers))
    organisationID = organisations[0]['id']
    print "organisationID = " + str(organisationID)
    networkIDs = getNetworkIDs(baseURL, headers, organisationID)
    print len(networkIDs)
    devices = getDevices(baseURL, headers, networkIDs)
