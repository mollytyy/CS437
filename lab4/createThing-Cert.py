################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string

################################################### Directory management
import os
import shutil

################################################### Parameters for Thing
thingArn          = ''
thingId           = -1
thingName         = ''
defaultPolicyName = 'CPRS_policy'

thingDirPath      = ""
certificatePath   = ""
privateKeyPath    = ""
publicKeyPath     = ""

###################################################

def createThing():
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = thingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  for element in data: 
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
        createCertificate()


def createCertificate():
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
            setAsActive = True
    )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data: 
            if element == 'certificateArn':
                    certificateArn = data['certificateArn']
            elif element == 'keyPair':
                    publicKey = data['keyPair']['PublicKey']
                    privateKey = data['keyPair']['PrivateKey']
            elif element == 'certificatePem':
                    certificatePem = data['certificatePem']
            elif element == 'certificateId':
                    certificateId = data['certificateId']

    if os.path.exists(thingDirPath):
        shutil.rmtree(thingDirPath)
    os.mkdir(thingDirPath)

    with open(publicKeyPath, "w") as out:
        out.write(publicKey)
    with open(privateKeyPath, "w") as out:
        out.write(privateKey)
    with open(certificatePath, "w") as out:
        out.write(certificatePem)

    response = thingClient.attach_policy(
            policyName = defaultPolicyName,
            target     = certificateArn
    )
    response = thingClient.attach_thing_principal(
            thingName = thingName,
            principal = certificateArn
    )

###################################################

certsDirPath = "./certificates"
if os.path.exists(certsDirPath):
    shutil.rmtree(certsDirPath)
os.mkdir(certsDirPath)

thingCount = 5
thingClient = boto3.client('iot')
for i in range(thingCount):
    thingName = 'device_' + str(i)

    thingDirPath    = certsDirPath + "/" + thingName
    certificatePath = thingDirPath + "/" + "{}.certificate.pem".format(thingName)
    privateKeyPath  = thingDirPath + "/" + "{}.private.pem".format(thingName)
    publicKeyPath   = thingDirPath + "/" + "{}.public.pem".format(thingName)

    createThing()