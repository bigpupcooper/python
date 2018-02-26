alien_0 = {'color': 'green', 'points': 5}
print(alien_0['color'])
print(alien_0['points'])


##access values in a dictionary
print (alien_0['color'])

##add more values into a dictionary for a key

alien_0['x_position'] = 0
alien_0['y_position'] = 25
print(alien_0)

###########################
#Empty Dictionary
alien_0 = {}
alien_0['color'] = 'green'
alien_0['points'] = 5
print(alien_0)

### change a value
alien_0 = {'color': 'green'}
print("The alien is " + alien_0['color'] + ".")
alien_0['color'] = 'yellow'
print("The alien is now " + alien_0['color'] + ".")

#####Remove key value pairs
alien_0 = {'color': 'green', 'points': 5}
print(alien_0)
del alien_0['points']
print(alien_0)

#and add back in
alien_0['points'] = 5
print(alien_0)

#format for dictionary longer lines
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
    }
print ("Sarah's favorite language is " +
       favorite_languages['sarah'].title() +
       ".")

