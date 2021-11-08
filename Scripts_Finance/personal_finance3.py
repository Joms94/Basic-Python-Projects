def calculate_interest(assets, interest, time_years):
    gross = round(assets*(interest**time_years))
    profit = round(gross-assets)
    print("Your $" + str(assets) + " will grow to $" + str(gross) + ".")
    print("You can expect a profit of " + str(profit) + " dollarydoos over " + str(time_years) + " years.")
    if profit < 100:
        print("That's pretty bad. Sorry champ.")
    if profit > 10000:
        print("Look at moneybags over here!")
    else:
        print("Not bad!")


def float_input(request_message):
    # :input:  <string: The message you give to the user to request an input.>
    # :output: <float: The inputted value.>
    while True:
        try:
            user_float = float(input(request_message))
            return user_float
        except ValueError:
            print("Use a valid number!")
            continue


def user_input():
    # Compound interest calculation based on user input.
    while True:
        assets = float_input("How much cash you got mate?")
        interest = float_input("What kind of interest rate you getting? Use either a decimal or integer.")/100+1
        if interest < 1:
            interest + 1
        time_years = float_input("How long you gonna let that cash sit? (in years)")
        calculate_interest(assets, interest, time_years)
        proceed = input("Do another calculation? (Y/N)")
        if proceed == 'Y':
            continue
        if proceed == 'N':
            print("Thanks for stopping by!")
            break
        else:
            print("Uhh... I don't know what you said, so I'm just going to... go.")
            break


user_input()
