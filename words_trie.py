import utils


class TrieNode:
    def __init__ (self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.score_multiplier = 2
        self.replace_penalty_multiplier = 1
        self.remove_add_penalty_multiplier = 2
        self.penalty_offset = 5
        self._next_penalty_base = lambda x: x - 1 if x > 1 else 1


    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True


    def search_sentences(self, sentence):
        words = utils.extract_words(sentence)
        sentences = {}
        mismatch_detected = False
        matching_words_score = 0
        for index, word in enumerate(words):
            word_matches = self._search_words(word, self._calc_word_offset(words, index))    
            if len(word_matches) == 1 and word_matches[0][0] == word:
                matching_words_score += word_matches[0][1] + index * self.score_multiplier
                continue
            elif len(word_matches) != 0 and not mismatch_detected:
                mismatch_detected = True
                for match in word_matches:
                    modified_words = words.copy()
                    modified_words[index] = match[0]
                    sentences[' '.join(modified_words)] = match[1]
            else:
                return {}
            
        for sentence in sentences:
            sentences[sentence] += matching_words_score

        if sentences != {}: 
            return sentences
        else:
            return {sentence: len(sentence) * self.score_multiplier}
    
        
    def _search_words(self, word, word_offset, max_edits = 1):
        score = 0
        penalty_base = self.penalty_offset - word_offset
        if penalty_base < 1: 
            penalty_base = 1
        results = []
        does_word_exist = [False]
        self._dfs(self.root, word, 0, '', max_edits, results, does_word_exist, penalty_base, score)
        return results


    def _calc_word_offset(self, words, index):
        if index < 0 or index > len(words):
            raise ValueError("Index is out of bounds")
        return sum( len(word)+index-1 if index == 0 else len(word)+index  for word in words[:index] )


    def _dfs(self, node, word, index, current_word, edits_left, results, does_word_exist, penalty_base, score):

        if word == '': return
        if edits_left < 0: return

        if index == len(word):
            if node.is_end_of_word:
                results.append( (current_word, score) )
                if word == current_word:
                    results.clear()
                    results.append( (current_word, score) )
                    does_word_exist[0] = True
            if not does_word_exist:    
                results.extend( ( (current_word + char, score - penalty_base * self.remove_add_penalty_multiplier) 
                                 for char, child in node.children.items() if child.is_end_of_word ) ) # edge case where the missing char is last
            return
        
        current_char = word[index]
        
        # Exact match
        if current_char in node.children:
            if self._dfs(node.children[current_char], word, index + 1, current_word+current_char, edits_left, results, does_word_exist, 
                          self._next_penalty_base(penalty_base), score + self.score_multiplier): return True
        
        if does_word_exist == [False]:
            
            # Replacement
            for char in node.children:
                if char != current_char: # ignore exact match
                    self._dfs(node.children[char], word, index + 1, current_word+char, edits_left-1, results,
                               does_word_exist, self._next_penalty_base(penalty_base), score - penalty_base * self.replace_penalty_multiplier) 
            
            # Insertion (skip char in given word)
            self._dfs(node, word, index + 1, current_word, edits_left-1, results, does_word_exist,
                       self._next_penalty_base(penalty_base), score - penalty_base * self.remove_add_penalty_multiplier)
            
            # Deletion (same as replacement but the index stays)
            for char in node.children:
                self._dfs(node.children[char], word, index, current_word+char, edits_left-1, results, does_word_exist,
                           self._next_penalty_base(penalty_base), score - penalty_base * self.remove_add_penalty_multiplier)
