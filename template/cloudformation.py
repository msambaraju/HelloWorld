#!/usr/bin/python

import time
import getopt
import sys
import json

# accesskey, secret,keyname, stackname, rollbacktimeout, waittime
options, remainder = getopt.getopt(sys.argv[1:], '', ['accesskey=','secret=','keyname=','stackname=','rollbacktimeout=','waittime='])

for opt, arg in options:
    if opt == '--accesskey':
        accessKey = arg
    elif opt =='--secret':
        secretKey = arg
    elif opt == '--keyname':
        keyPairName = arg
    elif opt == '--stackname':
        stackName= arg
    elif opt == '--rollbacktimeout':
        rollbacktimeout = arg
    elif opt == '--waittime':
        waittime = arg
        
'''
print accessKey
print secretKey
print keyPairName
print stackName
print rollbacktimeout
print waittime
'''
cloudFormationOutput = {}



from boto.s3.connection import S3Connection
s3conn = S3Connection(accessKey, secretKey)
s3conn.auth_region_name = 'us-east-1'
bucket = s3conn.create_bucket('ipmstempbucket_0101')

from boto.s3.key import Key
bucketKey = Key(bucket)
bucketKey.key = 'templatefile'
bucketKey.set_contents_from_filename('docker_server.template')
s3url = "https://s3.amazonaws.com/ipmstempbucket_0101/templatefile"


from boto.cloudformation.connection import CloudFormationConnection
cfConn = CloudFormationConnection(accessKey, secretKey)
parameters = {}
parameters["KeyName"] = keyPairName
#stackName = "TestStack"
disableRollback = False 

cfConn.create_stack(stackName, template_url = s3url, parameters= parameters.items(), 
                    disable_rollback = disableRollback, timeout_in_minutes = rollbacktimeout)

#print "Creating the stack"

count = 0
finished = False
while (count < 9 and finished == False):
    stacks = cfConn.describe_stacks(stackName)
    if len(stacks) == 1 :
        stack = stacks[0]
        if stack.stack_status == 'CREATE_COMPLETE':
            finished=True
            #print stack.stack_status
            for output in stack.outputs:
                #print('%s=%s (%s)' % (output.key, output.value, output.description))
                cloudFormationOutput[output.key] = output.value
        elif stack.stack_status.endswith('_FAILED') or \
            stack.stack_status in ('ROLLBACK_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE'):
            #print "Failed to create stack found invalid status" + stack.stack_status
            finished = True
            raise "Failed to create stack", stackName
        else:
            #print "Found In progress status" + stack.stack_status
            #print stack.stack_status
            count = count+1
            #print "sleeping for some time"
            time.sleep(int(waittime)) 
            #print "woke up from sleep"
    else :
        finished = True
        raise "Invalid stack name", stackName

cloudFormationOutputJson = json.dumps(cloudFormationOutput)

print cloudFormationOutputJson
