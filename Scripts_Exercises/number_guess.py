def target():
    import random
    hidden_num = random.randint(1,20)
    print("GOAL IS CURRENTLY " + str(hidden_num))
    return str(hidden_num)


def game(number):
    guess = input("I'm thinking of a number between 1 and 20...\n")
    goal = number
    while True:
        if guess == goal:
            print("Correct!")
            break
        if guess < goal:
            guess = input("Larger!\n")
            continue
        if guess > goal:
            guess = input("Smaller!\n")
            continue
        else:
            break


game(target())