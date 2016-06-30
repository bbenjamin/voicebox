__author__ = 'jamiebrew'

import operator

# information about a unique string within a corpus
class ngram(object):

    def __init__(self, string):
        self.string = string
        self.count = 1                  # how many times this ngram occurs
        self.after = []                 # list of dictionaries
        self.before = []                # list of dictionaries
        self.frequency = 0              # normalized rate of occurrence
        self.sig_score = 0                    # significance score
        self.rhymes = {}

    def __str__(self):
        return self.string+"\ncount: "+str(self.count)+"\nfreq: "+str(self.frequency)+"\nsig: "+str(self.sig_score)+'\n'

    def __repr__(self):
        return self.string
    
    def __len__(self):
    	return len(self.string)

    # returns top n words occuring distance after this ngram
    def get_after(self, distance=1, n=20, sort_attribute="COUNT"):
        dictionary = self.after[distance-1]
        #print 'top %s words occuring %s after "%s":' % (n, distance, self.string)
        word_list = [] #TODO: cleaner way to do this
        for key in dictionary:
            if sort_attribute == "COUNT":
                word_list.append((dictionary[key], dictionary[key].count))
            elif sort_attribute == "FREQUENCY":
                word_list.append((dictionary[key], dictionary[key].frequency))
            elif sort_attribute == "SIG_SCORE":
                word_list.append((dictionary[key], dictionary[key].sig_score))
        return list(reversed(sorted(word_list, key=lambda tup: tup[1])))[0:n]

    # returns top n words occuring distance before this ngram
    def get_before(self, distance=1, n=20, sort_attribute="COUNT"):
        dictionary = self.before[distance-1]
        #print 'top %s words occuring %s before "%s":' % (n, distance, self.string)
        word_list = [] #TODO: cleaner way to do this
        for key in dictionary:
            if sort_attribute == "COUNT":
                word_list.append((dictionary[key], dictionary[key].count))
            elif sort_attribute == "FREQUENCY":
                word_list.append((dictionary[key], dictionary[key].frequency))
            elif sort_attribute == "SIG_SCORE":
                word_list.append((dictionary[key], dictionary[key].sig_score))
        return list(reversed(sorted(word_list, key=lambda tup: tup[1])))[0:n]

    def get_attribute(self, sort_attribute):
        if sort_attribute == "COUNT":
            return self.count
        elif sort_attribute == "FREQUENCY":
            return self.frequency
        elif sort_attribute == "SIG_SCORE":
            return self.sig_score
