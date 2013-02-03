# This code consolidates all the spending for one company to both parties
# The output file final_data.csv was used for visualization
# So, we also mapped the sector that the corporation belongs to as well as the percent change in stock prices on Nov 3 and Nov 5 
# Levenshtein distance used to find the parity in org names : Threshold 0.9
# Author : Rashmi Raman mail.rashmiraman@gmail.com

import csv
import Levenshtein

file3reader = csv.reader(open("final_data.csv", "rU"), delimiter=",")
file1reader = csv.reader(open("snp500.csv", "rU"), delimiter=",")
file2reader = csv.reader(open("stockData2012.csv", "rU"), delimiter=",")


header1 = file2reader.next() 

mydict = {rows[1]:"" for rows in file1reader}
sectordict = {rows[1]:rows[0] for rows in file2reader}

file2reader = csv.reader(open("stockData2012.csv", "rU"), delimiter=",")
header1 = file2reader.next() 

percentdict = {rows[1]:rows[4] for rows in file2reader}
#print percentdict

file4writer = csv.writer(open("final_spending_data.csv","wb"),delimiter=",")
file4writer.writerow(["SECTOR","EMPLOYER","DEM","REP","STOCKPERCENTCHANGE"])


for snporg in mydict:
	if snporg in sectordict:
		sector = sectordict[snporg]
	else:
		sector = "Other"
	if snporg in percentdict:
		percentchange = percentdict[snporg]
	else:
		percentchange = "Not available"
	print "Writing data for " + snporg
	sumD = 0
	sumR = 0
	file3reader = csv.reader(open("final_data.csv", "rU"), delimiter=",")
	header1 = file3reader.next()
	for EMPLOYER,CAND_PTY_AFFILIATION,TRANSACTION_AMT in file3reader:
		ratio = Levenshtein.ratio(EMPLOYER,snporg)
		print "Ratio for " + EMPLOYER + " " + snporg + " is : " + str(ratio)
		if ratio > 0.9:
			if CAND_PTY_AFFILIATION == "DEM":
				sumD = sumD + float(TRANSACTION_AMT)
			else:
				sumR = sumR + float(TRANSACTION_AMT)
	file4writer.writerow([sector,snporg,sumD, sumR, percentchange])
	print "Written : " + sector + snporg + str(sumD) + str(sumR) + percentchange
	
print "Written contribution file"