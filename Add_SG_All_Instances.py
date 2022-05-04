#Declaring imported packages
import sys
import boto3

#Declaring necessary variables
ec2_client = boto3.client('ec2')
instanceList = ec2_client.describe_instances()
file = open("Instance_SG_Assignment_For_Recovery.txt", 'w')
instances = []
groups = []
i = 0

#Loops through each instance output from the Describe-Instances call made above
for x in instanceList['Reservations']:
	temp=[]
	
	#Records the instance ID to an array for instance IDs
	instances.append(x['Instances'][0]['InstanceId'])
	file.write('#####' + x['Instances'][0]['InstanceId'] + '#####\n')
	
	#Records that instance's Security Groups to another array with an index matching the corresponding instance in the other array
	for y in x['Instances'][0]['SecurityGroups']:
		temp.append(y['GroupId'])
		file.write(y['GroupId'] + '\n')
	temp.append(sys.argv[1])
	groups.append(temp)
	file.write('\n\n')

#The loop will iterate through each of the instances and apply the corresponding security groups to those instances.
#Should the loop run into an error while executing the Modify-Instance-Attributes API the instance will be skipped and the loop will continue on to the next instance
while i < len(instances):
	try:
		ec2_client.modify_instance_attribute(InstanceId=instances[i], Groups=groups[i])
	except:
		print('An error occurred applying Security Group: '+ sys.argv[1] + ' to Instance: ' + instances[i])
	else:
		print('Security Group: '+ sys.argv[1] + ' added to Instance: ' + instances[i])
		
	i += 1

file.close()