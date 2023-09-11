#!/usr/bin/env python3
""" Module for testing sort algorithms. """

# pylint: disable=protected-access

import unittest
from src.trie import Trie
from src.exceptions import SearchMiss

class TestList(unittest.TestCase):
    """ Submodule for unittests, derives from unittest.TestCase """
    def setUp(self):
        """ Create object for all tests """
        # Arrange
        self.file_name = "frequency.txt"
        # self.file_name = "tiny_frequency.txt"
        self.trie = Trie(self.file_name)
        self.word = "MyOwnWordNotInOriginalTrie"
        self.frequency = "100.9"


    def tearDown(self):
        """ Remove dependencies after test """
        self.trie = None
        self.word = None
        self.frequency = None


    def test_word_not_in_trie(self):
        """ test if word is not in Trie. """
        with self.assertRaises(SearchMiss):
            _ = self.trie.is_word("ThisWordIsNotInTrie")


    def test_if_word_in_trie(self):
        """ test to add a word and see if it is in Trie."""
        self.trie.add_word(self.word, self.frequency)
        self.assertIsInstance(self.trie.is_word(self.word), list)


    def test_remove_word(self):
        """ test to remove a word from Trie. """
        self.trie.add_word(self.word, self.frequency)
        self.trie.delete_word(self.word)
        with self.assertRaises(SearchMiss):
            _ = self.trie.is_word(self.word)


    def test_remove_word_not_in_trie(self):
        """ Test to remove a word that is not in Trie. """
        word = "ThisIsNotInTrie"

        with self.assertRaises(SearchMiss):
            self.trie.delete_word(word)


    def test_correct_nr_of_words_in_trie(self):
        """ Test if nr of words in trie == nr of words in file. """
        all_words_in_trie = {}
        all_words_in_file = []

        with open(self.file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                all_words_in_file.append(line)
        self.trie._get_words(self.trie.root, "", all_words_in_trie)

        self.assertEqual(len(all_words_in_trie.keys()), len(all_words_in_file))


    def test_add_existing_word(self):
        """ Adding an existing word should not create a duplicate. """
        all_words_before = {}
        all_words_after = {}

        self.trie.add_word(self.word, self.frequency)
        self.trie._get_words(self.trie.root, "", all_words_before)
        before = len(all_words_before.keys())

        self.trie.add_word(self.word, self.frequency)
        self.trie._get_words(self.trie.root, "", all_words_after)
        after = len(all_words_after.keys())

        self.assertEqual(after, before)


    def test_get_all_words_merge_sort(self):
        """
        test if all words are printed in alphabetical order with merge sort.
        """
        all_words = {}
        self.trie._get_words(self.trie.root, "", all_words)
        list_for_merge_sort = list(all_words.keys())
        list_for_sorted = list_for_merge_sort.copy()

        self.trie._merge_sort(list_for_merge_sort)
        sorted_with_python = sorted(list_for_sorted)

        for i, word in enumerate(sorted_with_python):
            self.assertEqual(word, list_for_merge_sort[i])
