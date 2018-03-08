import datetime
import numpy as np
import sys
from collections import Counter
import matplotlib.pyplot as plt

now = datetime.datetime.now()
arguments = sys.argv[1:] #position zero is the name of the script
months_of_interest = [1,2,3,4,5,6,7,8,9,10,11,12] #the whole year
date_of_interest = []
date_present = False
show = False

if(len(arguments) != 0):
    months_of_interest = []
    for a in arguments :
        if(a == 'date' or a == 'show') :
            if len(months_of_interest) == 0:
                months_of_interest = [1,2,3,4,5,6,7,8,9,10,11,12]
            break
        months_of_interest.append(int(a))

    for a in arguments:
        if a == 'show':
            show = True
        if a == 'date':
            date_present = True
            continue
        if date_present:
            date_of_interest.append(a)

clths = open("clothes.txt",'r')
outfit = open("outfit.txt",'r')
month = open("months.txt",'r')
clths_lines = clths.readlines()[2:]
outfit_lines = outfit.readlines()[1:]
months_lines = month.readlines()
month.close()
clths.close()
outfit.close()



sc = open("supercategory.txt")
supercategory = sc.readlines()[2:]
sc.close()

sc_map = dict({})
for s in supercategory :
    line = s.split('/')
    for i in line[1].replace(')','').replace('(','').replace('\n','').split(','):
        sc_map[i] = line[0]

super_super_cat = dict({})
super_super_cat['pants'] = 'pants'
super_super_cat['short'] = 'pants'
super_super_cat['dress'] = 'dress/skirt'
super_super_cat['skirt'] = 'dress/skirt'


clothes_map = dict({})
for l in clths_lines:
    line = l.split('/')
    clothes_map[line[0]] = line[1:]

months_map = dict({})
for m in months_lines:
    m = m.replace('\n','')
    line = m.split('/')
    months_map[int(line[0])]=line[1]

#counter of shop occurence repetition of clothes allowed
shop_count = Counter()
color_count = Counter()
clothes_date_count = Counter()
clothes_count = Counter()
cat_count = Counter()
pants_vs_dress_count = Counter()
outfit_count = []

nb_clothes = 0

if not date_present :
    date_of_interest = outfit_lines[-1].split('/')[0].split('.')
    #date_of_interest = list(map(int,date_of_interest))

clothes_date = []

for o in outfit_lines:
    line = o.split('/')
    date = line[0]
    month = date.split('.')[1]
    mask = np.isin(int(month), months_of_interest)
    clothes = line[1].replace('(','').replace(')','').split(',')
    if(month < date_of_interest[1] or (month == date_of_interest[1] and date.split('.')[0] <= date_of_interest[0])):
        outfit_count.append(clothes)
    notes = line[2:]
    for c in clothes :
        if(date.split('.') == date_of_interest):
            clothes_date.append(c) #collect the names
        if(mask):
            #to count only occurence of a clothe when worn 2 or more times in the day with something different
            clothes_date_count.update([(date,c)])
            nb_clothes += 1
            supercat = sc_map.get(clothes_map.get(c)[0])
            super_super_category = super_super_cat.get(supercat)
            if(super_super_category != None):
                pants_vs_dress_count.update([super_super_category])
            cat_count.update([supercat])
            shop_count.update([clothes_map.get(c)[-2]])
            color_count.update([clothes_map.get(c)[1].replace('(','').replace(')','').split(',')[0]])


clo_date,occ = zip(*clothes_date_count.most_common())
for c_d in clo_date:
    clothes_count.update([c_d[1]])

c_c_m_c = clothes_count.most_common()
clothes_list, clothes_repartition = zip(*c_c_m_c)

clothes_repartition = np.array(clothes_repartition)
number_equal = len(clothes_repartition[clothes_repartition == clothes_repartition[0]])

year_count = Counter()
age = datetime.timedelta()
nb_clothes_no_repetition= 0

for c in clothes_list :
    nb_clothes_no_repetition += 1
    months_year = clothes_map.get(c)[-1].replace('\n', '').split('.')
    year_count.update([months_year[1]])
    age += abs(datetime.date(int(months_year[1]), int(months_year[0]), 1) - datetime.date(now.year, now.month, now.day))

age_date = datetime.timedelta()
nb_clothes_date= 0
nb_occ_date = 0

for c in np.unique(np.array(clothes_date)) :
    nb_clothes_date += 1
    months_year = clothes_map.get(c)[-1].replace('\n', '').split('.')
    age_date += abs(datetime.date(int(months_year[1]), int(months_year[0]), 1) - datetime.date(now.year, now.month, now.day))



mean_age_date = (age_date/nb_clothes_date).days
nb_years_date = np.floor(mean_age_date/365)
nb_months_date = np.floor((mean_age_date%365)/30)

print("the outfit worn the {day} {month} {year} is {y} years and {m} months old".format(day = date_of_interest[0],month = months_map.get(int(date_of_interest[1])),year = date_of_interest[2],y = nb_years_date, m = nb_months_date))




mean_age = (age/nb_clothes_no_repetition).days
nb_years = np.floor(mean_age/365)
nb_months = np.floor((mean_age%365)/30)

s =''
if(nb_years > 1):
    s ='s'

month_sentence = ""
start = 'the month of '
for m in months_of_interest[:-2]:
    month_sentence+= str(months_map.get(m))
    month_sentence+= ', '
if(len(months_of_interest)>1):
    start = 'the months of '
    month_sentence+= str(months_map.get(months_of_interest[-2]))
if(month_sentence != ""):
    month_sentence+=' and '
month_sentence+= str(months_map.get(months_of_interest[-1]))

if(len(months_of_interest)== 12):
    month_sentence = 'the year 2018'
else :
    month_sentence = start + month_sentence

count_outfit = 0
for o in outfit_count:
    if o == clothes_date :
        count_outfit+=1
if count_outfit == 0:
    for o in outfit_count:
        mask = np.isin(o,clothes_date)
        if(np.all(mask)):
            count_outfit+=1

if(count_outfit == 1):
    print("the outfit is novel")
else :
    print("the outfit has already been worn during this year")

print("the wardrobe actually worn during {mo} contains {n} items and is {y} year{plur} and {m} months old".format(mo = month_sentence,n=nb_clothes_no_repetition,y = nb_years, plur = s, m = nb_months))




most_worn = ''
for m in clothes_list[0:number_equal]:
    most_worn += ' '+m

if(number_equal == 1):
    most_worn = ' is ' + most_worn
else:
    most_worn = ' are '+most_worn
print("the most worn item during "+month_sentence+most_worn+" with "+str(clothes_repartition[0])+" occurences")

#plot part
if show:
    other_threshold = 0.037

    shop_majority = shop_count.most_common()
    _,n = zip(*shop_majority)
    n_copy = np.array(n)-nb_clothes*other_threshold
    to_keep = sum(1 for i in n_copy if i > 0)
    shop_majority = shop_count.most_common(to_keep)
    _,n = zip(*shop_majority)
    if nb_clothes-np.sum(n) > 0 :
        shop_majority.append(('others',nb_clothes-np.sum(n)))
    shop_list,occ = zip(*shop_majority)

    fig1, ax1 = plt.subplots()
    ax1.pie(occ,labels=shop_list,labeldistance = 1.1, autopct='%1.0f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title("most worn brand during "+month_sentence)


    fig2,ax2 = plt.subplots()
    _,nb_color = zip(*color_count.most_common())
    total_color = sum(nb_color)
    nb_color_copy = np.array(nb_color)-total_color*other_threshold
    to_keep = sum(1 for i in nb_color_copy if i > 0)
    color_majority =color_count.most_common(to_keep)
    _,nb_color = zip(*color_majority)
    if total_color-np.sum(nb_color) > 0 :
        color_majority.append(('others',total_color-np.sum(nb_color)))
    colors,nb_color = zip(*color_majority)

    ax2.pie(nb_color,labels=colors,labeldistance = 1.1, autopct='%1.0f%%',
            shadow=True, startangle=90)
    ax2.axis('equal')
    plt.title('most worn color during '+month_sentence)



    fig3,ax3 = plt.subplots()
    years,nb_year = zip(*year_count.most_common())
    ax3.pie(nb_year,labels=years,labeldistance = 1.1, autopct='%1.0f%%',
            shadow=True, startangle=90)
    ax3.axis('equal')
    plt.title('Year of origin of worn clothes during '+month_sentence)

    fig4,ax4 = plt.subplots()
    cat,nb_occ = zip(*cat_count.most_common())
    ax4.pie(nb_occ,labels=cat,labeldistance = 1.1, autopct='%1.0f%%',
            shadow=True, startangle=90)
    ax4.axis('equal')
    plt.title('category of worn clothes during '+month_sentence)

    fig5,ax5 = plt.subplots()
    cat,nb_occ = zip(*pants_vs_dress_count.most_common())
    ax5.pie(nb_occ,labels=cat,labeldistance = 1.1, autopct='%1.0f%%',
            shadow=True, startangle=90)
    ax5.axis('equal')
    plt.title('pants versus dress during '+month_sentence)

    plt.show()