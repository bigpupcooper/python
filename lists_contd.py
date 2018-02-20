#Slicing a list
players = ['charles', 'martina', 'michael', 'florence', 'eli']
print(players[0:3])
print(players[1:4])
print(players[:4])
print(players[2:])
print(players[-3:]) #prints that last three


print("Here are the first three players on my team:")
for player in players[:3]:
    print(player.title())


###Copying a list, the use of [:] means everything
my_foods = ['pizza', 'falafel', 'carrot cake']
friend_foods = my_foods[:] # this is copying the entire list
print("My favorite foods are:")
print(my_foods)
print("\nMy friend's favorite foods are:")
print(friend_foods)

##
