import boto3

def createVPCResources(event):
    print("Inside createVPCResources function")
    vpc_cidr = event['vpc_cidr']
    subnets = event['subnets']
    lambda_name = "SRE-B2B-VPC-POC"
    vpc_name = "VPC-POC"
    try:
        client = boto3.client('ec2',region_name='ap-south-2')
        create_vpc_response = client.create_vpc(
            CidrBlock=vpc_cidr,
            TagSpecifications=[{
                'ResourceType': 'vpc',
                'Tags': [
                    {
                        'Key': 'CreatedByLambda',
                        'Value': lambda_name
                    },
                    {
                        'Key': 'Name',
                        'Value': vpc_name
                    },
                ]
            },],
            DryRun=False,
            AmazonProvidedIpv6CidrBlock=False
        )
        print("VPC Creation Response:")
        print(create_vpc_response)
        
        # Wait for VPC to become available
        vpc_id = create_vpc_response['Vpc']['VpcId']
        vpc_client = boto3.resource('ec2').Vpc(vpc_id)
        vpc_client.wait_until_available()
        print(f"VPC '{vpc_name}' is now available")
        vpc_cidr = event['vpc_cidr']
        subnets = event['subnets']
        
        for subnet in subnets:
            print(f"Creating Subnet for: {subnet}")
            try:
                create_subnet_response = client.create_subnet(
                    TagSpecifications=[
                        {
                            'ResourceType': 'subnet',
                            'Tags': [
                                {
                                    'Key': 'CreatedByLambda',
                                    'Value': lambda_name
                                },
                                {
                                    'Key': 'Name',
                                    'Value': subnet['subnet_name']
                                },
                            ]
                        },
                    ],
                    AvailabilityZone=subnet['subnet_az'],
                    CidrBlock=subnet['subnet_cidr'],
                    VpcId=vpc_id,
                )
                print(f"Subnet created: {create_subnet_response}")
                #Store Subnet Data in DynamoDB
                try:
                    dynamodb_client = boto3.client('dynamodb')
                    data_response = dynamodb_client.put_item(TableName='SRE-B2B-VPC-POC-DB', 
                    Item={
                        'subnetID': {'S':str(create_subnet_response['Subnet']['SubnetId'])},
                        'subnetCIDR': {'S':str(create_subnet_response['Subnet']['CidrBlock'])},
                        'subnetAZ': {'S':str(create_subnet_response['Subnet']['AvailabilityZone'])},
                        'subnetARN': {'S':str(create_subnet_response['Subnet']['SubnetArn'])},
                        'vpcID': {'S':str(create_subnet_response['Subnet']['VpcId'])}
                    })
                except Exception as e:
                    print(f"An error occurred while storing subnetdata in DynamoDB: {e}")
            except Exception as e:
                print(f"An error occurred while creating Subnets: {e}")
        print("Subnets Data:")
        print(create_subnet_response)
        print(create_vpc_response)
        return create_vpc_response
    except Exception as e:
        print(f"An error occurred while creating VPC: {e}")
    
def getVPCInfo(event):
    print("Inside getVPCInfo function")
    dynamodb = boto3.resource('dynamodb')
    try:   
        table = dynamodb.Table('SRE-B2B-VPC-POC-DB')
        getDynamoDBResponse = table.scan()
        all_data = getDynamoDBResponse['Items']
        print("All items from Dynamodb:"+str(all_data))
        print(getDynamoDBResponse)
        return getDynamoDBResponse
    except Exception as e:
        print(f"An error occurred: {e}")
