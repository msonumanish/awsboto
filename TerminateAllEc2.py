import boto3

# Terminate all Ec2 resource

client = boto3.client("ec2")

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

allRunnungInstance = []

for instance in response["Reservations"]:
    print(instance["Instances"][0]["InstanceId"])
    allRunnungInstance.append(instance["Instances"][0]["InstanceId"])
    #State
    print(instance["Instances"][0]["State"])

print('Terminate {} '.format(allRunnungInstance))

# Terminate all running instance
if(len(allRunnungInstance)>0):
    client.terminate_instances(InstanceIds=allRunnungInstance)
else:
    print("No running ec2 to terminate")


