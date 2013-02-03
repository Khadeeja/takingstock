# This code picks up the contributions which were cleaned up in Stata and consolidates against SNP500 companies
#Levenshtein distance used to find the parity in org names : Threshold 0.9
#Author : Rashmi Raman mail.rashmiraman@gmail.com

import csv
import Levenshtein

file1reader = csv.reader(open("snp500.csv", "rU"), delimiter=",")
file2reader = csv.reader(open("collapsed_contibution_data_2012only_presonly.csv","rU"), delimiter=",")
file3reader = csv.reader(open("new_parent_company_data.csv","rU"), delimiter=",")

header1 = file1reader.next() 
header2 = file2reader.next() 
header3 = file3reader.next() 


mydict = {rows[1]:"" for rows in file1reader}
#print mydict

file4writer = csv.writer(open("final_data.csv","wb"),delimiter=",")

file4writer.writerow(header2)


for EMPLOYER,CAND_PTY_AFFILIATION,TRANSACTION_AMT in file2reader:
	if EMPLOYER in mydict:
		print "Exact match " + EMPLOYER
		file4writer.writerow([EMPLOYER, CAND_PTY_AFFILIATION, TRANSACTION_AMT])
	else:
		for snporg in mydict:
			ratio = Levenshtein.ratio(EMPLOYER,snporg)
			if ratio > 0.9:
				print "Fuzzy parent company match " + EMPLOYER + " with " + snporg
				file4writer.writerow([snporg, CAND_PTY_AFFILIATION, TRANSACTION_AMT])
				break
			else:
				for child_company_name, parent_company_name in file3reader:
					ratio = Levenshtein.ratio(child_company_name, EMPLOYER)
					if ratio > 0.9:
						print "Fuzzy subsidiary company match " + EMPLOYER + " with " + child_company_name
						file4writer.writerow([parent_company_name + " + " + child_company_name,CAND_PTY_AFFILIATION,TRANSACTION_AMT])
						break
print "Done"






