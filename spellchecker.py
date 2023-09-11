#!/usr/bin/python3
""" Main file with SpellChecker class """

import sys
import inspect
from src.trie import Trie
from src.exceptions import SearchMiss


class SpellChecker:
    """ SpellChecker class """

    _OPTIONS = {
        "1": "word_in_trie",
        "2": "prefix_search",
        "3": "change_dictionary",
        "4": "print_all_words",
        "5": "remove_word",
        "6": "exit"
    }

    def __init__(self):
        """ Initialize class """
        file_name = "frequency.txt"
        self.trie = Trie(file_name)

    def _get_method(self, method_name):
        """
        Uses function getattr() to dynamically get value of an attribute.
        """
        return getattr(self, self._OPTIONS[method_name])

    def _print_menu(self):
        """
        Use docstring from methods to print options for the program.
        """
        menu = ""

        for key in sorted(self._OPTIONS):
            method = self._get_method(key)
            docstring = inspect.getdoc(method)

            menu += "{choice}: {explanation}\n".format(
                choice=key,
                explanation=docstring
            )

        # print(chr(27) + "[2J" + chr(27) + "[;H")
        print(menu)

    def word_in_trie(self):
        """ Check if word is in Trie. """
        value = input("\nword: \n>>> ")
        try:
            _ = self.trie.is_word(value.lower())
            print("word is spelled correctly.")
        except SearchMiss:
            print("word does not exist")

    def prefix_search(self):
        """ Search with prefixes. """
        first_value = input("\nEnter 3 letters: \n>>> ")
        try:
            self.trie.auto_complete(first_value.lower())
        except SearchMiss as e:
            print(e)
        while True:
            value = input("\nEnter another letter or 'quit' to exit: \n>>>")
            if value == "quit":
                break
            first_value += value
            try:
                self.trie.auto_complete(first_value.lower())
            except SearchMiss as e:
                print(e)

    def change_dictionary(self):
        """ Change dictionary for trie. """
        value = input("\nnew file: \n>>> ")
        try:
            self.trie = Trie(value)
        except FileNotFoundError:
            print("file doesn't exist")

    def print_all_words(self):
        """ Print all words in trie. """
        self.trie.get_words()

    def remove_word(self):
        """ Remove word from trie. """
        value = input("\nword: \n>>> ")
        try:
            self.trie.delete_word(value.lower())
            print("deleted word")
        except SearchMiss as e:
            print(e)

    @staticmethod
    def exit():
        """ Quit the program """
        sys.exit()

    def main(self):
        """ Start method """
        while True:
            self._print_menu()
            choice = input("Enter menu selection:\n-> ")

            try:
                self._get_method(choice.lower())()
            except KeyError:
                print("Invalid choice!")

            input("\nPress any key to continue ...")

if __name__ == "__main__":
    s = SpellChecker()
    s.main()
