import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load models
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Synonyms (minimal + useful)
SYNONYMS = {
    "ml": "machine learning",
    "nlp": "natural language processing",
    "structured query language": "sql",
    "powerbi": "power bi"
}

# Noise words
NOISE_WORDS = {
    "understanding", "strong", "good", "nice",
    "skills", "skill", "experience", "knowledge",
    "requirement", "requirements", "ability",
    "problem", "solve", "working", "real"
}

# Normalize text
def normalize_text(text):
    text = text.lower().replace("-", " ").replace("/", " ")
    for key, value in SYNONYMS.items():
        text = text.replace(key, value)
    return text


# Extract keywords (clean version)
def extract_keywords(text):
    doc = nlp(text)
    keywords = set()

    # Token-level (ONLY meaningful words)
    for token in doc:
        if (
            token.is_alpha
            and not token.is_stop
            and len(token.text) > 2
            and token.pos_ in ["NOUN", "PROPN"]
        ):
            word = token.lemma_.lower()
            word = SYNONYMS.get(word, word)
            keywords.add(word)

    # Phrase-level (noun chunks)
    for chunk in doc.noun_chunks:
        phrase = chunk.text.lower()

        if (
            len(phrase) > 3
            and not any(noise in phrase for noise in NOISE_WORDS)
        ):
            phrase = SYNONYMS.get(phrase, phrase)
            keywords.add(phrase)

    return keywords


# Filter keywords
def filter_keywords(keywords):
    return {
        word for word in keywords
        if len(word) > 3 and word not in NOISE_WORDS
    }


# Semantic similarity
def semantic_similarity(resume, jd):
    embeddings = model.encode([resume, jd])
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]
    return similarity


# Final scoring
def match_score(resume, jd):
    resume = normalize_text(resume)
    jd = normalize_text(jd)

    resume_keywords = filter_keywords(extract_keywords(resume))
    jd_keywords = filter_keywords(extract_keywords(jd))

    match = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords - resume_keywords

    if len(jd_keywords) == 0:
        return 0, match, missing_keywords

    # Keyword score (40%)
    keyword_score = (len(match) / len(jd_keywords)) * 40

    # Skill score (30%)
    important_skills = [
        "python", "sql", "machine learning",
        "pandas", "numpy", "power bi", "data analysis"
    ]

    skill_match = sum(1 for skill in important_skills if skill in resume and skill in jd)
    skill_score = (skill_match / len(important_skills)) * 30

    # Semantic score (30%)
    semantic_score = semantic_similarity(resume, jd) * 30

    final_score = keyword_score + skill_score + semantic_score
    final_score = min(final_score, 100)

    return round(final_score, 2), match, missing_keywords