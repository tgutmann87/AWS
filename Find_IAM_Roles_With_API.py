import csv
import sys
import json
import boto3

iam_client = boto3.client('iam')

with open('IAMPolicyDetails.csv', 'w', newline='') as file:
    file = csv.writer(file)
    file.writerow(['Policy Name', 'Policy ARN', 'Default Version', 'TypeError', 'Statement'])
     
    response = iam_client.list_policies()
    print("Getting IAM Policies...")
     
    for i in response['Policies']:
        policyName = i['PolicyName']
        policyARN = i['Arn']
        policyDefaultVersion = i['DefaultVersionId']
#        print(policyName + " , " + policyARN + " , " + policyDefaultVersion)

        policyResponse = iam_client.get_policy_version(PolicyArn=policyARN, VersionId=policyDefaultVersion)
        
        try:
            for statement in policyResponse['PolicyVersion']['Document']['Statement']:
                try:
                    if statement['Action'].count('ssm:StartSession') > 0:
                        file.writerow([policyName, policyARN, policyDefaultVersion, '', statement])
                except KeyError:
                    try:
                        if statement['NotAction'].count('ssm:StartSession') > 0:
                            file.writerow([policyName, policyARN, policyDefaultVersion, '', statement, ''])
                    except:
                        print("KeyError: No Action or NotAction Key")
        except TypeError:
            file.writerow([policyName, policyARN, policyDefaultVersion, 'X', policyResponse['PolicyVersion']['Document']])
                    
    while response['IsTruncated']:
        response = iam_client.list_policies(Marker=response['Marker'])
        print("Getting More IAM Policies...")
        
        for i in response['Policies']:
            policyName = i['PolicyName']
            policyARN = i['Arn']
            policyDefaultVersion = i['DefaultVersionId']
#            print(policyName + " , " + policyARN + " , " + policyDefaultVersion)

            policyResponse = iam_client.get_policy_version(PolicyArn=policyARN, VersionId=policyDefaultVersion)

            try:
                for statement in policyResponse['PolicyVersion']['Document']['Statement']:
                    try:
                        if statement['Action'].count('ssm:StartSession') > 0:
                            file.writerow([policyName, policyARN, policyDefaultVersion, '', statement])
                    except KeyError:
                        try:
                            if statement['NotAction'].count('ssm:StartSession') > 0:
                                file.writerow([policyName, policyARN, policyDefaultVersion, '', statement])
                        except:
                            print("KeyError: No Action or NotAction Key")
            except TypeError:
                file.writerow([policyName, policyARN, policyDefaultVersion, 'X', policyResponse['PolicyVersion']['Document']])