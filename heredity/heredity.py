import csv
import itertools
import sys

PROBS = {
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        2: {
            True: 0.65,
            False: 0.35
        },
        1: {
            True: 0.56,
            False: 0.44
        },
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    "mutation": 0.01
}

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    names = set(people)
    for have_trait in powerset(names):
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    normalize(probabilities)

    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")

def load_data(filename):
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data

def powerset(s):
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

def joint_probability(people, one_gene, two_genes, have_trait):
    prob = 1.0
    for person in people:
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        mother = people[person]["mother"]
        father = people[person]["father"]
        if mother is None and father is None:
            gene_prob = PROBS["gene"][gene_count]
        else:
            if mother in two_genes:
                m_count = 2
            elif mother in one_gene:
                m_count = 1
            else:
                m_count = 0
            if father in two_genes:
                f_count = 2
            elif father in one_gene:
                f_count = 1
            else:
                f_count = 0

            def inherit_prob(parent_count):
                if parent_count == 0:
                    return PROBS["mutation"]
                elif parent_count == 1:
                    return 0.5
                else:
                    return 1 - PROBS["mutation"]

            p_from_mother = inherit_prob(m_count)
            p_from_father = inherit_prob(f_count)

            if gene_count == 0:
                gene_prob = (1 - p_from_mother) * (1 - p_from_father)
            elif gene_count == 1:
                gene_prob = p_from_mother * (1 - p_from_father) + (1 - p_from_mother) * p_from_father
            else:
                gene_prob = p_from_mother * p_from_father

        trait_prob = PROBS["trait"][gene_count][person in have_trait]

        prob *= gene_prob * trait_prob

    return prob

def update(probabilities, one_gene, two_genes, have_trait, p):
    for person in probabilities:
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0
        probabilities[person]["gene"][gene_count] += p

        has_trait = person in have_trait
        probabilities[person]["trait"][has_trait] += p

def normalize(probabilities):
    for person in probabilities:
        gene_total = sum(probabilities[person]["gene"].values())
        if gene_total > 0:
            for gene_count in probabilities[person]["gene"]:
                probabilities[person]["gene"][gene_count] /= gene_total

        trait_total = sum(probabilities[person]["trait"].values())
        if trait_total > 0:
            for trait_val in probabilities[person]["trait"]:
                probabilities[person]["trait"][trait_val] /= trait_total

if __name__ == "__main__":
    main()