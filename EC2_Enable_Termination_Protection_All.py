#This specific script doesn't require any arguments.
#The region is specified by the default region in your .AWS\Credentials file.
#Additionally, the default Access/Secret key from that credentials file is also used to execute all APIs
#
#
#
#
#
#Importing necessary packages
import sys
import boto3

#Initializes the EC2 Client & Resource Objects
ec2_client = boto3.client('ec2')
ec2 = boto3.resource('ec2')

#Declaring the InstanceList variable and setting it to and setting it as an array type
instanceList = []

#Makes initial call to AWS API to get list of instances and their details
response = ec2_client.describe_instances()

#Parses that list for the Instance IDs and stores them in InstanceList for later use
for i in response['Reservations']:
	instanceList.append(i['Instances'][0]['InstanceId'])

#While there's a NextToken present in the response reach back out using the AWS API and pull the next page of instances
while 'NextToken'in response:
	response = ec2_client.describe_instances(NextToken=response['NextToken'])

#Parses that list for the Instance IDs and stores them in InstanceList for later use	
	for i in response['Reservations']:
		instanceList.append(i['Instances'][0]['InstanceId'])

#Creates Logging File
file = open("Instance_List_Test", 'w') #WARNING: This will overwrite any previous logging files
file.write("=====Termination Protection Settings Prior to Change=====\n\n\n")
		
for i in instanceList:
	#Pulls the current Termination Protection attribute 
	temp = ec2.Instance(i).describe_attribute(Attribute='disableApiTermination')
	
	#Records that current Termination Protection attribute to the log and console
	file.write('Instance ID ' + i + ' : \n\tCurrent "Termination Protection On" Setting = ' + str(temp['DisableApiTermination']['Value']) + '\n\n\n')
	print ('\nInstance ID ' + i + ' : \n\tCurrent "Termination Protection On" Setting = ' + str(temp['DisableApiTermination']['Value']))
	
	#If that current Termination Protection setting is False go and modify the instance attributes to enable Termination Protection. Records successful API execution to the console.
	if temp['DisableApiTermination']['Value'] == False:
		ec2.Instance(i).modify_attribute(DisableApiTermination={'Value' : True})
		print ('\tTermination Protection was successfully turned on for this instance.\n\n')

#Safely closes the logging file saving all changes
file.close()
