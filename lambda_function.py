import json
import boto3,functions

def lambda_handler(event, context):
    #TO DO implement
    print("Inside Lambda")
    print(event)
    if 'tagsflag' in event:
        body = event['body-json']["op"]
    else:
        body=(event['params']['querystring']['op'])
    
    if body == "createVPCResources":
        createVPCResponse = functions.createVPCResources(event['body-json'])
        print("------------------Get Create VPC Output-----------------")
        print(createVPCResponse)
    elif body == 'getVPCInfo':
        getVPCInfoResponse = functions.getVPCInfo(body)
        print("------------------Get Subnets Data from DynamoDB-----------------")
        print(getVPCInfoResponse)
        HTML_CONTENT_START = "<html><head><title>VPC Details</title><style>table{font-family:arial,sans-serif;border:1px solid #dddddd;width:100%;} h2{font-family:arial,sans-serif;width:100%;text-align:center;} h3{font-family:arial,sans-serif;width:100%;padding-left:25%;} td,th{border:1px solid #dddddd;text-align:left; padding:8px;} tr:nth-child(even){background-color:#dddddd;}</style></head><body>"
        HTML_CONTENT_END = "</body></html>"
        print(type(getVPCInfoResponse))
        html_content = str()
        if len(getVPCInfoResponse['Items']) == 0:
            print("The dictionary is empty")
            return "<h2>No VPC Resources Created!</h2><h3>Please first run the lambda function to create VPC Resources.</h3>"
        else:
            print("The dictionary is not empty")
            s1 = json.dumps(getVPCInfoResponse['Items'])
            x = json.loads(s1)
            HTML_CONTENT_START += "<table><tr><th>VPC ID</th><th>Subnet ID</th><th>Subnet CIDR</th><th>Subnet AZ</th><th>Subnet ARN</th></tr>"
            for item in x:
                print(item['vpcID'])
                table_row = "<tr style='background: #FFA500'><td>"
                html_content += table_row + item['vpcID'] + "</td><td>" + item['subnetID'] + "</td><td>" + item['subnetCIDR'] + "</td><td>" + item['subnetAZ'] + "</td><td>" + item['subnetARN'] + "</td></tr>"
            html_content_final = HTML_CONTENT_START + html_content + "</table>" + HTML_CONTENT_END
            return html_content_final
    else:
        print("Invalid Operation")
        return "<h2>Invalid query string parameter value!</h2><h3>Allowed value is 'getVPCInfo'.</h3>"

    #return {
    #    'statusCode': 200,
    #    'body': json.dumps('Hello from Lambda!')
    #}

