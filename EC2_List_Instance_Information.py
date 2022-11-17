#This specific script doesn't require any arguments.
#The region is specified by the default region in your .AWS\Credentials file.
#Additionally, the default Access/Secret key from that credentials file is also used to execute all APIs
#
#
#
#
#
#Importing necessary packages
import csv
import sys
import boto3

#Initializes the EC2 Client Object
ec2_client = boto3.client('ec2')

#Declaring the InstanceList variable and setting it to and setting it as an array type
instanceList = []

#Creating the CSV file which will store the instance data
with open("InstanceData.csv", 'w', newline='') as file:
	file = csv.writer(file)
	file.writerow(['InstanceName', 'InstanceID', 'Region' , 'Platform', 'Instance Type', 'Private IP', 'Public IP', 'BillingCode', 'Services'])

	#Makes initial call to AWS API to get list of instances and their details
	response = ec2_client.describe_instances()

	#Parses that list for the Instance IDs and stores them in InstanceList for later use
	#Row order ['InstanceName', 'InstanceID', 'Region' , 'Platform', 'Instance Type', 'Private IP', 'Public IP', 'BillingCode']
	for i in response['Reservations']:
		instanceName = ''
		billingCode = ''
		service = ''
		
		for j in i['Instances'][0]['Tags']:
			if j['Key'] == "Name":
				instanceName = j['Value']
			elif j['Key'] == "BillingCode":
				billingCode = j['Value']
			elif j['Key'] == "Service":
				service = j['Value']
			
		file.writerow([instanceName, i['Instances'][0]['InstanceId'], i['Instances'][0]['Placement']['AvailabilityZone'], i['Instances'][0].get('Platform'), i['Instances'][0]['InstanceType'], i['Instances'][0]['PrivateIpAddress'], i['Instances'][0].get('PublicIpAddress'), billingCode, service])
				
	#While there's a NextToken present in the response reach back out using the AWS API and pull the next page of instances
	while 'NextToken'in response:
		print("Next Token")
		response = ec2_client.describe_instances(NextToken=response['NextToken'])
		
		#Parses that list for the Instance IDs and stores them in InstanceList for later use
		#Row order ['InstanceName', 'InstanceID', 'Region' , 'Platform', 'Instance Type', 'Private IP', 'Public IP', 'BillingCode']
		for i in response['Reservations']:
			instanceName = ''
			billingCode = ''
			service = ''
			
			for j in i['Instances'][0]['Tags']:
				if j['Key'] == "Name":
					instanceName = j['Value']
				elif j['Key'] == "BillingCode":
					billingCode = j['Value']
		
			file.writerow([instanceName, i['Instances'][0]['InstanceId'], i['Instances'][0]['Placement']['AvailabilityZone'], i['Instances'][0].get('Platform'), i['Instances'][0]['InstanceType'], i['Instances'][0]['PrivateIpAddress'], i['Instances'][0].get('PublicIpAddress'), billingCode, service])
