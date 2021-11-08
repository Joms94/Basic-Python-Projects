def elmer_fuddify(string1, string2):
    # Opens a text file and saves a new version of that file with every 'r' replaced with a 'w'.
    string1 = open(string1, "rt")
    string2 = open(string2, "wt")
    for line in string1:
        string2.write(line.replace("r", "w"))
    string1.close()
    string2.close()
    print("Fuddified!")


def user_input():
    while True:
        try:
            target_file = input("Please specify a path to the file you wish to fuddify.")
            new_file = input("Where will the new fuddi-file be created?")
            elmer_fuddify(target_file, new_file)
            extra_fudd = input("More fudd? (Y/N)")
            if extra_fudd == "Y":
                continue
            if extra_fudd == "N":
                print("Ok. Catch you on the fudd side.")
                break
            else:
                print("What the fudd did you just say? I'm out.")
                break
        except ValueError:
            print("Hmm... I don't recognise that file.")
            continue
        except FileNotFoundError:
            print("Invalid path. Try again!")
            continue
        except OSError:
            print("Something totally un-fudd happened. Try again.")
            continue


user_input()
