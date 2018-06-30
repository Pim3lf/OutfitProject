# OutfitProject
Add statistics to the database of my clothes
works with two external txt files :

clothes.txt:

contains all the references of clothes in the wardrobe in this following format :
	
	label/category/colors+/materials+/shop or brand/acquisition date
	
the actual data begins at line 2
	
outfit.txt:

contains all the references of outfit with the clothes contained in clothes.txt in this following format :
	
	date/clothes+/cuteness(1 to 5)/elegance(1 to 5)/will wear again (-1,0,1)
	
the actual data begins at line 1
