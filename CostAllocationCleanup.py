import sys
import csv
import datetime

#Declaring known variables in advance.
billingCodes = []
totalCosts = []
i = 1

#Opens the file writing it to a list.
file = open(sys.argv[1], "r")
bill = file.readlines()
file.close()

#Removes the comment on the first line in addition to the last 10 lines due to that being bill totals.
bill.pop(0)
length = len(bill)
while i <= 10:
	bill.pop(length - i)
	i += 1

#The modified file is then open by the CSV module within Python.
#Empty 'cells' are marked with |Empty|
CAReader = csv.DictReader(bill, restval="|Empty|")

#The reader goes through the CSV file line by line.
for line in CAReader:
	
	#If the Total Cost field of the line item isn't equal to zero the script will check to see if the Billing Code has already been recorded.
	if float(line["TotalCost"]) != 0:
		
		#If that Billing Code has already been found the existing Total Cost for that line item is added to the overall total cost for that Billing Code.
		if billingCodes.count(line["user:BillingCode"]):
			temp = billingCodes.index(line["user:BillingCode"])
			totalCosts[temp] = totalCosts[temp] + float(line["TotalCost"])
		
		#If the Billing Code hasn't already been recorded then it and the Total Cost will be added to the necessary lists.	
		else:
			billingCodes.append(line.get("user:BillingCode"))
			totalCosts.append(float(line.get("TotalCost")))

#Replaces the empty/non-existant Billing Code entry to readable text for the CSV file.
temp = billingCodes.index("")
billingCodes[temp] = "No tag/value specified"

#A new CSV file is created for the data that we want.
file = open("Cost_Allocation_Total_Cost_By Department.csv", "w", newline="")
CAWriter = csv.writer(file)
CAWriter.writerow(["Department Code", "Total Cost"])

#Writes the rows from the necessary lists.
temp = len(billingCodes) - 1
while temp >= 0:
	CAWriter.writerow([billingCodes[temp], totalCosts[temp]])
	temp -= 1
	
#Debugging printouts.
print(billingCodes)			
print(totalCosts)
temp = 0
for x in totalCosts:
	temp += x	
print(temp)