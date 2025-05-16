import json
import boto3,functions

def lambda_handler(event, context):
    # TO DO implement
    if 'tagsflag' in event:
        body = event['body-json']["op"]
    else:
        body=(event['params']['querystring']['op'])
    
    if body == "createVPCResources":
        # To create VPC, Subnets and store the result in DynamoDB table
        print(event)
        createVPCResponse = functions.createVPCResources(event['body-json'])
        return createVPCResponse
    elif body == 'getVPCInfo':
        # To fetch resource creation data from DynamoDB table and show in tabular format
        print(event)
        getVPCInfoResponse = functions.getVPCInfo(body)
        print("------------------Subnets Data from DynamoDB-----------------")
        print(getVPCInfoResponse)
        HTML_CONTENT_START = "<html><head><title>VPC Details</title><style>table{font-family:arial,sans-serif;border:1px solid #dddddd;width:100%;} h2{font-family:arial,sans-serif;width:100%;text-align:center;} h3{font-family:arial,sans-serif;width:100%;padding-left:25%;} td,th{border:1px solid #dddddd;text-align:left; padding:8px;} tr:nth-child(even){background-color:#dddddd;}</style></head><body>"
        HTML_CONTENT_END = "</body></html>"
        html_content = str()
        if len(getVPCInfoResponse['Items']) == 0:
            return "<h2>No VPC resources created yet!</h2><h3>Please first invoke the VPC creation API to create VPC Resources.</h3>"
        else:
            HTML_CONTENT_START += "<table><tr><th>VPC ID</th><th>Subnet ID</th><th>Subnet CIDR</th><th>Subnet AZ</th><th>Subnet ARN</th></tr>"
            items = getVPCInfoResponse['Items']
            for item in items:
                table_row = "<tr style='background: #FFA500'><td>"
                html_content += table_row + item['vpcID'] + "</td><td>" + item['subnetID'] + "</td><td>" + item['subnetCIDR'] + "</td><td>" + item['subnetAZ'] + "</td><td>" + item['subnetARN'] + "</td></tr>"
            html_content_final = HTML_CONTENT_START + html_content + "</table>" + HTML_CONTENT_END
            return html_content_final
    else:
        return "<h2>Invalid querystring passed!</h2>"
