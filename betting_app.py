import random

MAX_LINES = 3
MAX_BET= 50000000
MIN_BET = 500

ROWS = 3
COLS = 3

symbols = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 6
}

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)
            
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    
    return columns

def check_winnings(columns, lines, bet, symbols):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += bet * symbols[symbol]
            winning_lines.append(line + 1)
    return winnings, winning_lines

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
        print()



def deposit():
    while True:
        amount = input("Enter the amount to deposit: shs")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("Please enter a positive amount.")    
                
        else:
            print("Invalid input. Please enter a valid amount.")
    return amount

def get_number_of_lines():
    while True:
        lines = input("Enter the lines to bet on (1-"+str(MAX_LINES)+")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
            
                break
            else:
                print(f"Please enter a number of lines between 1 and {MAX_LINES}.")    
                
        else:
            print(f"Please enter a number of lines between 1 and {MAX_LINES}.")
    return lines

def get_bet():
    while True:
        bet = input("Enter the bet amount: ")
        if bet.isdigit():
            bet = int(bet)
            if MIN_BET <= bet <= MAX_BET:
                break
            else:
                print(f"Please enter a bet between shs{MIN_BET} and shs{MAX_BET}.")
        else:
            print(f"Please enter a bet between shs{MIN_BET} and shs{MAX_BET}.")
    return bet    

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            print(f"You do not have enough balance to place this bet. Your balance is shs{balance}.")
        else:
            break

    print(f"You have deposited shs{balance} and bet on {lines} lines.")
    print(f"You have placed a bet of shs{bet} on {lines} lines.")
    total_bet = bet * lines

    slots = get_slot_machine_spin(ROWS, COLS, symbols)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbols)
    print(f"You have won shs{winnings}.")
    print(f"You won on lines: {', '.join(map(str, winning_lines))}.")
    return winnings - total_bet


def main():
    balance = deposit()
    while True:
        print(f"Your current balance is shs{balance}.")
        user_input = input("Press enter to spin or type 'exit' to quit: ").lower()
        if user_input == "exit":
            print(f"Thank you for playing! Your final balance is shs{balance}.")
            break
        if balance <= 0:
            print("You have run out of money! Please deposit more to continue playing.")
            balance += deposit()
            continue

        winnings = spin(balance)
        balance += winnings
        print(f"Your new balance is shs{balance}.")



if __name__ == "__main__":
    main()
