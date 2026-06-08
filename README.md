# The Unofficial Guide — Columbia CS Course Reviews

## Domain

This project answers questions about Columbia University CS course and professor reviews. I focused on workload, exam style, projects, teaching quality, and practical registration advice. Official course descriptions say what a class covers, but they usually do not explain how students experienced a professor, how rough the exams felt, or what the project workload was actually like.

## Document Sources

All documents are public CULPA course-review pages/API responses collected into `.txt` files.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | COMS W1004 Intro to Computer Science in Java | Public student reviews | `documents/coms-w1004-intro-java.txt`; https://culpa.info/course/3807 |
| 2 | COMS W3134 Data Structures in Java | Public student reviews | `documents/coms-w3134-data-structures.txt`; https://culpa.info/course/4 |
| 3 | COMS W3157 Advanced Programming | Public student reviews | `documents/coms-w3157-advanced-programming.txt`; https://culpa.info/course/4758 |
| 4 | COMS W3203 Discrete Mathematics | Public student reviews | `documents/coms-w3203-discrete-math.txt`; https://culpa.info/course/397 |
| 5 | COMS W4111 Introduction to Databases | Public student reviews | `documents/coms-w4111-databases.txt`; https://culpa.info/course/664 |
| 6 | COMS W4115 Programming Languages and Translators | Public student reviews | `documents/coms-w4115-plt.txt`; https://culpa.info/course/3105 |
| 7 | COMS W4156 Advanced Software Engineering | Public student reviews | `documents/coms-w4156-advanced-software-engineering.txt`; https://culpa.info/course/1616 |
| 8 | COMS W4701 Artificial Intelligence | Public student reviews | `documents/coms-w4701-artificial-intelligence.txt`; https://culpa.info/course/26 |
| 9 | COMS W4771 Machine Learning | Public student reviews | `documents/coms-w4771-machine-learning.txt`; https://culpa.info/course/1921 |
| 10 | COMS E6111 Advanced Database Systems | Public student reviews | `documents/coms-e6111-advanced-database-systems.txt`; https://culpa.info/course/4956 |

The collected corpus contains 140 individual review records across 10 course documents.

## Chunking Strategy

**Chunk size:** 900 characters maximum.

**Overlap:** 150 characters for long reviews that need to be split.

**Why these choices fit your documents:** The source files are review-heavy: each record has a course, professor, review ID, rating, review text, and workload notes. The chunker preserves review boundaries first so a professor/course/workload note stays attached to the student comment it came from. Long reviews are split with overlap and repeated metadata so follow-up chunks still identify the course, professor, source URL, and review ID.

**Preprocessing:** The ingestion step unescapes HTML entities, strips cookie/ad/read-more noise, normalizes whitespace, keeps review text plus workload notes, writes cleaned documents to `data/cleaned_documents/`, and writes chunks to `data/chunks.jsonl`.

**Final chunk count:** 377 chunks. Sanity checks: min length 263, max length 871, 0 chunks missing source metadata.

## Sample Chunks

**1. Source document:** `documents/coms-w3203-discrete-math.txt`

```text
Source: COMS W3203 Discrete Mathematics CULPA reviews
Source URL: https://culpa.info/course/397
Course: COMS W3203 Discrete Mathematics
Professor: Tony Dear
Review ID: 89138
Submitted: 2026-02-13T15:58:26
Rating: 3
Part 1/1
Review text:
Genuinely the hardest class I have ever taken at Columbia. BUT he does curve significantly to compensate for the extra rigor.
You will probably be fighting for your life at some points of this course, which has to happen at some point of one's academic career - this is an ivy after all!
Don't freak out if you have to take this class with Dear - he is very nice, and you will probably learn more than the other section of Discrete.
Workload notes:
2 Midterms and a final. Homework due once every 2 weeks. Rather than individual exams being curved, he curves the end grade.
```

**2. Source document:** `documents/coms-w3157-advanced-programming.txt`

```text
Source: COMS W3157 Advanced Programming CULPA reviews
Source URL: https://culpa.info/course/4758
Course: COMS W3157 Advanced Programming
Professor: Jae Lee
Review ID: 88658
Submitted: 2025-12-28T15:19:28
Rating: 5
Part 1/1
Review text:
The whole class is one long project masterfully broken up into a series of small labs. You go from learning the C language to implementing your own linked list to creating your own server. Super satisfying to do.
Jae just makes the class so interesting, he explains everything super well. MAKE SURE YOU READ THE LECTURE NOTES THOUHG!!! This was my biggest mistake.
Workload notes:
I knew this class was going to be hard, and it was. I didn't work as much as I should have, but probably around 7 hours a week, and then a bunch for exams for cramming. But honestly workload is worth.
```

**3. Source document:** `documents/coms-w4111-databases.txt`

```text
Source: COMS W4111 Introduction to Databases CULPA reviews
Source URL: https://culpa.info/course/664
Course: COMS W4111 Introduction to Databases
Professor: Luis Gravano
Review ID: 89252
Submitted: 2026-03-31T20:20:30
Rating: 4
Part 1/1
Review text:
I really enjoyed the class and Prof. Gravano was really kind. Compared to the experiences of some of my other friends who took the class with other professors, I definitely think this class was really organized. The second half of the course was a bit difficult but it wasn't too bad.
Workload notes:
3 homeworks, 1 midterm, 1 final
```

**4. Source document:** `documents/coms-w4115-plt.txt`

```text
Source: COMS W4115 Programming Languages and Translators CULPA reviews
Source URL: https://culpa.info/course/3105
Course: COMS W4115 Programming Languages and Translators
Professor: Stephen Edwards
Review ID: 79944
Submitted: 2017-04-25T20:20:18
Rating: 4
Part 1/1
Review text:
Professor Edwards is fantastic. He is engaging, funny, and extremely smart. This was a really great class, and I learned a ton. That being said, the project is definitely a ton of work, so start early! The material that you learn in class doesn't help much with the project itself. So, don't worry about starting the project before you feel like you learn the relevant information in class, because you likely will learn the information way after you need to already have applied it to your compiler.
Workload notes:
Midterm, in class final
3 short homeworks
Giant Project
```

**5. Source document:** `documents/coms-w4701-artificial-intelligence.txt`

```text
Source: COMS W4701 Artificial Intelligence CULPA reviews
Source URL: https://culpa.info/course/26
Course: COMS W4701 Artificial Intelligence
Professor: Ansaf Salleb-Aouissi
Review ID: 88071
Submitted: 2025-12-05T18:12:12
Rating: 3
Part 1/1
Review text:
really easy class but too easy where you don’t learn anything. going to lecture felt unproductive since you could watch the lectures in 2x speed. you could get an easy A on exams if you paid attention and woke up on time for exams. felt like i didn’t learn anything important and online videos on youtube covered the concepts in more depth. learned a lot of different concepts but none in enough detail for it to matter. take the class if you want an easy A
Workload notes:
exams 30% hw are both coding and conceptual
```

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`.

**Production tradeoff reflection:** This model is free, local, fast, and good enough for short English review chunks. For a real advising tool, I would benchmark stronger embeddings on a labeled eval set because professor names, course codes, and repeated workload terms can blur together. I would compare retrieval quality against API cost, latency, longer context support, privacy concerns around student reviews, and multilingual support if the corpus grew beyond English. I would also test hybrid lexical + semantic search because exact strings like `COMS W4115`, `OCaml`, and `Jae Lee` matter a lot here.

## Retrieval Test Results

**Query 1:** What do COMS W3203 reviewers say about Tony Dear's exams and curve?

Top returned chunks:
- COMS W3203 / Tony Dear, review 89811, distance 0.408
- COMS W3203 / Tony Dear, review 87237, distance 0.468
- COMS W3203 / Tony Dear, review 89971, distance 0.471
- COMS W3203 / Tony Dear, review 87396, distance 0.473
- COMS W3203 / Tony Dear, review 89138, distance 0.476

Relevance explanation: These chunks are relevant because they all come from Tony Dear's W3203 reviews and discuss exam difficulty, practice/exam mismatch, final average, curve/B+ curve, or homework/exam structure.

**Query 2:** For COMS W4111 Databases, what project technologies or assignments do reviewers mention?

Top returned chunks:
- COMS W4111 / Luis Gravano, review 86646, distance 0.377
- COMS W4111 / Luis Gravano, review 86646, distance 0.395
- COMS W4111 / Kenneth Ross, review 88530, distance 0.396
- COMS W4111 / Donald Ferguson, review 88266, distance 0.398
- COMS W4111 / Donald Ferguson, review 85904, distance 0.406

Relevance explanation: The top Gravano chunks mention SQL databases, schema design, PostgreSQL/database server work, a large semester project, and exams. The Ross chunk is still course-relevant and discusses what students learn from the database course.

**Query 3:** What do COMS W3157 Advanced Programming reviewers say about workload, labs, and exams?

Top returned chunks:
- COMS W3157 / Jae Lee, review 88886, distance 0.338
- COMS W3157 / Jae Lee, review 87915, distance 0.396
- COMS W3157 / Jae Lee, review 86419, distance 0.396
- COMS W3157 / Jae Lee, review 88658, distance 0.409
- COMS W3157 / Jae Lee, review 89207, distance 0.419

Relevance explanation: These chunks are relevant because they are all W3157/Jae Lee chunks and mention labs, exam prep, lecture notes, office hours, and workload. Initial semantic-only retrieval returned a W4156 chunk first; course-code metadata reranking fixed that failure.

## Grounded Generation

**System prompt grounding instruction:** The generator tells the model to answer only from the retrieved review chunks, avoid outside knowledge, say exactly `I don't have enough information on that.` when the chunks are insufficient, use cautious wording such as "reviewers say," and cite factual claims with source IDs like `[S1]`.

**Structural grounding choices:**
- The retriever returns source text, metadata, source label, and distance.
- `generator.py` filters out chunks with distance greater than `0.65` before any Groq call.
- The user prompt formats each chunk as `[S1]`, `[S2]`, etc. with source URL, course, professor, review ID, and chunk text.
- Source attribution is appended in code after the model response, so citations do not depend only on the prompt.
- If no relevant chunks survive the distance cutoff, the system refuses before calling Groq.

## Example Responses

These examples were produced with `python scripts/run_eval.py --mode live` using the real Groq call.

**Grounded response 1**

Query: What do COMS W3203 reviewers say about Tony Dear's exams and curve?

Response: Reviewers say that Tony Dear's exams are difficult [S1, S2, S4]. They note that the exams can be challenging and may require careful thinking and problem-solving [S3]. However, reviewers also mention that the class is graded on a curve [S1, S2, S5], which helps to compensate for the extra rigor of the exams [S5]. The curve is applied to the end grade [S5] or the overall score [S1], with one reviewer mentioning that the curve is around a B+ [S1].

Source attribution:
- [S1] COMS W3203 Discrete Mathematics | Tony Dear | review 89811 | `documents/coms-w3203-discrete-math.txt`; distance=0.408; https://culpa.info/course/397
- [S2] COMS W3203 Discrete Mathematics | Tony Dear | review 87237 | `documents/coms-w3203-discrete-math.txt`; distance=0.468; https://culpa.info/course/397
- [S3] COMS W3203 Discrete Mathematics | Tony Dear | review 89971 | `documents/coms-w3203-discrete-math.txt`; distance=0.471; https://culpa.info/course/397
- [S4] COMS W3203 Discrete Mathematics | Tony Dear | review 87396 | `documents/coms-w3203-discrete-math.txt`; distance=0.473; https://culpa.info/course/397
- [S5] COMS W3203 Discrete Mathematics | Tony Dear | review 89138 | `documents/coms-w3203-discrete-math.txt`; distance=0.476; https://culpa.info/course/397

**Grounded response 2**

Query: What do COMS W4115 PLT reviewers say about the major project and OCaml?

Response: Reviewers say that the project in COMS W4115 PLT is "monstrous" and requires good teammates to decide on features and implement them together [S2]. They also mention that OCaml can be "very frustrating" but will uncover new areas of software development [S2, S3]. One reviewer notes that they didn't fully understand the project they worked on, even the features they implemented, and felt like they "stumbled around in the dark" [S1]. Another reviewer found OCaml to be "super weird and fun" [S3].

Source attribution:
- [S1] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83055 | `documents/coms-w4115-plt.txt`; distance=0.416; https://culpa.info/course/3105
- [S2] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83051 | `documents/coms-w4115-plt.txt`; distance=0.449; https://culpa.info/course/3105
- [S3] COMS W4115 Programming Languages and Translators | Ronghui Gu | review 85512 | `documents/coms-w4115-plt.txt`; distance=0.460; https://culpa.info/course/3105
- [S4] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83055 | `documents/coms-w4115-plt.txt`; distance=0.463; https://culpa.info/course/3105
- [S5] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83051 | `documents/coms-w4115-plt.txt`; distance=0.493; https://culpa.info/course/3105

**Out-of-scope query**

Query: How do I bake sourdough bread?

System response: I don't have enough information on that.

Source attribution: Sources: none (no sufficiently relevant chunks retrieved).

## Query Interface

**Input fields:** A single `Question` textbox.

**Output format:** The app returns an `Answer` markdown panel, a distinct `Sources` markdown panel, and a `Retrieved chunks` markdown panel showing the top chunks, course/professor, distance, source file, and preview. Run with:

```bash
source .venv/bin/activate
python app.py
```

Then open http://127.0.0.1:7860.

**Sample Interaction Transcript**

> **User:** What do COMS W4115 PLT reviewers say about the major project and OCaml?

> **System:** Reviewers say that the project in COMS W4115 PLT is "monstrous" and requires good teammates to decide on features and implement them together [S2]. They also mention that OCaml can be "very frustrating" but will uncover new areas of software development [S2, S3]. One reviewer notes that they didn't fully understand the project they worked on, even the features they implemented, and felt like they "stumbled around in the dark" [S1]. Another reviewer found OCaml to be "super weird and fun" [S3].
>
> Sources:
> - [S1] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83055 | `documents/coms-w4115-plt.txt`; distance=0.416; https://culpa.info/course/3105
> - [S2] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83051 | `documents/coms-w4115-plt.txt`; distance=0.449; https://culpa.info/course/3105
> - [S3] COMS W4115 Programming Languages and Translators | Ronghui Gu | review 85512 | `documents/coms-w4115-plt.txt`; distance=0.460; https://culpa.info/course/3105
> - [S4] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83055 | `documents/coms-w4115-plt.txt`; distance=0.463; https://culpa.info/course/3105
> - [S5] COMS W4115 Programming Languages and Translators | Stephen Edwards | review 83051 | `documents/coms-w4115-plt.txt`; distance=0.493; https://culpa.info/course/3105

## Evaluation Report

Full live eval output is also written to `data/evaluation_results.md`.

| # | Question | Expected answer | Retrieved chunks | Actual system response (summarized) | Accuracy |
|---|----------|-----------------|------------------|-------------------------------------|----------|
| 1 | What do COMS W3203 reviewers say about Tony Dear's exams and curve? | Exams can be difficult or harder than examples/homework, but reviews mention a curve/B+ curve/end-grade curve. | W3203 / Tony Dear reviews 89811, 87237, 89971, 87396, 89138. | Says Dear's exams are difficult/challenging, require careful thinking, and that the class is graded on a curve, including an end-grade or B+ curve. | Accurate |
| 2 | What do COMS W3157 Advanced Programming reviewers say about workload, labs, and exams? | Jae Lee's version is hard but rewarding, lab-heavy, with later labs taking significant time and exams tied to lectures/labs/practice exams. | W3157 / Jae Lee reviews 88886, 87915, 86419, 88658, 89207. | Says Labs 6 and 7 take substantial time, labs should be started early, one review estimates around 7 hours per week plus exam cramming, practice exams matter, the curve helps, and the workload is worth it despite the difficulty. | Accurate |
| 3 | For COMS W4111 Databases, what project technologies or assignments do reviewers mention? | SQL/PostgreSQL database work, schema design, populating data, and building a simple web app around the database, plus exams/homework depending on professor. | W4111 reviews 86646, 86646, 88530, 88266, 85904. | Mentions designing a database for an application, implementing it in SQL, populating data, building a simple web app, homework assignments, and midterm/final exams. | Accurate |
| 4 | What do COMS W4115 PLT reviewers say about the major project and OCaml? | Students learn/use OCaml and complete a large group compiler/language project; several advise choosing a good group and starting early. | W4115 reviews 83055, 83051, 85512, 83055, 83051. | Says the project is "monstrous," good teammates matter, OCaml can be frustrating but useful, one reviewer felt lost in the project, and another found OCaml weird and fun. | Accurate |
| 5 | How do COMS W4701 AI reviewers describe Ansaf Salleb-Aouissi's homework and exams? | Coding/conceptual assignments, dropped lowest grades in one review, and two exams or midterm-style tests. | W4701 / Ansaf reviews 86239, 86239, 83233, 84856, plus one W4701 / Tony Dear chunk. | Says the homework was tedious but useful, coding/conceptual balance was positive, a buggy grading script was criticized, exams were difficult with time pressure and a curve, and the class had 5 coding assignments, 5 conceptual assignments, and two exams. | Partially accurate |

Q5 is marked partial because retrieval found the main Ansaf workload chunk, but the top set still included a weaker Ansaf review and one Tony Dear W4701 chunk. The answer gets the main homework and exam structure right, but it misses the expected dropped-lowest-grade detail and the retrieved context is mixed enough that I would not call it fully accurate.

## Failure Case Analysis

**Question that failed:** What do COMS W3157 Advanced Programming reviewers say about workload, labs, and exams?

**What the system returned before the fix:** Semantic-only retrieval ranked a COMS W4156 Advanced Software Engineering chunk first, even though the query named COMS W3157.

**Root cause tied to a pipeline stage:** This was a retrieval failure. `all-MiniLM-L6-v2` over-weighted shared terms like "advanced," "workload," and "labs" and under-weighted the exact course code. That is a real weakness of pure semantic retrieval in a course-review corpus where many classes share the same vocabulary.

**What changed to fix it:** `retriever.py` now retrieves a wider candidate set and reranks by exact course-code metadata first, exact professor-name metadata second, then semantic distance. `planning.md` documents this implementation update.

**Remaining limitation:** The metadata reranking only helps when the query includes an exact course code or professor name. A vague query like "which database class has the most practical project?" falls back mostly to semantic retrieval, so it can still pull the wrong course or mix undergraduate and graduate database reviews. A production version should add better query clarification or hybrid search for those broad comparison questions.

## Spec Reflection

**One way the spec helped during implementation:** Writing `planning.md` first kept the chunker tied to the actual document structure. Since the corpus was made of reviews, not long essays, the implementation kept course, professor, review ID, rating, review text, and workload notes together in each chunk.

**One way implementation diverged from the spec, and why:** The original retrieval plan was plain semantic top-k retrieval. Testing showed that this could confuse W3157 and W4156, so I added metadata-aware reranking for course codes and professor names. That change was necessary because exact course and professor strings are not small details in this domain; they decide which reviews are relevant.

## AI Usage

1. Planning and source collection: I directed Codex to build the project around Columbia CS course/professor reviews and to proceed without a back-and-forth approval step. Codex wrote the first full `planning.md`, discovered CULPA's public API from the site bundle, selected ten course-review sources, and wrote `scripts/collect_culpa_sources.py`. I reviewed the source list and kept the replacement of the thin COMS W3156 source with richer COMS W3157 evidence.

2. Retrieval implementation: I gave Codex the chunking/retrieval plan and the project requirements. Codex implemented SentenceTransformer + Chroma retrieval and then revised it after testing exposed a real W3157/W4156 retrieval failure. The change I kept was metadata-aware reranking for exact course codes and professor names.

3. Generation and evaluation: I directed Codex to connect Groq, enforce grounded answers, and rerun the evaluation with live output once the key was available. Codex implemented the prompt, refusal path, distance cutoff, source attribution, Gradio UI, and `scripts/run_eval.py`. I used the live eval output in this README and kept Q5 marked partially accurate instead of making the system look better than it was.

## Runbook

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Paste GROQ_API_KEY into .env. Do not commit .env.
python ingest.py
python retriever.py
python scripts/run_eval.py --mode live
python app.py
```

Local app URL: http://127.0.0.1:7860
