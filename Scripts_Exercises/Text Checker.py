#Text Analysis
# You have been recruited by your friend, a linguistics enthusiast, to create a utility tool
# that can perform analysis on a given piece of text. Complete the class 'analysedText'
# with the following methods -

# Constructor - Takes argument 'text',makes it lower case and removes all punctuation.
# Assume only the following punctuation is used - period (.), exclamation mark (!), comma (,) and question mark (?).
# Store the argument in "fmtText"
# freqAll - returns a dictionary of all unique words in the text along with the number of their occurences.
# freqOf - returns the frequency of the word passed in argument.


class analysedText(object):

    def __init__(self, text):
        # Remove punctuation.
        self.text = text
        formattedText = text.replace('.', '').replace('!', '').replace('?', '').replace(',', '')

        # Make text lowercase.
        formattedText = formattedText.lower()

        self.fmtText = formattedText

    def freqAll(self):
        # Turns text object into a list.
        splitText = self.fmtText.split(" ", -1)

        # Counts number of occurrences of each word in the specified string and adds them to a second list.
        occurrencesList = []
        for i in range(len(splitText)):
            occurrencesList.append(splitText.count(splitText[i]))

        # Interleafs both lists, then converts them into a dictionary.
        self.completeDictionary = dict(zip(splitText, occurrencesList))
        return self.completeDictionary

    def freqOf(self, word):
        self.word = word
        targetWord = self.completeDictionary.get(word)
        return targetWord

# This is what the course coordinator came up with.
# class analysedText(object):
#
#     def __init__(self, text):
#         remove punctuation
        # formattedText = text.replace('.', '').replace('!', '').replace('?', '').replace(',', '')
        #
        # make text lowercase
        # formattedText = formattedText.lower()
        #
        # self.fmtText = formattedText
    #
    # def freqAll(self):
    #     split text into words
        # wordList = self.fmtText.split(' ')
        #
        # Create dictionary
        # freqMap = {}
        # for word in set(wordList):  # use set to remove duplicates in list
        #     freqMap[word] = wordList.count(word)
        #
        # return freqMap
    #
    # def freqOf(self, word):
    #     get frequency map
        # freqDict = self.freqAll()
        #
        # if word in freqDict:
        #     return freqDict[word]
        # else:
        #     return 0
#

# The following is for debugging purposes.
text1 = analysedText("Am I a little teapot? I am short, but am I stout? Help. HELP!")
allWordFrequency = text1.freqAll()
print("freqAll result: " + str(allWordFrequency))
singleWordFrequency = text1.freqOf("am")
print("freqOf result: " + str(singleWordFrequency))