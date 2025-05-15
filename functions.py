import boto3

def createVPCResources(event):
    vpc_cidr = event['vpc_cidr']
    subnets = event['subnets']
    vpc_name = event['vpc_name']
    lambda_name = "lambda-function-name"   #Include your lambda function name here
    try:
        # Create VPC
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
        # End - Create VPC

        # Create Subnets
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
                
                #Store data in DynamoDB
                try:
                    dynamodb_client = boto3.client('dynamodb')
                    data_response = dynamodb_client.put_item(TableName='dynamo-db-table-name', 
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
        # End Create Subnets
        return create_vpc_response
    except Exception as e:
        print(f"An error occurred while creating VPC: {e}")
    
def getVPCInfo(event):
    # Function to get VPC and Subnets Info from DynamoDB
    dynamodb = boto3.resource('dynamodb')
    try:   
        table = dynamodb.Table('dynamo-db-table-name')
        getDynamoDBResponse = table.scan()
        return getDynamoDBResponse
    except Exception as e:
        print(f"An error occurred: {e}")
