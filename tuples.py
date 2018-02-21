# Tuple, this is a list that can't be changed
# Use () rather than []

dimensions = (200, 50)
print(dimensions[0])
print (dimensions[1])

#dimensions[0] = 250 #This will error since you are trying to change a value in the tuple

print ("Original dimensions:")
for dimension in dimensions:
    print(dimension)

dimensions = (400, 100)
print("\nModified dimensions:")
for dimension in dimensions:
    print(dimension)

foods = ('meat','spuds', 'chicken', 'veg', 'soup')
print (foods)

for food in foods:
    print (food)

#foods[0] = 'chicken'






