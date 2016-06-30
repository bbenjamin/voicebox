__author__ = 'jamiebrew'

import corpus
import operator

# keeps a dictionary of corpora with associated weights
class voice(object):

    def __init__(self, paths_names_weights, voicename):
        self.name = voicename
        self.weighted_corpora = {}
        for path, name, weight in paths_names_weights:
            self.weighted_corpora[name] = [corpus.corpus(path, name), weight]

    def suggest(self, sentence, cursor_position, num_words, sort_attribute = "FREQUENCY"):
        suggestions = {}
        for key in self.weighted_corpora:
            corpus, weight = self.weighted_corpora[key]
            if not weight == 0:
                contributed_suggestions = corpus.suggest(sentence, cursor_position, num_words, sort_attribute)
                for word, score in contributed_suggestions:
                    if word in suggestions:
                        suggestions[word] += score * weight
                    else:
                        suggestions[word] = score * weight
        suggestion_list = list(reversed(sorted(suggestions.items(), key=operator.itemgetter(1))))[0:num_words]
        return suggestion_list[0:num_words]

def first_test():
    p_n_w = [('texts/batman', 'batman', 1), ('texts/bowie', 'bowie', 1), ('texts/queenspeech', 'queen', 2)]

    v = voice(p_n_w, 'queen_bowman')
    suggestions =  v.suggest('i am so very',4,20)
    print len(suggestions)
    for s in suggestions:
        print s
