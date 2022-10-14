import csv
import boto3

#Declaring 'primitive' vairables
i = 0
flag = True
nextToken = ''

#Declaring class variables
workspacesClient = boto3.client('workspaces')
file = open('Workspaces.csv', 'w', newline='')
csvWriter = csv.writer(file)

#Writing table header
csvWriter.writerow(['Workspace ID', 'Username', 'Computer Name', 'Subnet ID'])

#Grabbing first batch of workspaces only 25 can be pulled with each request
workspaces = workspacesClient.describe_workspaces()

#Checks if NextToken is available
#NextToken is present if there's additional workspaces past the limit of 25. Think of it as turning the page to see more.
try:
	if workspaces['NextToken']:
		nextToken = workspaces['NextToken']
#If it isn't present the variable is set to empty.
except KeyError:
	nextToken = ''
	
#As long as the flag is True the loop will continue. The flag is controlled by whether if a 'NextToken' is included in the response to the DescribeWorkspaces call.	
while flag:
	for workspace in workspaces["Workspaces"]:
		#Debugging statement
		print(str(i) + ' : ' + workspace['WorkspaceId'])
		
		#Writes the workspace and some of it's information to the CSV file
		csvWriter.writerow([workspace['WorkspaceId'], workspace['UserName'], workspace['ComputerName'], workspace['SubnetId']])
		i+= 1
	
	if nextToken:
		#Debugging statement
		#print('Token Present')
		
		#Calls the next batch of workspaces if NextToken was present
		workspaces = workspacesClient.describe_workspaces(NextToken=nextToken)
		
		#Checks if NextToken is available
		try:
			if workspaces['NextToken']:
				nextToken = workspaces['NextToken']
		#If it isn't present the variable is set to empty.
		except KeyError:
			nextToken = ''
	#If NextToken wasn't present the flag is set to false causing the loop to stop
	else:
		flag = False

#Closing the CSV file for good housekeeping		
file.close()

#Debugging statement
print('Total Workspace: ' + str(i))
