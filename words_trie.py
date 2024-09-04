class TrieNode:
    def __init__ (self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_similar(self, word, max_edits = 1):
        results = [] 
        does_word_exist = [False]
        self._dfs(self.root, word, 0, '', max_edits, results, does_word_exist)
        return results

    '''
    Searches for the exact (non empty) word in the trie tree and if not found it searches for all similar words using 3 different cases:
    replacement, insertion or subtraction of a char.
    word can be any generic type with len() function, == and [] operators
    '''
    def _dfs(self, node, word, index, current_word, edits_left, results, does_word_exist):

        if word == '': return
        if edits_left < 0: return

        if index == len(word):
            if node.is_end_of_word:
                results.append(current_word)
                if word == current_word:
                    results.clear()
                    results.append(current_word)
                    does_word_exist[0] = True
            results.extend(current_word + char for char, child in node.children.items() if child.is_end_of_word) # edge case where the missing char is last
            return
        
        current_char = word[index]
        
        # Exact match
        if current_char in node.children:
            if self._dfs(node.children[current_char], word, index + 1, current_word+current_char, edits_left, results, does_word_exist): return True
        
        if does_word_exist == [False]:
            
            # Replacement
            for char in node.children:
                if char != current_char: # ignore exact match
                    self._dfs(node.children[char], word, index + 1, current_word+char, edits_left-1, results, does_word_exist) 
            
            # Insertion (skip char in given word)
            self._dfs(node, word, index + 1, current_word, edits_left-1, results, does_word_exist)
            
            # Deletion (same as replacement but the index stays)
            # *** Fix last character missing ***
            for char in node.children:
                self._dfs(node.children[char], word, index, current_word+char, edits_left-1, results, does_word_exist)
