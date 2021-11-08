from Dictionary import *
from keyboard_disable import *


def typing_intro():
    dictionary = None
    while True:
        difficulty = input("Choose your difficulty level!\n* Baby Mode (WAH!)\n* Devil's Delight (666)\n")
        if difficulty == "WAH!":
            print("Let's go!")
            dictionary = BabyDictionary()
            break
        if difficulty == "666":
            print("Let's go!")
            dictionary = DevilsDictionary()
            break
        else:
            print("Pardon?")
            continue

    gameplay(dictionary)


def gameplay(dictionary):
    import time
    duration = 0
    allowed_time = 10
    start_time = time.time()
    wrong_answers = 0
    right_answers = 0
    input("Press any key to begin.")
    while duration <= allowed_time:
        end_time = time.time()
        duration = int(end_time - start_time)
        target_word = str(dictionary.generate_word())
        print(target_word)
        guessed_word = input()
        if target_word == guessed_word:
            right_answers += 1
            print("Correct!")
            continue
        if target_word != guessed_word:
            wrong_answers += 1
            print("Wrong!")
            continue
    if duration >= allowed_time:
        KeyboardDisable()
        timeout(wrong_answers,right_answers, duration)


def timeout(wrong_answers, right_answers, duration):
    import time
    print("\nTime's up!")
    print(str(right_answers) + " correct answers.")
    time.sleep(1.5)
    print(str(wrong_answers) + " mistakes.")
    time.sleep(1.5)
    wpm = str(int(right_answers + wrong_answers * (duration / 60)))
    accuracy_positive = int((right_answers - wrong_answers)/right_answers * 100)
    accuracy_negative = int((right_answers / wrong_answers) * 100)
    if accuracy_positive > 0:
        print("You typed at roughly " + wpm + " words per minute...\n...with " + str(accuracy_positive) + str("% accuracy."))
    else:
        print("You typed at roughly " + wpm + " words per minute...\n...with " + str(accuracy_negative) + str("% accuracy."))
    time.sleep(1.5)
    print("\nPress any key to play again.\n")
    typing_intro()


typing_intro()
