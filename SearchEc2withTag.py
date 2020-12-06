import boto3


client = boto3.client('ec2')

filters =[
    {'Name': 'tag:Name', 'Values': ['Boto3machine']}
]

response = client.describe_instances(Filters=filters)
#print(response["Reservations"])
for x in response["Reservations"]:
    #print(x["Instances"])
    for y in x["Instances"]:
        print(y["PublicDnsName"])
