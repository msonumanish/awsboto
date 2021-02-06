print ("Starting")
import boto3


client = boto3.client('ec2')

filters =[
    {'Name': 'tag:Name', 'Values': ['NatInstance']}
]

response = client.describe_instances()#Filters=filters)
print(response["Reservations"])
for x in response["Reservations"]:
    #print(x["Instances"])
    for y in x["Instances"]:
        print(y["InstanceId"])
        print("Shuting down the ec2")
        #client.terminate_instances(InstanceIds=[y["InstanceId"]])
