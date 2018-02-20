magicians = ['alice', 'david', 'carolina']
for magician in magicians:
    print (magician.title() + ", that was a great trick!")


magicians = ['alice', 'david', 'carolina']
for magician in magicians:
    print (magician.title() + ", that was a great trick!")
    print("I can't wait to see your next trick, " + magician.title() + ".\n")
print ("Thank you very much, that was a great magic show!")


#Using Range

for value in range(1, 5):
    print(value)

###########
numbers = list(range(1, 6))
print(numbers)

###even
even_numbers = list(range(2, 11, 2))
print(even_numbers)

###squares
squares = []
for value in range(1,11):
    square = value**2
    squares.append(square)
print(squares)
