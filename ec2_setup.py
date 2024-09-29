import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

ami_id = "ami-0a0e5d9c7acc336f1"
instances = ec2.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='Yuhsiang_Huang',
    TagSpecifications=[{
        'ResourceType': 'instance',
        'Tags': [{'Key': 'Name', 'Value': 'web-instance'}]
    }]
)


