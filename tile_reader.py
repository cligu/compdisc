import spacy
import re, sys
import numpy as np
from collections import OrderedDict, defaultdict

class TileReader:

	def __init__(self, vocab_tags=[]):
		self.nlp = spacy.load('en')
		self.doc = None
		self.vocab_tags = []

	def set_vocab_tags(self, tag_list):
		"""
		Function to set POS tags considered in vocabulary bulding. Typically only lexical
		tags such as NOUN, PROPN, VERB or ADJ will be used

		:param tag_list: List of POS tag strings to include in vocabulary building
		:return: void
		"""
		self.vocab_tags = tag_list

	def read(self, file_name):
		"""
		Reads a text file, runs NLP pipeline and collects vocabulary with frequencies

		:param file_name:
		:return: void
		"""
		text = open(file_name).read()
		text = re.sub(r'\n+', r'\n', text)
		self.doc = self.nlp(unicode(text.decode("utf8")))
		self.sentences = list(self.doc.sents)
		self.vocab = set([])
		freqs = defaultdict(int)
		tok_count = 0.0
		for token in self.doc:
			if token.pos_ in self.vocab_tags:
				self.vocab.add(token.lemma_)
			freqs[token.lemma_] += 1
			tok_count += 1
		self.vocab = list(self.vocab)
		self.freqs = freqs

	def get_blocks(self, k, as_text=False):
		"""
		Generator function returning 2-place tuple with lists of sentences before and after a split window
		of size 2*k
		:param k: Half the window size, i.e. the number of sentences to return on either side of the split
		:param as_text: Return each sentence as text if True, else as list of tokens
		:return: ([A1,A2,..Ak],[B1,B2,..Bk]) - the tuple of two blocks listing sentences before and after split
		"""
		if 2*k > len(self.sentences):
			raise IndexError("Window k="+str(k)+" too large for text.\n \
			Expected > 2*" + str(k) +" sentences but only " + str(len(self.sentences)) + " found in text")

		for index, sent in enumerate(self.sentences[:len(self.sentences)-k]):
			if index+k+k <= len(self.sentences):
				if as_text:
					return (self.sentences[index:index+k],self.sentences[index+k:])
				else:
					return (list((sent) for sent in self.sentences[index:index + k]), list((sent) for sent in self.sentences[index + k:]))

def demo():
	reader = TileReader()
	#reader.read(r"c:\\uni\\teaching\\compdisc\\python\\mr_robot.txt")
	reader.read(r"C:\\Users\\owner\\OneDrive\\Documents\\44_25 LING 765 Discourse Modeling\\data\\robot.txt")
	reader.set_vocab_tags(["NOUN","PROPN"])
	blocks = reader.get_blocks(3,True)
	for blockA, blockB in blocks:
		#print str(blockA) + "\n----\n" + str(blockB) +"\n\n"
		print blockA[0][0]



if __name__ == "__main__":
	demo()