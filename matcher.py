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
def match_score(resume, job_profile):
    # Normalize resume
    resume = normalize_text(resume)

    # Extract resume keywords
    resume_keywords = filter_keywords(extract_keywords(resume))

    # Extract job profile fields
    job_skills = set([normalize_text(s) for s in job_profile.get("skills", [])])
    job_keywords = set([normalize_text(k) for k in job_profile.get("keywords", [])])
    job_responsibilities = set([normalize_text(r) for r in job_profile.get("responsibilities", [])])

    # Combine all job requirements
    jd_keywords = filter_keywords(job_skills | job_keywords | job_responsibilities)

    # Match + Missing
    match = resume_keywords.intersection(jd_keywords)
    missing_keywords = jd_keywords - resume_keywords

    if len(jd_keywords) == 0:
        return 0, match, missing_keywords

    # Keyword Score (40%)
    keyword_score = (len(match) / len(jd_keywords)) * 40

    # Skill Score (30%)
    important_skills = [
        "python", "sql", "machine learning",
        "pandas", "numpy", "power bi", "data analysis"
    ]

    skill_match = sum(
        1 for skill in important_skills
        if skill in resume and skill in " ".join(job_skills)
    )

    skill_score = (skill_match / len(important_skills)) * 30

    # Semantic Score (30%)
    job_text = " ".join(list(job_skills) + list(job_keywords) + list(job_responsibilities))
    semantic_score_val = semantic_similarity(resume, job_text) * 30

    # Final Score
    final_score = keyword_score + skill_score + semantic_score_val
    final_score = min(final_score, 100)

    return round(final_score, 2), match, missing_keywords