import boto3
import json

client = boto3.client("ec2")



def TerminateEc2(event, context):  

    tagSearchedInstances = []
    allRunnungInstance = []
#All instance other than NatInstance need to terminated
    instancesToTerminate=[] 

    # Terminate all Ec2 resourc

    #get all the ec2 instance in the region and running

    response = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-code',
            'Values': [
                '16',
            ]
        },
    ]
    )


    print('response from call recieved')

    #get all tagged instance

    tagSearchedInstances = getInstanceByTag('NatInstance')

    for instance in response["Reservations"]:
        print(instance["Instances"][0]["InstanceId"])
        allRunnungInstance.append(instance["Instances"][0]["InstanceId"])

    print(' No Of runnig Instance {} '.format(len(allRunnungInstance)))

    if(len(allRunnungInstance)>0):
        # Remove tagged instances 
        print(' No Of Instance with tag {} '.format(len(tagSearchedInstances)))
        instancesToTerminate = [instance for instance in allRunnungInstance if instance not in tagSearchedInstances ]
        
        if(len(instancesToTerminate)>0):
            client.terminate_instances(InstanceIds=instancesToTerminate)
            print('Instances terminated')
        else:
            print('No instance to Terminate')

        # Stop all tagged insstance
        if(len(tagSearchedInstances))>0:
            client.stop_instances(InstanceIds=tagSearchedInstances)
            print ('tagged instances stopped successfully')
        else:
            print('No tagged instance to stop')
   
    else:
        print("No running ec2 to terminate or stop")


# Function to get Nat Instance, change the 'Values' as per desired
# filter to check instance with tagged and state as running
def getInstanceByTag(tageName):

    filters =[
        {'Name': 'tag:Name', 'Values': [tageName]},
        {
            'Name': 'instance-state-code',
            'Values': [
                '16',
            ]
        },
    ]

    listOfTaggedInstance=[]
    response = client.describe_instances(Filters=filters)
    #print(response["Reservations"])
    for x in response["Reservations"]:
        #print(x["Instances"])
        for y in x["Instances"]:
            print('tagged instance found {} '.format(y["InstanceId"]))
            # Add tagged instance in Array
            listOfTaggedInstance.append(y["InstanceId"])
            #client.terminate_instances(InstanceIds=[y["InstanceId"]])
    return listOfTaggedInstance

# comment out below for local testing
# TerminateEc2('test','Test')