#!/usr/bin/python3
""" Trie """

from src.node import Node
from src.exceptions import SearchMiss

class Trie:
    """
    reads file and creates a Trie.
    If no frequency in file all node.frequency = -1
    """

    def __init__(self, file_name):
        """ constructor. """
        self.root = Node('root')
        with open(file_name, mode="r", encoding="utf-8") as file:
            for line in file:
                word = line.split()
                if len(word) == 2:
                    self.add_word(word[0], word[1])
                else:
                    self.add_word(word[0])


    def _merge_sort(self, word_list):
        """ merge sort """
        if len(word_list) <= 1:
            return

        middle = len(word_list) // 2
        left_list = word_list[:middle]
        right_list = word_list[middle:]
        self._merge_sort(left_list)
        self._merge_sort(right_list)

        left_index = 0
        right_index = 0
        list_index = 0

        while left_index < len(left_list) and right_index < len(right_list):
            if left_list[left_index] <= right_list[right_index]:
                word_list[list_index] = left_list[left_index]
                left_index += 1
            else:
                word_list[list_index] = right_list[right_index]
                right_index += 1
            list_index += 1

        while left_index < len(left_list):
            word_list[list_index] = left_list[left_index]
            left_index += 1
            list_index += 1

        while right_index < len(right_list):
            word_list[list_index] = right_list[right_index]
            right_index += 1
            list_index += 1


    def get_words(self):
        """ Prints all words from Trie."""
        all_words = {}
        self._get_words(self.root, "", all_words)
        word_list = list(all_words.keys())
        self._merge_sort(word_list)
        self._print_words(word_list)


    def _get_words(self, node, prefixes, list_of_words):
        """
        Visit all nodes below node recursevly and add prefixes to
        list_of_words if the node is a word.
        """
        if node.word:
            list_of_words[prefixes] = node.frequency

        for char in node.letters:
            new_prefixes = prefixes + char
            self._get_words(node.letters[char], new_prefixes, list_of_words)


    @staticmethod
    def _print_words(list_of_words):
        """ prints words in list_of_words. """
        for word in list_of_words:
            print(word)


    def auto_complete(self, prefixes):
        """
        show (at most) 10 most frequent words beginning with prefixes.
        Raise SearchMiss if prefixes not in trie.
        """
        max_words = 10
        all_words = {}
        current_node = self.root

        for char in prefixes:
            if char not in current_node.letters:
                raise SearchMiss("no matching words")
            current_node = current_node.letters[char]

        self._get_words(current_node, prefixes, all_words)
        sorted_by_frequency = sorted(all_words.items(), key=lambda x: x[1], reverse=True)
        for i, word in enumerate(sorted_by_frequency):
            if i == max_words:
                break
            print(word[0])


    def delete_word(self, word):
        """
        Remove word if it is a word else,
        self.is_word(String) raise SearchMiss if word is not in Trie.
        """
        visited_nodes = self.is_word(word)

        last_node = visited_nodes.pop()
        last_node.word = False
        for node in reversed(visited_nodes):
            #previous nodes can become childless words
            if last_node.letters or last_node.word:
                break
            _ = node.letters.pop(last_node.prefix)
            last_node = node


    def add_word(self, word, frequency=-1):
        """ Add word and optional frequency to Trie. """
        current_node = self.root

        for char in word:
            if char in current_node.letters:  # if char already exist
                current_node = current_node.letters[char]
                continue
            new_node = Node(char)
            current_node.letters[char] = new_node
            current_node = new_node
        # last node is always a word
        current_node.word = True
        current_node.frequency = float(frequency)


    def is_word(self, word):
        """
        Returns List with visited nodes if word is a word in dictionary,
        Raise SearchMiss if not.
        """
        current_node = self.root
        visited_nodes = [current_node]  # root isn't added in loop

        for char in word:
            if char not in current_node.letters:
                raise SearchMiss("word is missing")
            current_node = current_node.letters[char]
            visited_nodes.append(current_node)

        if current_node.word is False:
            raise SearchMiss("word is missing")

        return visited_nodes
