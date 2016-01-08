import os
import sys

class Node:
    def __init__(self, char=False, is_word=False):
        self.children = {}
        self.char = char
        self.is_word = is_word

    def get_child(self, char):
        if char in self.children:
            return self.children[char]
        else:
            return None

    def add_child(self, char):
        new_child = Node(char)
        self.children[char] = new_child
        return new_child

    def set_is_word(self, is_word):
        self.is_word = is_word


class Trie:
    def __init__(self):
        self.root = Node()
        # This is a dict where the key is the word length
        # and the value is a list of words of that length
        self.word_len_dict = {}

    def insert(self, word):
        current = self.root
        for char in word:
            next_child = current.get_child(char)
            if not next_child:
                next_child = current.add_child(char)
            current = next_child
        current.set_is_word(True)
        self._set_word_in_dict(word)

    def _set_word_in_dict(self, word):
        ''' Keeping a dict wjere the key is an integer
        len(word) and the value is a list of words of
        that length.
        '''
        w_len = len(word)
        if w_len in self.word_len_dict:
            word_list = self.word_len_dict[w_len]
        else:
            word_list = []
        word_list.append(word)
        self.word_len_dict[w_len] = word_list

    def get_longest_compound_word(self):
        ''' Now, use the word_len_dict to inspect the
            longest words for compound-ness.
            Return the first (largest) that you find.

            This saves us from performing redundant 
            lookups and prefix madness as we go along.

            Since a dict has constant lookup time, we
            should save a lot of effort.
        '''
        reversed_key_list = list(reversed(self.word_len_dict.keys()))
        for key in reversed_key_list:
            for word in self.word_len_dict[key]:
                if self.is_word_compound(word):
                    # If we wanted to return a list of words that are
                    # all the same length, we would just append word
                    # to that list here.
                    # But, the instructions were explicit, so we will
                    # just return our first match
                    return word
        return None

    def is_word_compound(self, word):
        ''' A recursive function to check prefixes of a given word
            and tell if they are valid words.
        '''
        is_word_compound = False
        if word:
            for prefix in self.get_prefix_list(word):
                len_p = len(prefix)
                suffix = word[len_p:]
                if suffix:
                    if self.is_word_in_trie(suffix):
                        return True
                    else:
                        is_word_compound = self.is_word_compound(suffix)
        return is_word_compound


    def get_prefix_list(self, word):
        ''' Returns a list of all prefixes of the given word
            Tht list includes the word itself as a prefix.
        '''
        prefix = ''
        prefix_list = []
        current = self.root
        for char in word:
            current = current.get_child(char)
            if not current:
                return prefix_list
            prefix += char
            if current.is_word:
                prefix_list.append(prefix)
        return prefix_list


    def is_word_in_trie(self, word):
        ''' Check to see if a given word can be found
            in the trie, starting at the root.
        '''
        current = self.root
        for char in word:
            current = current.get_child(char)
            if not current:
                return False
        if current.is_word:
            return True
        else:
            return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage:  Please specify a filename."
    else:
        filename = sys.argv[1]
        trie = Trie()
        f = open(filename, 'r')
        for word in f:
            trie.insert(word.rstrip())
        lcw = trie.get_longest_compound_word()
        print lcw

