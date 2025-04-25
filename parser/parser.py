import nltk
from nltk import word_tokenize
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | VP NP | VP NP Conj VP | NP Conj VP
NP -> N | Det NP | P NP | P Det NP | P Det Adj NP | Det Adj NP | N Adv V | Conj NP | NP P | Conj VP NP | Adj NP | NP Adv | NP VP
VP -> V | V NP | Conj NP VP | NP VP | Conj VP | NP Conj NP VP | VP P | VP NP NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    list_of_words = list()
    sentence = sentence.lower()
    list_of_words = word_tokenize(sentence)
    for word in list_of_words:
        contains_alphabet = False
        for char in word:
            if char.isalpha():
                contains_alphabet = True
        if contains_alphabet == False:
            list_of_words.remove(word)
    return list_of_words
    raise NotImplementedError


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    npc = list()
    for subtree in tree.subtrees():
        secondary_subtrees = subtree.subtrees()
        np_count = 0
        for subtree2 in secondary_subtrees:
            if subtree2.label() == "NP":
                np_count += 1
        if subtree.label() == "NP" and np_count == 1:
            npc.append(subtree)
    return npc
    raise NotImplementedError


if __name__ == "__main__":
    main()
