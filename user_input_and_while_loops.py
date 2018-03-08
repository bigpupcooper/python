message = raw_input("Tell me something to repeat back:")
print(message)

#use the += to build a prompt over muliple lines
prompt = "If you tell us who you are, we can personalize the messages you see"
prompt += "\nWhat is you first name? "
name = raw_input(prompt)
print(name)

####input treated as a string, so convert it by using int()
age = raw_input("How old are you")
age = int(age)


#################
##While loops###

    current_number = 1
    while current_number <= 5:
        print(current_number)
        current_number = current_number + 1

###keep running until user asks to quit
prompt = "\nTell me something"
prompt += "\nEnter 'quit' to end"

message = ""
while message != 'quit':
    message = raw_input(prompt)
    print(message)

####Using a FLAG
prompt = "\nTell me something"
prompt += "\nEnter 'quit' to end"

active = True
while active:
    message = raw_input(prompt)
    if message == 'quit' :
        active = False
    else:
        print(message)

#####Using BREAK to exit a loop
prompt = "\nTell me something"
prompt += "\nEnter 'quit' to end"

while True:
    city = raw_input(prompt)
    if city == 'quit':
        break
    else:
        print("id love to go to " + city.title())

