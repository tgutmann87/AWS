import csv
import sys
import boto3

iam_client = boto3.client('iam')

with open('IAMPolicyDetails.csv', 'w', newline='') as file:
    file = csv.writer(file)
    file.writerow(['Policy Name', 'Policy ARN', 'Default Version'])
     
    response = iam_client.list_policies()
    print("Getting IAM Policies...")
     
    for i in response['Policies']:
        policyName = i['PolicyName']
        policyARN = i['Arn']
        policyDefaultVersion = i['DefaultVersionId']
        print(policyName + " , " + policyARN + " , " + policyDefaultVersion)

        policyResponse = iam_client.get_policy_version(PolicyArn=policyARN, VersionId=policyDefaultVersion)

        if(str(policyResponse['PolicyVersion']['Document']).find("ssm:StartSession") >= 0):
            file.writerow([policyName, policyARN, policyDefaultVersion])
                    
    while response['IsTruncated']:
        response = iam_client.list_policies(Marker=response['Marker'])
        print("Getting More IAM Policies...")
        
        for i in response['Policies']:
            policyName = i['PolicyName']
            policyARN = i['Arn']
            policyDefaultVersion = i['DefaultVersionId']
            print(policyName + " , " + policyARN + " , " + policyDefaultVersion)

            policyResponse = iam_client.get_policy_version(PolicyArn=policyARN, VersionId=policyDefaultVersion)

            if(str(policyResponse['PolicyVersion']['Document']).find("ssm:StartSession") >= 0):
                file.writerow([policyName, policyARN, policyDefaultVersion])