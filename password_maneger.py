pwd=input("Enter your password: ")

def view_password():
    with open("passwords.txt", "r") as file:
        passwords = file.readlines()
        if not passwords:
            print("No passwords stored.")
        else:
            print("Stored passwords:")
            for line in passwords:
                print(line.strip())



def add_password():
    name= input("Enter the name of the account: ")
    pwd= input("Enter the password: ")
    with open("passwords.txt", "a") as file:
        file.write(f"{name}: {pwd}\n")
while True:
    choice = input("Would you like to view or add a password? (view/add/exit): ").lower()
    if choice == "view":
        view_password()
    elif choice == "add":
        add_password()
    elif choice == "exit":
        print("Exiting the password manager.")
        break
    else:
        print("Invalid choice, please try again.")