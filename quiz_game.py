print("Welcome to the Quiz Game!")
player_name = input("Please enter your name: ")
print(f"Hello, {player_name}! Let's start the quiz.)
Print("You will be asked 5 questions. Try to answer them correctly")
Print("For each correct answer, you will earn 10 points.")
Print("WOULD YOU LIKE TO START? (yes/no)")

PLAYING =input("Do you want to play? ")
if PLAYING != "yes":
    print("Okay, maybe next time!")
    exit()
print("Great! Let's begin!")
answer= input("1. What is CPU stands for? ")
if answer== "central processing unit":
    print("Correct! You earned 10 points.")
    score = 10
else:
    print("Incorrect! The correct answer is 'central processing unit'.")
    score = 0 
    
       
answer= input("2. What is LED stands for? ")
if answer== "light-emitting diode":
    print("Correct! You earned 10 points.")
    score += 10
else:
    print("Incorrect! The correct answer is 'light-emitting diode'.")
    score = 0 
    
    
answer= input("3. What is CD stands for? ")
if answer== "compact disk":
    print("Correct! You earned 10 points.")
    score += 10
else:
    print("Incorrect! The correct answer is 'compact disk'.")
    score = 0 
    
    
answer= input("4. What is ALU stands for? ")
if answer== "arithmetic logic unit":
    print("Correct! You earned 10 points.")
    score += 10
else:
    print("Incorrect! The correct answer is 'arithmeti logic unit'.")
    score = 0    
    
    
answer= input("5. What is RAM stands for? ")
if answer== "random access memory":
    print("Correct! You earned 10 points.")
    score += 10
else:
    print("Incorrect! The correct answer is 'random access memory.")
    score = 0 
total_score= score + score + score + score + score
print(f"{player_name}, your total score is: {total_score} points.")
print("Thank you for playing the Quiz Game!")                        
