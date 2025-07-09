import random

top_of_range = input("Enter a number: ")
if top_of_range.isdigit():
    top_of_range = int(top_of_range)
    if top_of_range <= 0:
        print("Please enter a number greater than 0 next time.")
        exit()
else:
    print("Please enter a valid number next time.")
    exit()
random_number = random.randint(0, top_of_range)
while True:
    user_guess = input("Make a guess: ")
    if user_guess.isdigit():
        user_guess = int(user_guess)
    else:
        print("Please enter a valid number next time.")
        continue

    if user_guess == random_number:
        print("You got it right!")
        break
    elif user_guess < random_number:
        print("Too low!")
    else:
        print("Too high!")
print(f"The random number was {random_number}.")
print("Thanks for playing!")