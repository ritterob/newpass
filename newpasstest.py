# newpasstest.py

import unittest
import re
import newpass


class CreatePasswordBadInput(unittest.TestCase):
    def test_not_a_number(self):
        """create_password should fail if the input is not an integer."""
        self.assertRaises(
            newpass.NotIntegerError, newpass.create_password, 'Dave')

    def test_number_too_high(self):
        """create_password should fail if the input value is above 64."""
        self.assertRaises(
            newpass.NumberTooHighError, newpass.create_password, 65)

    def test_number_too_low(self):
        """create_password should fail if the input value is below 7."""
        self.assertRaises(
            newpass.NumberTooLowError, newpass.create_password, 6)


class CreatePasswordTestResult(unittest.TestCase):
    special_characters = re.compile('[ -/:-@[-`{-~]')

    def test_default_results(self):
        """
        create_password should return a 10-character password with no
        special characters by default.
        """
        for i in range(100):    # run the test 100 times
            result = newpass.create_password()
            self.assertEqual(len(result), 10)
            self.assertNotRegex(result, self.special_characters)

    def test_results_with_special_characters(self):
        """
        create_password should return a 10-character password with
        special characters at least once.
        """
        specials_found = False
        for i in range(100):    # run the test 100 times
            result = newpass.create_password(special=True)
            if self.special_characters.search(result):
                specials_found = True
            self.assertEqual(len(result), 10)
        self.assertTrue(specials_found)

    def test_results_with_varied_password_lengths(self):
        """
        create_password should return a password of the given length
        with no special characters.
        """
        for i in range(7, 65):   # test all valid password lengths
            for j in range(100):    # run each test 100 times
                result = newpass.create_password(i)
                self.assertEqual(len(result), i)
                self.assertNotRegex(result, self.special_characters)

    def test_results_with_varied_password_lengths_and_specials(self):
        """
        create_password shoud return a password of the given length
        with special characters at least once.
        """
        specials_found = False
        for i in range(7, 65):  # test all valid password lengths
            for j in range(100):    # run each test 100 times
                result = newpass.create_password(i, True)
                if self.special_characters.search(result):
                    specials_found = True
                self.assertEqual(len(result), i)
            self.assertTrue(specials_found)
            specials_found = False     # reset for each password length test


class CreateDicePassphraseBadInput(unittest.TestCase):
    def test_not_a_number(self):
        """
        create_dice_passphrase should fail if the input is not an
        integer.
        """
        self.assertRaises(
            newpass.NotIntegerError, newpass.create_dice_passphrase, 'Dave')

    def test_number_too_high(self):
        """create_dice_passhrase should fail if the input value is above 12."""
        self.assertRaises(
            newpass.NumberTooHighError, newpass.create_dice_passphrase, 13)

    def test_number_too_low(self):
        """create_dice_passphrase should fail if the input value is below 4."""
        self.assertRaises(
            newpass.NumberTooLowError, newpass.create_dice_passphrase, 3)


class CreateDicePassphraseTestResult(unittest.TestCase):
    def test_default_results(self):
        """
        create_dice_passphrase should return an 8-word passphrase
        between 20 and 50 characters long by default.
        """
        for i in range(100):  # run the test 100 times
            passphrase = newpass.create_dice_passphrase()
            self.assertEqual(len(passphrase.split()), 8)
            self.assertTrue(20 <= len(passphrase) <= 50)

    def test_results_with_varied_password_lengths(self):
        """
        create_dice_passphrase should return a passphrase with the
        required number of words that is between 20 and 50 characters
        long.
        """
        for i in range(4, 13):   # test all valid passphrase sizes
            for j in range(100):    # run each test 100 times
                passphrase = newpass.create_dice_passphrase(i)
                self.assertEqual(len(passphrase.split()), i)
                self.assertTrue(20 <= len(passphrase) <= 50)


if __name__ == '__main__':
    unittest.main()
