
import datetime
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

now = datetime.datetime.now()

f = open("clothes.txt","r")

lines = f.readlines()

f.close()

sc = open("supercategory.txt")
supercategory = sc.readlines()[2:]
sc.close()

sc_map = dict({})
for s in supercategory :
    line = s.split('/')
    for i in line[1].replace(')','').replace('(','').replace('\n','').split(','):
        sc_map[i] = line[0]


sup_col = open("supercolor.txt")
supercolor = sup_col.readlines()[2:]
sup_col.close()

sup_col_map = dict({})
for s in supercolor :
    line = s.split('/')
    for i in line[1].replace(')', '').replace('(', '').replace('\n', '').split(','):
        sup_col_map[i] = line[0]


years= Counter()
years_in_shop = Counter()
shops= Counter()
colors = Counter()
s_colors = Counter()
main_color= Counter()
s_main_color = Counter()
materials = Counter()
category = Counter()

shop_year= []
shop_super_category = []
year_super_category = []
year_super_color = []
shop_super_color = []
super_category_color = []

lines = lines[2:]
nb_clothes = len(lines)
total_age = datetime.timedelta()

for l in lines :
    split = l.split('/')
    date = split[-1]
    shops.update([split[-2]])
    category.update([split[1]])

    colors_list = split[2].replace('(','').replace(')','').split(',')
    colors.update(colors_list)
    main_color.update([colors_list[0]])
    s_main_color.update([sup_col_map.get(colors_list[0])])
    for c in colors_list :
        s_colors.update([sup_col_map.get(c)])

    materials_list = split[3].replace('(', '').replace(')', '').split(',')
    materials.update(materials_list)

    months_year = date.split('.')
    years.update([int(months_year[1])])

    age = abs(datetime.date(int(months_year[1]),int(months_year[0]),1)-datetime.date(now.year,now.month,now.day))
    total_age += age
    super_c = sc_map.get(split[1])
    year_super_category.append((int(months_year[1]), super_c))
    year_super_color.append((int(months_year[1]),sup_col_map.get(colors_list[0])))
    super_category_color.append((super_c,sup_col_map.get(colors_list[0])))
    if(split[-2]== 'H&M' or split[-2]=='C&A' or split[-2]=='Zalando' or split[-2] == 'Primark'):
        shop_super_color.append((split[-2],sup_col_map.get(colors_list[0])))
        years_in_shop.update([int(months_year[1])])
        shop_super_category.append((split[-2],super_c))
        shop_year.append((split[-2],int(months_year[1])))


mean_age = (total_age/nb_clothes).days
nb_years = np.floor(mean_age/365)
nb_months = np.floor((mean_age%365)/30)

print("la garderobe contient {n} items et a en moyenne {y} ans et {m} mois".format(n=nb_clothes,y = int(nb_years),m= int(nb_months)))


plt.figure()
plt.ylabel('number of clothes')
plt.title('shop versus year')
width = 0.35


c = Counter()
c.update(shop_year)
c = c.most_common()

item,nb = zip(*c)

item_shop,item_year =zip(*item)
item_shop = np.array(item_shop)
item_year = np.array(item_year)

present_year,_ = zip(*years_in_shop.most_common())
present_year = np.sort(np.array(present_year))
plt.xticks(present_year)

shop_of_interest = ['H&M','C&A','Primark','Zalando']
shop_lists = [np.zeros(present_year.shape)]

for s in shop_of_interest :
    shop_list = []
    for y in  present_year:

        intersec = np.intersect1d(np.where(item_shop == s),np.where(item_year == y))
        if(len(intersec) == 0):
            shop_list.append(0)
        else :
            shop_list.append(nb[intersec[0]])

    shop_lists.append(shop_list)


max_y = np.max(np.sum(shop_lists,axis = 0))
plt.yticks(np.arange(0, max_y+1, 1))

for i in np.arange(1,len(shop_of_interest)+1):
    bot = np.sum(shop_lists[0:i],axis = 0)
    plt.bar(present_year,shop_lists[i], bottom = bot)

plt.legend(shop_of_interest)


plt.figure()
plt.ylabel('number of clothes')
plt.title('category versus year')

e = Counter()
e.update(year_super_category)
e = e.most_common()

item,nb = zip(*e)

item_year,item_cat =zip(*item)
item_cat = np.array(item_cat)
item_year = np.array(item_year)

present_year,_ = zip(*years.most_common())
present_year = np.sort(np.array(present_year))
plt.xticks(present_year)

cat_of_interest = np.unique(item_cat)

cat_lists = [np.zeros(present_year.shape)]

for c in cat_of_interest :
    cat_list = []
    for y in  present_year:
        intersec = np.intersect1d(np.where(item_cat == c),np.where(item_year == y))
        if(len(intersec) == 0):
            cat_list.append(0)
        else :
            cat_list.append(nb[intersec[0]])

    cat_lists.append(cat_list)


max_y = np.max(np.sum(cat_lists,axis = 0))

plt.yticks(np.arange(0, max_y+1, 1))

for i in np.arange(1,len(cat_of_interest)+1):
    bot = np.sum(cat_lists[0:i],axis = 0)
    plt.bar(present_year,cat_lists[i], bottom = bot)

plt.legend(cat_of_interest)


plt.figure()
plt.ylabel('number of clothes')
plt.title('shop versus category')

c = Counter()
c.update(shop_super_category)
c = c.most_common()

item,nb = zip(*c)

item_shop,item_cat =zip(*item)
item_shop = np.array(item_shop)
item_cat = np.array(item_cat)

categories = np.unique(item_cat)
ind = np.arange(len(categories))
plt.xticks(ind,categories)

shop_of_interest = ['H&M','C&A','Primark','Zalando']
shop_lists = [np.zeros(categories.shape)]

for s in shop_of_interest :
    shop_list = []
    for c in  categories:

        intersec = np.intersect1d(np.where(item_shop == s),np.where(item_cat == c))
        if(len(intersec) == 0):
            shop_list.append(0)
        else :
            shop_list.append(nb[intersec[0]])

    shop_lists.append(shop_list)


max_y = np.max(np.sum(shop_lists,axis = 0))
plt.yticks(np.arange(0, max_y+1, 1))

for i in np.arange(1,len(shop_of_interest)+1):
    bot = np.sum(shop_lists[0:i],axis = 0)
    plt.bar(ind,shop_lists[i], bottom = bot)

plt.legend(shop_of_interest)

plt.figure()
plt.ylabel('number of clothes')
plt.title('shop versus color')

c = Counter()
c.update(shop_super_color)
c = c.most_common()

item,nb = zip(*c)

item_shop,item_col =zip(*item)
item_shop = np.array(item_shop)
item_col = np.array(item_col)

colories = np.unique(item_col)
ind = np.arange(len(colories))
plt.xticks(ind,colories)

shop_of_interest = ['H&M','C&A','Primark','Zalando']
shop_lists = [np.zeros(colories.shape)]

for s in shop_of_interest :
    shop_list = []
    for c in  colories:

        intersec = np.intersect1d(np.where(item_shop == s),np.where(item_col == c))
        if(len(intersec) == 0):
            shop_list.append(0)
        else :
            shop_list.append(nb[intersec[0]])

    shop_lists.append(shop_list)


max_y = np.max(np.sum(shop_lists,axis = 0))
plt.yticks(np.arange(0, max_y+1, 1))

for i in np.arange(1,len(shop_of_interest)+1):
    bot = np.sum(shop_lists[0:i],axis = 0)
    plt.bar(ind,shop_lists[i], bottom = bot)

plt.legend(shop_of_interest)

plt.figure()
plt.ylabel('number of clothes')
plt.title('category versus color')

e = Counter()
e.update(super_category_color)
e = e.most_common()

item,nb = zip(*e)

item_cat,item_col =zip(*item)
item_cat = np.array(item_cat)
item_col = np.array(item_col)

present_cat = np.unique(item_cat)
ind = np.arange(len(present_cat))
plt.xticks(ind,present_cat)

col_of_interest = np.unique(item_col)

col_lists = [np.zeros(present_cat.shape)]

for c in col_of_interest :
    col_list = []
    for y in present_cat:
        intersec = np.intersect1d(np.where(item_col == c),np.where(item_cat == y))
        if(len(intersec) == 0):
            col_list.append(0)
        else :
            col_list.append(nb[intersec[0]])

    col_lists.append(col_list)


max_y = np.max(np.sum(col_lists,axis = 0))

plt.yticks(np.arange(0, max_y+1, 1))

for i in np.arange(1,len(col_of_interest)+1):
    bot = np.sum(col_lists[0:i],axis = 0)
    plt.bar(present_cat,col_lists[i], bottom = bot)

plt.legend(col_of_interest)

plt.figure()
plt.ylabel('number of clothes')
plt.title('color versus year')

e = Counter()
e.update(year_super_color)
e = e.most_common()

item,nb = zip(*e)

item_year,item_col =zip(*item)
item_col = np.array(item_col)
item_year = np.array(item_year)

present_year,_ = zip(*years.most_common())
present_year = np.sort(np.array(present_year))
plt.xticks(present_year)

col_of_interest = np.unique(item_col)

col_lists = [np.zeros(present_year.shape)]

for c in col_of_interest :
    col_list = []
    for y in  present_year:
        intersec = np.intersect1d(np.where(item_col == c),np.where(item_year == y))
        if(len(intersec) == 0):
            col_list.append(0)
        else :
            col_list.append(nb[intersec[0]])

    col_lists.append(col_list)


max_y = np.max(np.sum(col_lists,axis = 0))

plt.yticks(np.arange(0, max_y+1, 1))

for i in np.arange(1,len(col_of_interest)+1):
    bot = np.sum(col_lists[0:i],axis = 0)
    plt.bar(present_year,col_lists[i], bottom = bot)

plt.legend(col_of_interest)

plt.show()

