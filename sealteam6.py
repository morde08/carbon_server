'''
Age (18-70), income (20000-100000), cost of living (), # of dependents (0-5), spending/month (1000-10000), credit score (400-800), delinquency (0 or 1 (15% chance)), marital status (0 or 1 (30% chance))

seperate CSV for credit card (1-4)

4 credit cards:
Venture - 1
VentureOne - 2
Quicksilver - 3
QuickSilverOne - 4
'''

import random
import csv

with open('x.csv', 'w') as csvfile:
	spamwriter = csv.writer(csvfile)
	for i in range(100000):
		spamwriter.writerow((random.randint(18, 70), random.randint(20000, 100000), random.randint(1000, 3000), random.randint(0, 5), random.randint(1000, 10000), random.uniform(400, 800), random.choice([0, 1, 1, 1, 1, 1]), random.choice([0, 1, 1])))

with open('y.csv', 'w') as csvfile:
	spamwriter = csv.writer(csvfile)
	for i in range(100000):
		spamwriter.writerow([random.randint(1,4)])