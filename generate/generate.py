import numpy as np
import random

def generate(no_of_users, no_of_products, no_of_bad_products, no_of_spammers,no_of_famous_products):
	mat = np.zeros(shape = (no_of_users,no_of_products))
	prev_prodlst = []
	current_prodlst = []
	for x in range(no_of_users):
		current_prodlst = []
		for z in range((25/(x+1))+2):
			if z > 0:
				y = random.randint(0,no_of_products-1)
				mat[x,y] = 1
				current_prodlst.append(y)

			else:
				if len(prev_prodlst) > 0:
					y = random.randint(0,len(prev_prodlst)-1)
					mat[x,prev_prodlst[y]] = 1
					current_prodlst.append(prev_prodlst[y])
					
				else:
					y = random.randint(0,no_of_products-1)
					mat[x,y] = 1
					current_prodlst.append(y)

		prev_prodlst = current_prodlst


			
	prev_usrlst = []
	current_usrlst = []
			
	for y in range(no_of_products):
		current_usrlst = []
		for z in range((15/(y+1))+1):
			if z > 0:
				x = random.randint(0,no_of_users-1)
				mat[x,y] = 1
				current_usrlst.append(x)
			else:
				if len(prev_usrlst) > 0:
					x = random.randint(0,len(prev_usrlst)-1)
					mat[prev_usrlst[x],y] = 1
					current_usrlst.append(prev_usrlst[x])
					#print x,y,mat[prev_usrlst[x],y]
				else:
					x = random.randint(0,no_of_users-1)
					mat[x,y] = 1
					current_usrlst.append(x)

		prev_usrlst = current_usrlst

	bad_prods = []
	bad_users = []

	for i in range(no_of_spammers):
		uid = random.randint(no_of_spammers,no_of_users-1)
		if uid in bad_users:
			i = i - 1
		else:
			bad_users.append(uid)
	print bad_users


	for i in range(no_of_bad_products):
		pid = random.randint(no_of_famous_products,no_of_products-1)
		if pid in bad_prods:
			i = i - 1
		else:
			bad_prods.append(pid)

	print bad_prods

	for x in bad_users:
		for y in bad_prods:
			z = random.randint(0,3)
			if z == 0:
				mat[x,y] = 1

	famous_prods = range(no_of_famous_products)
	for x in range(no_of_users):
		for y in range(no_of_products):
			if mat[x,y] == 1:
				if x not in bad_users and y in bad_prods:
					mat[x,y] = 2

				
	mat = mat.astype(int)

	for x in range(no_of_users):
		for y in range(no_of_products):
			mat[x,y] = int(mat[x,y])

	adjlst = []
	for x in range(no_of_users):
		for y in range(no_of_products):
			if mat[x,y] == 1:
				adjlst.append([x,y,mat[x,y]])
			elif mat[x,y] == 2:
				adjlst.append([x,y,0])
	

	ratedlst = []
	for x in range(no_of_users):
		for y in range(no_of_products):
			if mat[x,y] == 1 or mat[x,y] == 2:
				ratedlst.append([x,y,1])
			
	

	
	
	np.savetxt('mat.csv', mat, delimiter=',')

	thefile = open('toy1.txt', 'w')

	for item in adjlst:
		thefile.write(str(item[0])+","+str(item[1])+","+str(item[2])+"\n")

	thefile = open('rated.txt', 'w')

	for item in ratedlst:
		thefile.write(str(item[0])+","+str(item[1])+","+str(item[2])+"\n")

	usrlst = range(no_of_users)
	productlst = range(no_of_products)

	thefile = open('products.txt', 'w')

	for item in productlst:
		thefile.write(str(item)+"\n")

	thefile = open('users.txt', 'w')

	for item in usrlst:
		thefile.write(str(item)+"\n")

	thefile = open('badusers.txt', 'w')

	for item in bad_users:
		thefile.write(str(item)+"\n")

	thefile = open('badprods.txt', 'w')

	for item in bad_prods:
		thefile.write(str(item)+"\n")


generate(196, 78, 6, 4,7)