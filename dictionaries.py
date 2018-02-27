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

###########Looping in dictionary#
#method items() returns a list of key-value pairs

user_0 = {
    'username':'efermi',
    'first': 'enrico',
    'last': 'fermi',
    }

for key, value in user_0.items():
    print("\nKey: " + key)
    print("Value: " + value)

#applying the looping thru all key-value pairs

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
    }
for name, language in favorite_languages.items():
print(name.title() + "'s favorite language is " +
    language.title() + ".")

#Looping through all the KEYS in a dict
#use the keys() method
favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
    }
friends = ['phil', 'sarah']
for name in favorite_languages.keys():
    print(name.title())
    if name in friends:
        print("Hi" + name.title() +
            ", I see your fav language is " +
            favorite_languages[name].title())

#Looping thru all VALUES in a dict

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
    }
print("The following languages, have been mentioned:")
for language in favorite_languages.values():
    print(language.title())

# The above will loop all and show duplicates, so use set()

favorite_languages = {
    'jen': 'python',
    'sarah': 'c',
    'edward': 'ruby',
    'phil': 'python'
    }
print("The following languages, have been mentioned:")
for language in set(favorite_languages.values()):
    print(language.title())


