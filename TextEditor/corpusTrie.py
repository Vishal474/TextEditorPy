import pickle

class TrieNode():

	def __init__(self):
		self.children = {}
		self.eo_word = False
		self.weight = 0

class Trie(object):

	def __init__(self):

		self.head = TrieNode()
		self.word_list = {}

	def formTrie(self):

		with open("corpus.txt",'r') as file:
			line = file.readlines()
			for word in line:
				self.insert(word)

	def insert(self,word):

		node = self.head
		alphabet, weight = word.split(",")
		# split weightage and alphabet from word

		for a in list(alphabet):
			if not node.children.get(a):
				node.children[a] = TrieNode()

			node = node.children[a]

		node.eo_word = True
		node.weight = weight

	def createPickledTrie(self):
		with open("sampletrie.pkl",'wb') as file:
			pickle.dump(self.head,file,pickle.HIGHEST_PROTOCOL)

	def loadTrie(self):
		with open("sampletrie.pkl",'rb') as file:
			self.head = pickle.load(file)

	def wordSearch(self,word):

		node = self.head
		
		# Searches the given key in trie for a full match 
        # and returns True on success else returns False. 
		
		for a in word: 
			if not node.children.get(a):
				return False
  
			node = node.children[a]
  
		return node and node.eo_word

	def suggestionsRec(self, node, word): 
          
        # Method to recursively traverse the trie 
        # and return a whole word.  
		if node.eo_word: 
			self.word_list[word] = int(node.weight.strip())

		for a,n in node.children.items(): 
			self.suggestionsRec(n, word + a) 

	def prefixSearch(self,word):

		# Returns all the words in the trie whose common 
        # prefix is the given key thus listing out all  
        # the suggestions for autocomplete. 
		self.word_list = {}
		node = self.head 
		not_found = False
		temp_word = '' 
  
		for a in list(word): 
			if not node.children.get(a): 
				not_found = True
				break
  
			temp_word += a 
			node = node.children[a] 
  
		if not_found: 
			return word
		# elif node.last and not node.children: 
		# 	return -1
  
		self.suggestionsRec(node, temp_word) 

		return self.word_list