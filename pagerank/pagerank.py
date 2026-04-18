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
    N = len(corpus)
    prob = {}
    outgoing = corpus[page]

    # If no outgoing links, treat as equal probability to all pages
    if not outgoing:
        for p in corpus:
            prob[p] = 1 / N
        return prob

    # Base teleportation probability to every page
    teleport = (1 - damping_factor) / N
    for p in corpus:
        prob[p] = teleport

    # Add damping_factor * (1/|outgoing|) to each linked page
    link_prob = damping_factor / len(outgoing)
    for p in outgoing:
        prob[p] += link_prob

    return prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
       # Initialise counts
    counts = {page: 0 for page in corpus}
    
    # Choose first page uniformly at random
    import random
    current_page = random.choice(list(corpus.keys()))
    counts[current_page] += 1
    
    for _ in range(n - 1):
        # Get transition probabilities from current page
        probs = transition_model(corpus, current_page, damping_factor)
        # Choose next page according to probability distribution
        pages = list(probs.keys())
        probabilities = [probs[p] for p in pages]
        current_page = random.choices(pages, weights=probabilities, k=1)[0]
        counts[current_page] += 1
    
    # Normalise counts to probabilities
    return {page: counts[page] / n for page in corpus}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.
    """
    N = len(corpus)
    # Initialise all pages with equal probability
    pr = {page: 1 / N for page in corpus}
    
    # Convergence threshold (typical for this problem)
    while True:
        new_pr = {}
        for page in corpus:
            # Start with the teleportation term
            rank = (1 - damping_factor) / N
            
            # Sum contributions from all pages that link to 'page'
            for other in corpus:
                # If 'other' has no outgoing links, treat as linking to all pages
                out_links = corpus[other]
                if not out_links:
                    rank += damping_factor * (pr[other] / N)
                else:
                    if page in out_links:
                        rank += damping_factor * (pr[other] / len(out_links))
            new_pr[page] = rank
        
        # Check for convergence (maximum change < 0.001)
        diff = max(abs(new_pr[page] - pr[page]) for page in corpus)
        if diff < 0.001:
            break
        pr = new_pr
    
    return pr





        
if __name__ == "__main__":
    main()
