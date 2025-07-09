import random

user_wins = 0
computer_wins = 0

while True:
    user_input = input("Type Rock/Paper/Scissors or Q to quit: ").lower()
    if user_input == "q":
        break

    if user_input not in ["rock", "paper", "scissors"]:
        print("Invalid input, please try again.")
        
        continue

    random_number = random.randint(0, 2)
    if random_number == 0:
        computer_input = "rock"
    elif random_number == 1:
        computer_input = "paper"
    else:
        computer_input = "scissors"

    print(f"Computer chose: {computer_input}")

    if user_input == computer_input:
        print("It's a tie!")
    elif (user_input == "rock" and computer_input == "scissors") or \
         (user_input == "paper" and computer_input == "rock") or \
         (user_input == "scissors" and computer_input == "paper"):
        print("You win!")
        user_wins += 1
    else:
        print("You lose!")
        computer_wins += 1
        