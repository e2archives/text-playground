
# coding: utf-8

# In[162]:

import spacy
import itertools
import networkx as nx


# In[163]:

nlp = spacy.load('en')


# In[196]:

class TextSummarizer:  
    def __init__(self,docs=None,token_filter=None,dist_func=None):
        self.docs = docs
        self.token_filter = token_filter if token_filter else self.is_noun_or_adj 
        self.graph_sent = None
        self.graph_words = None
        self.nouns = None
        self.sents = None
        self.ents = None
        
    def sent_bow(self):
        for i,sent in enumerate(self.docs.sents):
            bow = [token.vector for token in sent.subtree if is_noun_or_adj(token)]
            yield (i,bow,sent)
    
    def pack(self):
        return {
            'sents': self.sents,
            'nouns': self.nouns,
            'ents': self.ents
        }
    
    def summarize(self):
        self.graph_nouns = self._buildGraph("noun_chunks")
        nouns = nx.pagerank(self.graph_nouns, weight='weight')
        self.nouns = sorted(nouns, key=nouns.get, reverse=True)

        self.graph_sent = self._buildGraph("sents")
        sents = nx.pagerank(self.graph_sent, weight='weight')
        self.sents = sorted(sents, key=sents.get, reverse=True)[0:5]
        ents = dict()
        
        for ent in self.docs.ents:
            if ents.get(ent.label_) is None:
                ents[ent.label_] = set()
            ents[ent.label_].add(ent.text)
        
        for key in ents:
          ents[key] = list(ents[key])
        
        self.ents = ents
        return self
        
    
    def _buildGraph(self,node_type=None):
        if node_type is "noun_chunks":
            chunk_iter = self.docs.noun_chunks
        else:
            chunk_iter = self.docs.sents
        
        sents = [sent for sent in chunk_iter] 
        sents_str = [sent.text for sent in sents]

        gr = nx.Graph() #initialize an undirected graph
        gr.add_nodes_from(sents_str)
        nodePairs = list(itertools.combinations(sents, 2))

        for pair in nodePairs:
            sent1 = pair[0]
            sent2 = pair[1]
            weight = sent1.similarity(sent2)
            gr.add_edge(sent1.text, sent2.text, weight=weight)
            
        return gr

    def from_file(file):
        with open(file) as f:
            docs = nlp(f.read())
        return TextSummarizer(docs)
        
    def from_text(text):
        return TextSummarizer(nlp(text))
                
    def is_noun_or_adj(token):
        return token.pos == spacy.parts_of_speech.NOUN or token.pos == spacy.parts_of_speech.ADJ

