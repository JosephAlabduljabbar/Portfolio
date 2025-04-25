import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    page_dict = corpus
    prob_distribution = dict()
    base_chance = (1-damping_factor)/len(page_dict)

    for key in page_dict:
        prob_distribution.update({key: base_chance})

    if len(page_dict.get(page)) > 0:
        chance_to_add = damping_factor/len(page_dict.get(page))
        links = page_dict.get(page)
        for key in prob_distribution:
            if key in links:
                prob_distribution.update({key: prob_distribution.get(key) + chance_to_add})
    else:
        for key in prob_distribution:
            prob_distribution.update({key: 1/len(prob_distribution)})

    return prob_distribution
    raise NotImplementedError

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_dict = corpus
    prob_distribution = dict()
    for key in page_dict:
        prob_distribution.update({key: 0})

    start_page_index = random.randint(0, len(page_dict)-1)
    start_page = list(page_dict)[start_page_index]

    for i in range(n):
        possible_next_pages = transition_model(corpus, start_page, damping_factor)
        random_selection = random.randint(0, 10000)/10000
        cumulative_prob = 0
        for key in possible_next_pages:
            cumulative_prob += possible_next_pages.get(key)
            if cumulative_prob >= random_selection:
                prob_distribution.update({key: prob_distribution.get(key) + 1})
                start_page = key
                break
                

    for key in prob_distribution:
        prob_distribution.update({key: prob_distribution.get(key)/n})
    return prob_distribution
    raise NotImplementedError


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prob_distribution = dict()
    for key in corpus:
        prob_distribution.update({key: 1/len(corpus)})
    
    max_change = 1
    while max_change > 0.001:
        max_change = 0
        for key in prob_distribution:
            sigma_term = 0
            pages_with_links = list()
            for key2 in corpus:
                for value in list(corpus.get(key2)):
                    if value == key:
                        pages_with_links.append(key2)
            for value in pages_with_links:
                if len(list(corpus.get(value))) == 0:
                    sigma_term += prob_distribution.get(value)/len(corpus)
                else:
                    sigma_term += prob_distribution.get(value)/len(list(corpus.get(value)))
            old_value = prob_distribution.get(key)
            new_value = ((1-damping_factor)/len(corpus)) + (damping_factor*sigma_term)
            if abs(old_value-new_value) > max_change:
                max_change = abs(old_value-new_value)
            pages_with_links.clear()
            prob_distribution.update({key: new_value})

    return prob_distribution

    raise NotImplementedError


if __name__ == "__main__":
    main()
