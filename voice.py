__author__ = 'jamiebrew'

import corpus
import operator

# keeps a dictionary of sources with associated weights
# TODO: a source can be a corpus or a voice (which itself points to several sources)
class voice(object):

    def __init__(self, weighted_corpora):
        self.name = 'no_name'
        self.weighted_corpora = weighted_corpora

    def suggest(self, sentence, cursor_position, num_words):
        suggestions = {}
        for key in self.weighted_corpora:
            corp, weight = self.weighted_corpora[key]
            if not weight == 0:
                contributed_suggestions = corp.suggest(sentence, cursor_position, num_words)
                for word, score in contributed_suggestions:
                    if word not in suggestions:
                        suggestions[word] = [0, {}]
                        suggestions[word][1][corp.name] = score * weight
                    else:
                        suggestions[word][0] += score * weight
                        suggestions[word][1][corp.name] = score * weight
        suggestions = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))[0:num_words]
        return suggestions[0:num_words]

    # adds a corpus to this voice
    def add_corpus(self, corp, name, weight):
        self.weighted_corpora[corp.name] = [corp, weight]


def first_test():
    p_n_w = [('texts/batman', 'batman', 1), ('texts/bowie', 'bowie', 1), ('texts/queenspeech', 'queen', 2)]

    v = voice(p_n_w, 'queen_bowman')
    suggestions =  v.suggest('i am so very',4,20)
    print len(suggestions)
    for s in suggestions:
        print s
