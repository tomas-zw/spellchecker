#!/usr/bin/python3
""" Node """

class Node:
    """ Nodes for Trie. """

    def __init__(self, prefix, frequency=-1):
        """ constructor. """
        self.prefix = prefix
        self.word = False
        self.letters = {}
        self.frequency = frequency
