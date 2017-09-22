# A suite of functions to interact with the Meraki API
#
#
#

import requests, json, logging
from merakiConfig import apiKey, apiVersion, verifySSL


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
    else:
        print "There was an issue with your request. Here is the error text:\n" + response.text


def getDevices(baseURL, headers, networkID):
    print "Getting devices..."
    print "number of networks:" + str(len(networkID))
    s = requests.Session()
    s.headers.update(headers)
    s.verify = verifySSL
    dlist = []
    for net in networkID:
        netID = net['id']
        url = baseURL + "/networks/" + str(netID) + "/devices"
        response = s.get(url=url)
        if response.status_code == 200:
            deviceIDs = json.loads(response.text)

            for dev in deviceIDs:
                emptydev = {}
                emptydev['name'] = dev['name']
                emptydev['serial'] = dev['serial']
                dlist.append(emptydev)
        else:
            print "There was an issue with your request. Here is the error text:\n" + response.text
    s.close()
    return dlist


def getClientDetails2(baseURL, headers, deviceID, timespan="86400"):
    print "Getting clients..."
    s = requests.Session()
    s.headers.update(headers)
    s.verify = verifySSL
    clist = []
    for dev in deviceID:
        devID = dev['serial']
        url = baseURL + "/devices/" + str(devID) + "/clients?timespan=" + timespan
        response = s.get(url=url)
        if response.status_code == 200:
            clients = json.loads(response.text)
            i=0
            for client in clients:
                print "client number: " + i
                i=i+1
                emptycli = {}
                emptycli['description'] = client['description']
                emptycli['ip'] = client['ip']
                emptycli['mac'] = client['mac']
                emptycli['apID'] = client['id']
                emptycli['apName'] = (item for item in devices if item["serial"] == client["id"])
                clist.append(emptycli)
        else:
            print "There was an issue with your request. HTTP Code was:" + response.status_code + ". Here is the error text:\n" + response.text
    dedupe = [i for n, i in enumerate(clist) if i not in clist[n + 1:]]
    s.close()
    return dedupe


def getGroupPolicies(baseURL, headers, networkID):
    print "Getting policies..."
    s = requests.Session()
    s.headers.update(headers)
    s.verify = verifySSL
    plist = []
    url = baseURL + "/networks/" + str(networkID) + "/groupPolicies"
    response = s.get(url=url)
    if response.status_code == 200:
        policies = json.loads(response.text)
        for policy in policies:
            emptydev = {}
            emptydev['name'] = policy['name']
            emptydev['groupPolicyId'] = policy['groupPolicyId']
            plist.append(emptydev)
    else:
         print "There was an issue with your request. Here is the error text:\n" + response.text
    s.close()
    return plist


def getClientPolicy(baseURL, headers, networkID, clientMAC, timespan = "86400"):
    s = requests.Session()
    s.headers.update(headers)
    s.verify = verifySSL
    url = baseURL + "/networks/" + str(networkID) + "/clients/" + clientMAC + "/policy?timespan=" + timespan
    response = s.get(url=url)
    if response.status_code == 200:
        policy = json.loads(response.text)
        policyID = policy["groupPolicyId"]
    else:
        print "There was an issue with your request. Here is the error text:\n" + response.text
    s.close()
    return json.dumps(policyID)


if __name__ == "__main__":
    baseURL = "https://dashboard.meraki.com/api/v" + apiVersion
    headers = {"X-Cisco-Meraki-API-Key" : apiKey}
    organisations = json.loads(getOrganisations(baseURL, headers))
    organisationID = organisations[0]['id']
    print "organisationID = " + str(organisationID)
    networkIDs = getNetworkIDs(baseURL, headers, organisationID)
    devices = getDevices(baseURL, headers, networkIDs)
    clients = getClientDetails2(baseURL, headers, devices)
    client = next((item for item in clients if item["ip"] == "172.30.22.41"), "Not found")
    groupPolicies = getGroupPolicies(baseURL, headers, networkIDs)


