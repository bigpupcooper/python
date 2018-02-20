bicycles = ['trek', 'cannondale', 'redline']
print (bicycles[2])

#print the array, this wiil show brackets and commas
print (bicycles)

#Insert raleigh in to the third element of teh array
bicycles.insert(2, 'raleigh')
print (bicycles)

#Append a new entry on to the list
bicycles.append('chopper')
print (bicycles)

#Print the length of the list
print len(bicycles)

#SORT - permanently
cars = ['bmw', 'audi', 'toyota', 'subaru']
print (cars)
cars.sort()
print (cars)
cars.sort(reverse=True)
print (cars)

#SORT a list temporarily

cars = ['bmw', 'audi', 'toyota', 'subaru']
print (cars)

print("\nHere is the sorted list:")
print(sorted(cars))

print("\nHere is the original list again:")
print(cars)

cars.reverse()
print (cars)

print(cars[-1])


