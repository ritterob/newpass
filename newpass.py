#!/usr/bin/env python3
# newpass.py
# Robert Ritter
# rritter@centriq.com

import random
import os
import json
import argparse
import textwrap


class NumberTooLowError(ValueError):
    pass


class NumberTooHighError(ValueError):
    pass


class NotIntegerError(ValueError):
    pass


class FileNotFoundError(IOError):
    pass


def create_password(num=10, special=False):
    """
    Create a password from randomly selected chrarcters.

    Keyword arguments:
    num -- number of characters in password (default 10)
    special -- whether to include special characters (default False)

    Raises:
    NotIntegerError -- if num is not an integer
    NumberTooLowError -- if num < 7
    NumberTooHighError -- if num > 64

    Returns: a string

    This function creates a string of num characters in length,
    randomly selecting each character in turn.  The ASCII character
    group is broken into sets and the function selects a character
    from one of them, biased toward the lower case letters (because
    that's my personal preference for passwords).  The sets are and
    their ASCII codes are:

    Uppercase letters:  65-90
    Lowercase letters:  97-122
    Numerals:           48-57
    Special characters: 32-47, 58-64, 91-96, 123-126

    By default passwords do not include special characters.  If they are
    desired, the selection process is weighted such that the likelihood
    that a character should be a special character is only one in five.
    On average, then, passwords genereated by this tool with the
    default length of 10 characters should contain two special
    characters, which seems reasonable to me.
    """
    if not isinstance(num, int):
        raise NotIntegerError('num must be a valid number')
    if num < 7:
        raise NumberTooLowError('num must be 7 or greater')
    if num > 64:
        raise NumberTooHighError('num must be 64 or lower')

    if random.random() < 0.5:   # Lead with a lower case letter...
        password = chr(random.randrange(97, 123))
    else:                       # ... otherwise lead with an upper case letter.
        password = chr(random.randrange(65, 91))

    while len(password) < num:
        x = random.randrange(0, 100)    # Like rolling a hundred-sided die.

        # If the user wants to include special characters in the
        # result, and if random number x is in the range of 80 to 99,
        # add a random special character.  Since there are four ASCII
        # ranges of such characters, we select the range from the first
        # "roll", then we "roll again" to  randomly choose a character
        # from that range.
        if special and len(password) < (num - 1):
            if x >= 80 and x < 85:
                password += chr(random.randrange(32, 48))
                x = random.randrange(0, 100)    # Get a new x.
            elif x >= 85 and x < 90:
                password += chr(random.randrange(58, 65))
                x = random.randrange(0, 100)    # Get a new x.
            elif x >= 90 and x < 95:
                password += chr(random.randrange(91, 97))
                x = random.randrange(0, 100)    # Get a new x.
            elif x >= 95 and x < 100:
                password += chr(random.randrange(123, 127))
                x = random.randrange(0, 100)    # Get a new x.

        # Add a random letter or digit.
        if x < 47:      # There's a 47% chance you'll get a lower case letter.
            password += chr(random.randrange(97, 123))
        elif x < 72:    # There's a 25% chance you'll get a numeral.
            password += chr(random.randrange(48, 58))
        else:           # There's a 28% chance you'll get an upper case letter.
            password += chr(random.randrange(65, 91))

    return password

    # end function create_password


def create_dice_passphrase(num=8):
    """
    Create a passphrase from randomly selected words.

    Keyword arguments:
    num -- number of words in passphrase (default 8)

    Raises:
    NotIntegerError -- if num is not an integer
    NumberTooLowError -- if num < 7
    NumberTooHighError -- if num > 64
    FileNotFoundError -- if WordList.json cannot be found

    Returns: a string

    This function creates a passphrase of num random words selected
    from a file called WordList.json that is stored in the script's
    directory.  The word list and the algorithm for selecting words come
    from the Diceware web site. To learn more about the Diceware
    algorithm, visit http://world.std.com/~reinhold/diceware.html.

    This program generates passphrases of at least 20 but no more than
    50 characters to ensure compatibility with miniLock file encryption.
    If the value of numberOfItems is too low or too high the function
    could get stuck in an infinite loop trying to find a passphrase of
    the correct length.  To prevent that from happening the function
    will raise an exception rather than try to fulfill the request.
    """
    if not isinstance(num, int):
        raise NotIntegerError('num must be a valid number')
    if num < 4:
        raise NumberTooLowError('num must be 4 or greater')
    if num > 12:
        raise NumberTooHighError('num must be 12 or lower')

    script_root = os.path.dirname(os.path.realpath(__file__))
    full_file_path = os.path.join(script_root, 'WordList.json')

    # Load the Dice word list file or raise an exception.
    try:
        with open(full_file_path, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
    except:
        raise FileNotFoundError('the file could not be found')

    # Continue creating passphrases until we get one of the correct size.
    while True:
        phrase = ''
        words = []

        # Per the Dice algorithm we'll simulate rolling 5 6-sided dice
        # to generate the key for each word in our passphrase.
        for roll in range(num):
            key = ''
            for die in range(5):
                key += str(random.randrange(1, 7))
            words.append(dictionary[key])
        phrase = ' '.join(words)
        if 20 <= len(phrase) <= 50:
            break

    return phrase

    # end function create_dice_passphrase


def main():
    # Get the commandline arguments.
    params = argparse.ArgumentParser(
        description=('Generates a password from random characters or a '
                     'passphrase using the Dice algorithm.'),
        epilog='_'
    )
    params.add_argument(
        '-n', '--number',
        type=int,
        help='the number of characters or words to include in the result'
    )
    # It doesn't make any sense to ask for a dice passphrase AND special
    # characters.
    ex_params = params.add_mutually_exclusive_group()
    ex_params.add_argument(
        '-s', '--special',
        action='store_true',  # normally false, make it true if present
        help='include special characters in the password'
    )
    ex_params.add_argument(
        '-d', '--dice',
        action='store_true',  # normally false, make it true if present
        help='use the Diceware algorithm to generate a passphrase'
    )

    args = params.parse_args()

    if args.dice:
        try:
            if args.number:
                result = create_dice_passphrase(args.number)
            else:
                result = create_dice_passphrase()
        except NotIntegerError:
            result = ('You can specify how many words you want in your '
                      'resulting passphrase. The value you enter for '
                      '"--number" must be an integer.')
        except NumberTooLowError:
            result = ('A secure passphrase should be at least 20 characters '
                      'long. This is difficult to achieve with fewer than '
                      'four words, so this program requires that "--number" '
                      'be at least 4.')
        except NumberTooHighError:
            result = ('To be compatible with minilock file encryption this '
                      'program limits passphrases to 50 characters. This is '
                      'difficult to achieve with more than 12 words, so this '
                      'script requires that "--number" be no more than 12.')
        except FileNotFoundError:
            result = ('This program builds passphrases from words found in a '
                      'file named WordList.json, which must be located in the '
                      'same directory as this script. You\'re seeing this '
                      'error because the file cannot be found there.')
        except:
            result = 'create_dice_passphrase failed for some reason.'
        finally:
            print(textwrap.fill(result))
    else:
        try:
            if args.number:
                result = create_password(args.number, args.special)
            else:
                result = create_password(special=args.special)
        except NotIntegerError:
            result = ('You can specify how many characters you want in your '
                      'resulting password. The value you enter for '
                      '"--number" must be an integer.')
        except NumberTooLowError:
            result = ('A secure password should be at least seven characters '
                      'long. This script requires that "--number" be at '
                      'least 7.')
        except NumberTooHighError:
            result = ('A reasonable password shouldn\'t be too long. This '
                      'script requires that "--number" be no more than 64.')
        except:
            result = 'create_password failed for some reason.'
        finally:
            print(textwrap.fill(result))


if __name__ == '__main__':
    main()
