cars = ['audi', 'bmw', 'subaru', 'toyota']
for car in cars:
    if car == 'bmw':
        print(car.upper())
    else:
        print(car.title())

#next bit
car = 'Audi'
if car.lower() == 'audi':
    print('True')
else:
    print('False')


# IN
requested_toppings = ['mushrooms', 'onions', 'pineapple']
if 'mushrooms' in requested_toppings:
    print ('yes')

#Not in a list
banned_users = ['andrew', 'carolina', 'david']
user = 'marie'
if user not in banned_users:
    print(user.title() + ', you can post a response if you wish.')

####Boolean

car = 'subaru'
print("Is car == 'subaru'? I predict True.")
print(car == 'subaru')
print("\nIs car == 'audi'? I predict False.")
print(car == 'audi')
#


#Voting
age = 19
if age >= 18:
    print('You are old enough to vote')


#####
age = 17
if age >=18:
    print("You are old enough to vote")
    print ("Have you registered to vote yet?")
else:
    print("Sorry, you are too young to vote")
    print("Please register to vote as soon as you reach 18")

#####
age = 21
if age < 4:
    print("You can go free")
elif age <18:
    print("Your admission is 5 dolla")
else:
    print("You pay 10 dolla")

##########more concise version of above

age = 12
if age <4:
    price = 0
elif age <18:
    price = 5
else:
    price = 10
print("You pay "  + str(price) + " !")


#####
requested_toppings = ['mushrooms', 'extra cheese']
if 'mushrooms' in requested_toppings:
    print("Adding mushrooms")
if 'pepperoni' in requested_toppings:
    print("Adding pepperoni")
if 'extra cheese' in requested_toppings:
    print("adding extra cheese")
print("\nFinished making your pizza!")

#######







