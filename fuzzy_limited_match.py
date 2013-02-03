# This code picks up the master list of parent -> child companies from the API and matches it against SNP 500
#Levenshtein distance used to find the parity in org names : Threshold 0.9
#Author : Rashmi Raman mail.rashmiraman@gmail.com

import csv
import Levenshtein


file1reader = csv.reader(open("snp500.csv", "rU"), delimiter=",")
file3reader = csv.reader(open("new_parent_company_data.csv","rU"), delimiter=",")

header1 = file1reader.next() 
header3 = file3reader.next() 


mydict = {rows[1]:"" for rows in file1reader}
#print mydict

file4writer = csv.writer(open("limited_mapping_data.csv","wb"),delimiter=",")
file4writer.writerow(header3)

for child_company_name, parent_company_name in file3reader:
	if parent_company_name in mydict:
		file4writer.writerow([parent_company_name,child_company_name])
	else:
		for snporg in mydict:
			ratio = Levenshtein.ratio(parent_company_name,snporg)
			if ratio > 0.9:
				print "Fuzzy match " + parent_company_name + " with " + snporg
				file4writer.writerow([parent_company_name,child_company_name])
				break
print "Written limited file"