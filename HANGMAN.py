import random
def get_word_list():
        # with context manager assures us the
        # file will be closed when leaving the scope
        with open('uniqWords.txt', encoding='utf-8') as f:
            # return the split results, which is all the words in the file.   
            return f.read().split()
def get_word():
    words = get_word_list()
    
    chosenWord = ""

    while len(chosenWord) < 2:
        chosenWord = random.choice(words)

    
    return(chosenWord)
def current_word(chosenWord, letters):
    # Example word : contract 
    # letters is an array with indexes that have been discovered 
    # exemple : letters = [0, 1, 3, 4, 7]
    # So the function will return : co-tr--t
    returnedWord = ""
    for i in range (0, len(chosenWord)):
        if i in letters:
            returnedWord += chosenWord[i]
        else : 
            returnedWord += '-'
    return returnedWord
def hangman_states(penalities): # FOR HARD MODE
    # Returns True if the game is lost, False in the other case
    # Prints nice images of a stickman hanging himself
    match penalities:
        case 0:
            print('''
            ============
            ''')
            return False
        case 1:
            print('''
                    |
                    |
                    |
                    |
                    |
            ============
            ''')
        case 2:
            print('''
                +---+
                    |
                    |
                    |
                    |
                    |
            ============
            ''')
        case 3:
            print('''
                +---+
                |   |
                    |
                    |
                    |
                    |
            ============
            ''')
        case 4:
            print('''
                +---+
                |   |
                o   |
                    |
                    |
                    |
            ============
            ''')
        case 5:
            print('''
                +---+
                |   |
                o   |
                |   |
                    |
                    |
            ============
            ''')
        case 6:
            print('''
                +---+
                |   |
                o   |
               /|   |
                    |
                    |
            ============
            ''')
        case 7:
            print('''
                +---+
                |   |
                o   |
               /|\\  |
                    |
                    |
            ============
            ''')
        case 8:
            print('''
                +---+
                |   |
                o   |
               /|\\  |
                 \\  |
                    |
            ============
            ''')
        case 9:
            print('''
                +---+   
                |   |   RIP
                o   |
               /|\\  |
               / \\  |
                    |
            ============
            ''')
def try_letter(chosenWord, letter):
    # Returns an array with the indexes of the letter you chose in the word
    # Example : chosenWord -> hello | letter -> 'l'
    # returns -> [2, 3]

    # If the letter isn't in the word, returns an empty array -> []
    if letter not in chosenWord : 
        return []
    else :
        letters = []
        for i in range(len(chosenWord)):
            if letter == chosenWord[i]:
                letters.append(i)
        return letters
def try_word(chosenWord, triedWord):
    if chosenWord == triedWord:
        return True
    else :
        return False
def AI_advices(currentWord, oldTries):
    # AI will scan the file containing all the words and look for possibilities
    # For example if the current letter is bi--
    # It will have scanned : 
    # bike
    # bill
    # bind
    # bird
    # bite
    # From the words it found, it will give the most likely character, based on the number of time they appear
    # For this example we have :
    # d -> 2
    # e -> 2
    # l -> 2
    # k -> 1
    # n -> 1
    # r -> 1
    # t -> 1
    # We see that the most likely are d,e and l
    # The AI will then return one of theses
    # BUT if, for example, the user already tried d and e (in oldTries)
    # We have a new curated list of words : 
    # bill
    # For this example, we have only one word, so the ai will return the only word, if we had multiple words, it would do the same as before

    # Getting all words : 
    words = get_word_list()

    # Array to store matching words
    matchingWords = []

    for word in words:
        # Only keep words of the right lenght
        if len(word) == len(currentWord):
            # Now compare each char with currentWord
            tmp = ""
            for c in range(len(currentWord)):
                if currentWord[c] != '-':# Only for letters we found
                    if currentWord[c] == word[c]:
                        tmp = word
                        continue
                    else : # If one letter doesn't match, we don't keep the word
                        tmp = ""
                        break
            if tmp != "": # If we found a word that matches, we keep it
                matchingWords.append(tmp)
    
    # Now we sanitize with oldTries
    if oldTries != []:
        for w in range (len(matchingWords)):
            for old in oldTries:     
                if old in matchingWords[w]:
                    matchingWords[w] = ""

    #print(matchingWords)
    matchingWords = list(filter(None, matchingWords))
            

    # If we only have one word left, the ai returns the full word 
    if len(matchingWords) == 1:
        return matchingWords[0]
    elif len(matchingWords) > 1:
        # If we have mutiple possible words, the AI will return the most likely letter
        # To get the most likely letter, we must count each letter in matchingWords that
        # are not in chosenWord
        min = list(map(chr, range(97, 123)))
        accents = ['é', 'è', 'ê', 'à', 'â', 'î', 'û', 'ù', 'ï', 'ë', 'ü', 'ö', 'ô', 'ã', 'ñ', 'ç']
        min += accents
        letters = []
        max = 0
        for c in min:
            if c not in currentWord:
                for word in matchingWords:
                    tmp = word.count(c)
                    if tmp > max:
                        max = tmp
                        letters = [c]
                    elif tmp == max:
                        letters.append(c)
        
        # Return a random letter among letters
        return random.choice(letters)
def game():
    # First choose the word
    chosenWord = get_word()

    # Ask for the difficulty
    print('''
                            Choose your difficulty :
        Normal -> infinite tries, calculates number of penalities at the end
        Hard -> Classic hangman, if you do too many mistakes, you will die
        
                           (N for normal | H for hard)
        ''')
    diff = input().upper()

    # Check if '--CHEAT' was written after the diff
    if diff[2:] == "--CHEAT":
        cheat = True
    else :
        cheat = False
    
    diff = diff[:1]
    if diff == "N":
        diff = "normal"
    elif diff == "H":
        diff = "hard"
    else :
        print("since you can't spell a simple letter, we put you in hard mode :)")
        diff = "hard"

    # Start the game in normal diff :
    if (diff == 'normal'):
        print('''
                Correct letter -> 1 penality
                Wrong letter -> 3 penalities
                Wrong full word -> 5 penalities
            ''')
        
        end_of_game = False
        letters = []
        oldTries = []
        penality = 0
        while (not end_of_game):
            # Gameplay loop :
            # Print current word and current score and old Tries
            # If cheat is activated -> print the result of the AI
            # Ask for letter or word
            # Tell if right or wrong and updates current score 
            # If game is won put end_of_game to True
            while (True): # Loop for rechoosing in case of error
                print("         Current word : "+current_word(chosenWord, letters))
                print("         Current score : "+str(penality))

                oldy = ""
                for i in oldTries:
                    oldy+=i+" "
                if oldy != "":
                    print("         Old Tries : "+oldy)
                
                print("         Choose a letter or word to guess : ")

                if cheat:
                    aiResponse = AI_advices(current_word(chosenWord, letters),oldTries)
                    if aiResponse != None:
                        if len(aiResponse) == 1:
                            print("         You shoud maybe try",aiResponse)
                        else : 
                            print("         I think you want the word",aiResponse)

                guess = input().lower()

                # Detect if guess if a word or a letter
                if len(guess) > 1 : # word
                    if try_word(chosenWord, guess):
                        print("     CONGRATULATION ! You guessed the word "+chosenWord+" with a score of "+str(penality)+" !")

                        end_of_game = True
                    else : 
                        print("         WRONG WORD ! -> +5 penality points")
                        penality += 5

                    break

                elif len(guess) == 1 : # letter 
                    result = try_letter(chosenWord, guess)
                    if not result : # result == []
                        print("         WRONG LETTER ! -> +3 penality points")
                        oldTries.append(guess)
                        penality += 3
                    else : 
                        for l in result :
                            if l not in letters: # verifies if the letter was not already found
                                letters.append(l)
                            else:
                                break
                        print("         CORRECT LETTER ! -> +1 penality point")
                        penality += 1
                    
                    break
                
                else : # invalid input
                    print("         Invalid input, please retry")
            
            # Check if game is won
            if try_word(chosenWord, current_word(chosenWord, letters)):
                print("     CONGRATULATION ! You guessed the word "+chosenWord+" with a score of "+str(penality)+" !")
                end_of_game = True

    elif (diff == 'hard'):
        print('''
                You have 10 mistakes allowed before Stickman is hanged
                                    Good Luck !
            ''')
        
        end_of_game = False
        letters = []
        oldTries = []
        penality = 0
        while (not end_of_game):
            # Gameplay loop :
            # Print current word and current hangman State and old Tries
            # If cheat is activated -> print the result of the AI
            # Ask for letter or word
            # Tell if right or wrong and updates current score 
            # If game is won put end_of_game to True
            while (True): # Loop for rechoosing in case of error
                print("         Current word : "+current_word(chosenWord, letters))
                hangman_states(penality)

                oldy = ""
                for i in oldTries:
                    oldy+=i+" "
                if oldy != "":
                    print("         Old Tries : "+oldy)

                print("         Choose a letter or word to guess : ")

                if cheat:
                    aiResponse = AI_advices(current_word(chosenWord, letters),oldTries)
                    if aiResponse != None:
                        if len(aiResponse) == 1:
                            print("         You shoud maybe try",aiResponse)
                        else : 
                            print("         I think you want the word",aiResponse)

                guess = input().lower()

                # Detect if guess if a word or a letter
                if len(guess) > 1 : # word
                    if try_word(chosenWord, guess):
                        print("     CONGRATULATION ! You guessed the word "+chosenWord+" with a score of "+str(penality)+" !")

                        end_of_game = True
                    else : 
                        print("         WRONG WORD !")
                        penality += 1

                    break

                elif len(guess) == 1 : # letter 
                    result = try_letter(chosenWord, guess)
                    if not result : # result == []
                        print("         WRONG LETTER !")
                        oldTries.append(guess)
                        penality += 1
                    else : 
                        for l in result :
                            if l not in letters: # verifies if the letter was not already found
                                letters.append(l)
                            else:
                                break
                        print("         CORRECT LETTER !")
                    
                    break
                
                else : # invalid input
                    print("         Invalid input, please retry")
            
            # Check if game is won
            if try_word(chosenWord, current_word(chosenWord, letters)):
                print("     CONGRATULATION ! You guessed the word "+chosenWord+" with a score of "+str(penality)+" !")
                end_of_game = True
            # Check if game is lost
            if penality == 9:
                print("STICKMAN IS DEAD :(, YOU LOSE")
                hangman_states(penality)
                print("The word was : "+chosenWord)
                end_of_game = True
game()