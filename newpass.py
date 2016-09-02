#!/usr/local/bin/python3
# newpass.py
# Robert Ritter
# rritter@centriq.com


import random, argparse, json, os



# - - - - - Functions - - - - - - - - -

def createStandardPassword():
    '''
    Returns: a string.

    This function creates a string of numberOfItems characters in length,
    randomly selecting each character in turn. The ASCII character group is
    broken into sets and the function selects a character from one of them,
    biased toward the lower case letters (because that's my personal preference
    for passwords).

        Uppercase letters:      65-90
        Lowercase letters:      97-122
        Numerals:               48-57
        Special characters:     32-47, 58-64, 91-96, 123-126
    
    By default passwords do not include special characters. If they are desired,
    the selection process is weighted such that the likelihood that a character
    should be a special character is only one in five. On average, then,
    passwords genereated by this tool with the default length of 10 characters
    should contain two special characters, which seems reasonable to me.
    '''

    if random.random() < 0.5:    # Lead with a lower case letter...
        password = chr(random.randrange(97,123))
    else:                        # ... otherwise lead with an upper case letter.
        password = chr(random.randrange(65,91))


    while len(password) < numberOfItems:
        x = random.randrange(0,100)    # Like rolling a hundred-sided die.

        # If the user wants to include special characters in the result, and if
        # random number x is in the range of 80 to 99, add a random special
        # character. Since there are four ASCII ranges of such characters, we
        # select the range from the first "roll", then we "roll again" to 
        # randomly choose a character from that range.
        if includeSpecialChars and len(password) < (numberOfItems - 1):
            if x >= 80 and x < 85:
                password += chr(random.randrange(32,48))
                x = random.randrange(0,100)        # Get a new x.
            elif x >= 85 and x < 90:
                password += chr(random.randrange(58,65))
                x = random.randrange(0,100)        # Get a new x.
            elif x >= 90 and x < 95:
                password += chr(random.randrange(91,97))
                x = random.randrange(0,100)        # Get a new x.
            elif x >= 95 and x < 100:
                password += chr(random.randrange(123,127))
                x = random.randrange(0,100)        # Get a new x.


        # Add a random letter or digit.
        if x < 47:        # There's a 47% chance you'll get a lower case letter.
            password += chr(random.randrange(97,123))
        elif x < 72:    # There's a 25% chance you'll get a numeral.
            password += chr(random.randrange(48,58))
        else:            # There's a 28% chance you'll get an upper case letter.
            password += chr(random.randrange(65,91))
    
    return password

    # end function createStandardPassword



def createDicePassphrase():
    '''
    Returns: a string.
    Raises: an IOError if the WordList.json file cannot be found,
            a ValueError if the value for numberOfItems is too small,
            a ValueError if the value for numberOfItems is too large.

    This function creates a passphrase of numberOfItems random words selected
    from a file called WordList.json that is stored in the script's directory.
    The word list and the algorithm for selecting words come from the Diceware
    web site. To learn more about the Diceware algorithm, visit
    http://world.std.com/~reinhold/diceware.html.

    This program generates passphrases of at least 20 but no more than 50
    characters to ensure compatibility with miniLock file encryption. If the
    value of numberOfItems is too low or too high the function could get stuck
    in an infinite loop trying to find a passphrase of the correct length. To
    prevent that from happening the function will raise an exception rather
    than try to fulfill the request.
    '''
    
    if numberOfItems < 4:
        raise ValueError('The value for numberOfItems is too low.')
    elif numberOfItems > 11:
        raise ValueError('The value for numberOfItems is too high.')
    
    pythonScriptRoot = os.path.dirname(os.path.realpath(__file__))
    fullFilePath = os.path.join(pythonScriptRoot, 'WordList.json')
    
    with open(fullFilePath, 'r', encoding = 'utf-16') as f: # This will raise an
        dictionary = json.load(f)                           # IOError if the
                                                            # file cannot be
                                                            # opened.
    
    while True:         # Python doesn't have a do-while loop construct, so we
        phrase = ''     # use a while loop and break out when our conditions are
        words = []      # met.
        
        for roll in range(numberOfItems):
            key = ''
            for die in range(5):
                key += str(random.randrange(1,7))
            words.append(dictionary[key])
        phrase = ' '.join(words)
        if len(phrase) >= 20 and len(phrase) <= 50:     # Only leave the loop if
            break                                       # phrase is a valid
                                                        # length.
    return phrase

    # end function createDicePassphrase



# - - - - - Main  - - - - - - - - - - -

# The following code is used to parse the command line and get the arguments
# that have been passed to the program, assign them to variables, and generate
# a useful help message.
params = argparse.ArgumentParser(
    description = 'Generates a password from random characters or a ' +
        'passphrase using the Diceware algorithm.', 
    epilog = '_'
)
params.add_argument(
    '-n', '--number', 
    default = 10, 
    type = int,
    help = 'the number of characters or words to include in the result, ' +
        'by default 10'
)
# Since it makes no sense to use the --special and --dice parameter switches
# together, this mutually exclusive parameter group ensures that only one or the
# other (or neither) is present.
exclusiveParams = params.add_mutually_exclusive_group()
exclusiveParams.add_argument(
    '-s', '--special',
    action = 'store_true',      # False by default, make it True if present.
    help = 'include special characters in the password'
)
exclusiveParams.add_argument(
    '-d', '--dice',
    action = 'store_true',      # False by default, make it True if present.
    help = 'use the Diceware algorithm to generate a passphrase'
)

args = params.parse_args()
numberOfItems        = args.number
includeSpecialChars = args.special
useDice             = args.dice



if useDice:
    try:
        print(createDicePassphrase())
    except ValueError as oops:
        if 'too low' in oops.args[0]:
            errorMessage = 'The value for --number is too low to create ' + \
                'a secure passphrase.'
        else:
            errorMessage = 'The value for --number is too high to create ' + \
                'a miniLock passphrase.'
        print(errorMessage)
        exit(1)
    except IOError:
        errorMessage = 'The --dice switch parameter requires that the ' + \
            'file WordList.json be located in the same directory as the ' + \
            'newpassword.py script file. Please ensure that the file is ' + \
            'present and your user account can read it.'
        print(errorMessage)
        exit(2)
else:
    if numberOfItems < 7:
        errorMessage = 'The value for --number is too low to create a ' + \
            'secure password.'
        print(errorMessage)
        exit(1)
    elif numberOfItems > 128:
        print('The value for --number is unreasonably high.')
        exit(1)
    else:    
        print(createStandardPassword())
