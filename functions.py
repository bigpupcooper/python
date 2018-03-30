def greet_user():
    """Display a simple greeting"""
    print("Hello!")

greet_user()

##############
#Passing information

def greet_user(username):
    """Display a simple greeting"""
    print("Hello " + username.title() + "!")

greet_user('jesse')

######
#Positional Arguements
def descirbe_pet(animal_type, pet_name):
    """Display information about a pet"""
    print("\nI have a " + animal_type + ".")
    print("My " + animal_type + "'s name is " + pet_name.title() + ".")

descirbe_pet('hamster', 'harry')
descirbe_pet('dog','cooper')

#################
#Keyword arguments
def descirbe_pet(animal_type, pet_name):
    """Display information about a pet"""
    print("\nI have a " + animal_type + ".")
    print("My " + animal_type + "'s name is " + pet_name.title() + ".")

descirbe_pet(animal_type= 'hamster', pet_name='George')

##################
#Set a default in a function (remember to have default at the end)

def descirbe_pet(pet_name, animal_type = 'dog'):
    """Display information about a pet"""
    print("\nI have a " + animal_type + ".")
    print("My " + animal_type + "'s name is " + pet_name.title() + ".")

descirbe_pet(pet_name='George')
descirbe_pet(pet_name='harry', animal_type='chicken')

