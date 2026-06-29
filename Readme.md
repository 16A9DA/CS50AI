A parser is a system that analyzes the grammatical structure of a sentence by breaking it into components like nouns, verbs, and phrases.
Attention is a mechanism in neural networks that allows the model to focus on the most relevant words in an input when making predictions.
Together, parsers capture structure explicitly, while attention learns it implicitly from data.

---

## Attention analysis :
---
# Attention Head Analysis (BERT)

This section analyzes the behavior of different attention heads in a Transformer-based model (BERT). Each attention head learns to focus on different linguistic patterns such as syntax, word relationships, and sentence structure.

---

## Layer 8, Head 3

This attention head focuses on **verb–object relationships**, where verbs attend strongly to the words they act upon.

### Example Sentences:
- “She opened the **door**.”
- “They built a **house**.”

In both examples, the verb (“opened”, “built”) strongly attends to its corresponding object noun.

---

## Layer 10, Head 7

This attention head focuses on **sentence structure and punctuation**, helping the model understand sentence boundaries.

### Example Sentences:
- “Hello, how are you **?**”
- “I went home **.** Then I slept.”

