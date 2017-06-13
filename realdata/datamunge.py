from __future__ import division
import numpy as np
import pandas as pd


ds = pd.read_csv('./itunes_meta.csv', error_bad_lines=False)
ds = ds.sort(['date', 'year'], ascending=[0, 0])
ds = ds[pd.notnull(ds['stars'])]
ds = ds[pd.notnull(ds['userid'])]
ds = ds[pd.notnull(ds['appid'])]

x = ds['userid'].value_counts()
ds = ds.loc[ds['userid'].isin(x.index[0:10000])]
x = x.index[0:10000].tolist()
y = ds['appid'].value_counts()
ds = ds.loc[ds['appid'].isin(y.index[0:4000])]
y = y.index[0:4000].tolist()
x = [ int(numbers) for numbers in x ]
y = [ int(numbers) for numbers in y ]

df = ds.as_matrix()

users_arr = ds['userid'].unique()
app_arr = ds['appid'].unique()
print len(users_arr), len(app_arr)
users_arr = list(set(users_arr))
x = list(set(x))
app_arr = list(set(app_arr))
y = list(set(y))
print len(users_arr), len(app_arr)

ratings_lst = []
rated_lst = []
helpful_lst = []
val1 = 0
val2 = 0


for i in range(len(df)):
	try:
		if [int(df[i,2]), int(df[i,0]), 1] in rated_lst:
			continue
		else:
			rated_lst.append([int(df[i,2]), int(df[i,0]), 1])
			if int(df[i,9]) == 0:
				helpful_lst.append([int(df[i,2]), int(df[i,0]), 0])
			else:
				score = int(df[i,8])/int(df[i,9])
				helpful_lst.append([int(df[i,2]), int(df[i,0]), score])
			
			if int(df[i,4]) >= 4:
				if int(df[i,2]) not in x:
					print df[i,2]
				ratings_lst.append([int(df[i,2]), int(df[i,0]), 1])
			else:
				 ratings_lst.append([int(df[i,2]), int(df[i,0]), 0])

	except ValueError:
		val1 += 1
		continue

print "val1:", val1

val1 = 0
mat = np.zeros(shape = (len(users_arr),len(app_arr)))
for rating in ratings_lst:
	try:
		if rating[2] == 0:
			mat[x.index(rating[0]), y.index(rating[1])] = 2
		else:
		 	mat[x.index(rating[0]), y.index(rating[1])] = 1
	except ValueError:
		val2 += 1
		continue
	except IndexError:
		val1 += 1
		continue
print "val1:", val1
print"val2:", val2

mat = mat.astype(int)
np.savetxt('mat.csv', mat, delimiter=',')

thefile = open('toy1.txt', 'w')

for item in ratings_lst:
	thefile.write(str(item[0])+","+str(item[1])+","+str(item[2])+"\n")

thefile = open('rated.txt', 'w')

for item in rated_lst:
	thefile.write(str(item[0])+","+str(item[1])+","+str(item[2])+"\n")

thefile = open('products.txt', 'w')

for item in x:
	thefile.write(str(item)+"\n")

thefile = open('users.txt', 'w')

for item in y:
	thefile.write(str(item)+"\n")
