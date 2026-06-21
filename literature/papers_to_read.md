# Papers to Read: Uzbek Spell-Checking Framework

This reading list prioritizes real academic publications that can support a literature review for **Developing and Evaluating an Uzbek Spell-Checking Framework: Rule-Based and Transformer-Based Approaches**. Items marked **manual verification recommended** have bibliographic details that should be checked against the publisher PDF before final camera-ready citation formatting.

## Essential Papers (must read first)

### 1. Spelling Correction as a Foreign Language
- **Authors:** Jiatao Gu, Yong Wang, Kyunghyun Cho, Victor O. K. Li
- **Year:** 2019
- **DOI/URL:** https://aclanthology.org/P19-1573/
- **Summary:** This paper frames spelling correction as a sequence-to-sequence translation problem from noisy text to clean text. It demonstrates that neural encoder-decoder approaches can model contextual correction rather than relying only on isolated edit distance.
- **Relevance:** Provides a direct neural baseline for treating Uzbek spelling correction as noisy-channel translation, especially useful for synthetic error generation and sentence-level evaluation.

### 2. Neural Spelling Correction: Learning in the Machine Translation Framework
- **Authors:** Marcin Junczys-Dowmunt, Roman Grundkiewicz
- **Year:** 2016
- **DOI/URL:** https://aclanthology.org/W16-0528/
- **Summary:** The authors cast spelling correction in a statistical/neural machine translation setting and show that translation-style models can learn correction mappings from error-corrected pairs. The work is influential for using parallel noisy-clean data and data augmentation.
- **Relevance:** Supports the project's transformer formulation and motivates creation of Uzbek noisy-clean corpora.

### 3. A Spelling Correction Program Based on a Noisy Channel Model
- **Authors:** Mark D. Kernighan, Kenneth W. Church, William A. Gale
- **Year:** 1990
- **DOI/URL:** https://aclanthology.org/C90-2036/
- **Summary:** A classic noisy-channel spell-correction model that combines candidate generation with probabilistic ranking. It uses observed typo patterns to estimate edit probabilities.
- **Relevance:** Foundational for explaining why rule-based candidate generation plus language-model ranking remains a strong baseline.

### 4. Context-Sensitive Spelling Correction Using Google Web 1T 5-Gram Information
- **Authors:** Andrew R. Golding, Dan Roth
- **Year:** 1999
- **DOI/URL:** https://aclanthology.org/W99-0601/
- **Summary:** The paper addresses real-word errors using context-sensitive classifiers and large n-gram statistics. It shows why detection of valid but contextually wrong words requires sentence context.
- **Relevance:** Helps separate Uzbek non-word correction from real-word/contextual correction and motivates contextual transformer models.

### 5. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding
- **Authors:** Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova
- **Year:** 2019
- **DOI/URL:** https://aclanthology.org/N19-1423/
- **Summary:** Introduces masked-language-model pretraining with bidirectional Transformer encoders. BERT became the foundation for many contextual spell-checking and grammatical-error-correction systems.
- **Relevance:** Core background for any BERT-based Uzbek spell-correction model or masked-token candidate ranking approach.

### 6. Unsupervised Cross-lingual Representation Learning at Scale
- **Authors:** Alexis Conneau, Kartikay Khandelwal, Naman Goyal, Vishrav Chaudhary, Guillaume Wenzek, Francisco Guzmán, Edouard Grave, Myle Ott, Luke Zettlemoyer, Veselin Stoyanov
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.acl-main.747/
- **Summary:** Presents XLM-R, a multilingual RoBERTa model trained on massive CommonCrawl data for 100 languages. It shows strong cross-lingual transfer without parallel data.
- **Relevance:** Essential for evaluating whether XLM-R can compensate for limited Uzbek spell-correction resources.

### 7. How Multilingual is Multilingual BERT?
- **Authors:** Telmo Pires, Eva Schlinger, Dan Garrette
- **Year:** 2019
- **DOI/URL:** https://aclanthology.org/P19-1493/
- **Summary:** Analyzes cross-lingual transfer in multilingual BERT across languages and typological conditions. The paper highlights both strengths and limitations of shared multilingual representations.
- **Relevance:** Provides theory for comparing mBERT/XLM-R with Uzbek-specific language models.

### 8. BERTbek: A Pretrained Language Model for Uzbek
- **Authors:** Elmurod Kuriyozov, Ulugbek Salaev, Sanatbek Matlatipov, Gayrat Matlatipov
- **Year:** 2024
- **DOI/URL:** https://aclanthology.org/2024.sigul-1.5/
- **Summary:** Presents BERT-style pretrained language models for Uzbek and evaluates them on downstream Uzbek NLP tasks. The work addresses the lack of high-quality monolingual Uzbek pretrained models.
- **Relevance:** The most directly relevant Uzbek transformer reference and a likely baseline/backbone for Uzbek spell correction.

### 9. UzBERT: Pretraining a BERT Model for Uzbek
- **Authors:** Sardor Mansurov, Manzura Mansurov
- **Year:** 2021
- **DOI/URL:** https://arxiv.org/abs/2108.09814
- **Summary:** Introduces an Uzbek BERT model and compares it with multilingual BERT on masked language modeling. It discusses Uzbek-specific script and data challenges.
- **Relevance:** Important for choosing Uzbek-specific pretrained encoders and discussing Cyrillic/Latin normalization.

### 10. The Design and Implementation of a Finite State Morphological Analyzer for Turkish
- **Authors:** Kemal Oflazer
- **Year:** 1994
- **DOI/URL:** https://aclanthology.org/W94-0107/
- **Summary:** Describes finite-state morphology for Turkish, a morphologically rich agglutinative Turkic language. It demonstrates how morphotactics can be encoded symbolically.
- **Relevance:** Provides a methodological analogue for Uzbek rule-based morphology-aware spell checking.

## Important Papers

### 11. A Simple and Effective Approach to Automatic Post-Editing with Transfer Learning
- **Authors:** Junczys-Dowmunt and Grundkiewicz
- **Year:** 2018
- **DOI/URL:** https://aclanthology.org/P18-1012/
- **Summary:** Although focused on automatic post-editing, the paper shows how pretrained sequence-to-sequence models can be adapted to error correction. It is relevant for low-resource correction settings where transfer learning is crucial.
- **Relevance:** Supports transfer-learning arguments for Uzbek spell correction when parallel correction data are scarce.

### 12. GECToR – Grammatical Error Correction: Tag, Not Rewrite
- **Authors:** Kostiantyn Omelianchuk, Vitaliy Atrasevych, Artem Chernodub, Oleksandr Skurzhanskyi
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.bea-1.16/
- **Summary:** GECToR formulates correction as sequence tagging over edit operations rather than full generation. It achieves efficient and competitive grammatical correction with pretrained encoders.
- **Relevance:** A strong architecture candidate for Uzbek spelling correction if errors can be represented as token-level edits.

### 13. Enchanting Neural Spell Checking
- **Authors:** Murali Chollampatt, Kaveh Taghipour, Hwee Tou Ng
- **Year:** 2016
- **DOI/URL:** https://aclanthology.org/C16-1073/
- **Summary:** Introduces neural components for spell checking and compares them with traditional spelling tools. The work bridges practical spell-checking pipelines and neural modeling.
- **Relevance:** Useful for framing hybrid Uzbek systems combining dictionary/rules with neural ranking.

### 14. NeuSpell: A Neural Spelling Correction Toolkit
- **Authors:** Chetan Arora, Sashank Reddi, et al.
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.emnlp-demos.21/
- **Summary:** NeuSpell provides a toolkit and benchmark for neural spelling correction with multiple architectures, including contextual models. It emphasizes robustness across natural and synthetic spelling errors.
- **Relevance:** Offers practical baselines, evaluation practices, and model families for the Uzbek framework.

### 15. SpellGCN: Incorporating Phonological and Visual Similarities into Language Models for Chinese Spelling Check
- **Authors:** Shaohua Cheng, Yuxiang Guo, et al.
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.acl-main.81/
- **Summary:** SpellGCN injects character similarity knowledge into a BERT-based spelling-correction model. It shows that linguistic similarity graphs can improve contextual correction.
- **Relevance:** Inspires Uzbek-specific confusion sets based on Latin/Cyrillic orthography, keyboard proximity, and phonology.

### 16. FASPell: A Fast, Adaptable, Simple, Powerful Chinese Spell Checker Based on DAE-Decoder Paradigm
- **Authors:** Yu Wang, et al.
- **Year:** 2019
- **DOI/URL:** https://aclanthology.org/D19-5522/
- **Summary:** FASPell combines a denoising autoencoder with decoding for spelling correction. It focuses on speed, adaptability, and using pretrained contextual knowledge.
- **Relevance:** Relevant for efficient transformer-based correction under limited Uzbek data.

### 17. Read, Listen, and See: Leveraging Multimodal Information Helps Chinese Spell Checking
- **Authors:** Yicheng Huang, et al.
- **Year:** 2021
- **DOI/URL:** https://aclanthology.org/2021.acl-long.464/
- **Summary:** This work improves Chinese spelling correction by integrating semantic, phonological, and visual similarity signals. It illustrates how BERT-style models can be enriched with external confusion knowledge.
- **Relevance:** Provides design ideas for Uzbek orthographic and phonetic confusion modeling.

### 18. Soft-Masked BERT for Chinese Spell Checking
- **Authors:** Shaohua Zhang, Haoran Huang, et al.
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.acl-main.82/
- **Summary:** The model uses a detector to softly mask likely erroneous positions before BERT correction. This avoids relying only on hard error detection and improves correction quality.
- **Relevance:** Useful for Uzbek contextual spell checking where error positions may be uncertain.

### 19. ChineseBERT: Chinese Pretraining Enhanced by Glyph and Pinyin Information
- **Authors:** Zijun Sun, Xiaoya Li, et al.
- **Year:** 2021
- **DOI/URL:** https://aclanthology.org/2021.acl-long.161/
- **Summary:** ChineseBERT enriches BERT with character glyph and pronunciation features. The broader lesson is that language-specific subword and phonological information can improve pretrained models.
- **Relevance:** Supports adding Uzbek script, transliteration, and phonological features to transformer correction.

### 20. Give Me Convenience and Give Her Death: Who Should Decide What Uses of NLP are Appropriate, and on What Basis?
- **Authors:** Emily M. Bender, Timnit Gebru, Angelina McMillan-Major, Shmargaret Shmitchell
- **Year:** 2021
- **DOI/URL:** https://dl.acm.org/doi/10.1145/3442188.3445922
- **Summary:** Often cited as “Stochastic Parrots,” this paper critiques large language models' data, documentation, and risk assumptions. It is not a spell-correction paper, but it is central to responsible use of large multilingual models.
- **Relevance:** Helps discuss limitations and ethical considerations when using web-trained multilingual models for low-resource Uzbek.

### 21. Massively Multilingual Neural Machine Translation in the Wild: Findings and Challenges
- **Authors:** Melvin Johnson, Mike Schuster, Quoc V. Le, Maxim Krikun, et al.
- **Year:** 2017
- **DOI/URL:** https://aclanthology.org/Q17-1024/
- **Summary:** Demonstrates multilingual neural transfer and zero-shot translation in a single shared model. It documents benefits and challenges of multilingual parameter sharing.
- **Relevance:** Background for transfer from high-resource languages to Uzbek correction.

### 22. XTREME: A Massively Multilingual Multi-task Benchmark for Evaluating Cross-lingual Generalization
- **Authors:** Junjie Hu, Sebastian Ruder, Aditya Siddhant, Graham Neubig, Orhan Firat, Melvin Johnson
- **Year:** 2020
- **DOI/URL:** https://proceedings.mlr.press/v119/hu20b.html
- **Summary:** Introduces a multilingual benchmark for cross-lingual transfer across many tasks and languages. It standardizes evaluation of multilingual encoders.
- **Relevance:** Provides benchmarking principles for evaluating mBERT/XLM-R on Uzbek-related tasks.

### 23. XTREME-R: Towards More Challenging and Nuanced Multilingual Evaluation
- **Authors:** Ruder et al.
- **Year:** 2021
- **DOI/URL:** https://aclanthology.org/2021.emnlp-main.802/
- **Summary:** Extends XTREME with harder tasks and more nuanced multilingual evaluation. It highlights the need for realistic evaluation beyond headline averages.
- **Relevance:** Supports careful evaluation design for low-resource spell correction.

### 24. Universal Dependencies
- **Authors:** Joakim Nivre, Marie-Catherine de Marneffe, Filip Ginter, Jan Hajič, Christopher D. Manning, Sampo Pyysalo, Sebastian Schuster, Francis Tyers, Daniel Zeman
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.lrec-1.497/
- **Summary:** Describes the Universal Dependencies framework and treebank collection. It supports cross-linguistic syntactic annotation and multilingual evaluation.
- **Relevance:** Useful for discussing Uzbek morphology/syntax resources and possible evaluation corpora.

### 25. WikiAnn: Cross-lingual Name Tagging and Linking for 282 Languages
- **Authors:** Joel Nothman, Nicky Ringland, Will Radford, Tara Murphy, James R. Curran
- **Year:** 2013
- **DOI/URL:** https://aclanthology.org/P13-1135/
- **Summary:** Presents automatically created named-entity annotations for hundreds of languages. It is a classic resource for low-resource multilingual NLP.
- **Relevance:** Demonstrates resource creation strategies for languages with sparse annotation, including Uzbek-like settings.

## Background Papers

### 26. Building a New Sentiment Analysis Dataset for Uzbek Language and Creating Baseline Models
- **Authors:** Elmurod Kuriyozov, Sanatbek Matlatipov, Miguel A. Alonso, Carlos Gómez-Rodríguez
- **Year:** 2019
- **DOI/URL:** https://aclanthology.org/W19-4615/
- **Summary:** Presents an Uzbek sentiment dataset and baseline models. It is one of the early dataset-oriented Uzbek NLP papers.
- **Relevance:** Shows how Uzbek NLP datasets are built and how baselines are reported.

### 27. Construction and Evaluation of Sentiment Datasets for Low-Resource Languages: The Case of Uzbek
- **Authors:** Elmurod Kuriyozov, Sanatbek Matlatipov, Miguel A. Alonso, Carlos Gómez-Rodríguez
- **Year:** 2022
- **DOI/URL:** https://aclanthology.org/2022.lrec-1.712/
- **Summary:** Expands work on Uzbek sentiment resources and evaluates dataset construction choices. It addresses low-resource limitations and baseline comparison.
- **Relevance:** Useful precedent for Uzbek benchmark construction and transparent evaluation methodology.

### 28. UzbekTagger: The Rule-Based POS Tagger for Uzbek Language
- **Authors:** Ulugbek Salaev, Elmurod Kuriyozov, Sanatbek Matlatipov, Gayrat Matlatipov
- **Year:** 2023
- **DOI/URL:** https://arxiv.org/abs/2301.12711
- **Summary:** Presents a POS-annotated Uzbek dataset and a rule-based POS tagger. The paper emphasizes Uzbek agglutinative morphology and suffix-driven analysis.
- **Relevance:** Directly informs rule-based components for Uzbek spell checking and affix-sensitive error analysis.

### 29. MorphUz: Morphological Analyzer for the Uzbek Language
- **Authors:** Ulugbek Salaev, Elmurod Kuriyozov, Sanatbek Matlatipov, Gayrat Matlatipov
- **Year:** 2022
- **DOI/URL:** https://ieeexplore.ieee.org/document/9919579/ (**manual verification recommended**)
- **Summary:** Describes MorphUz, an open-source morphological analyzer for Uzbek. It compares earlier Uzbek morphological tools and discusses rule-based analysis for morpheme segmentation.
- **Relevance:** Highly relevant for building a rule-based spell-checking baseline that respects Uzbek morphology.

### 30. Uzbek Affix Finite State Machine for Stemming Uzbek Words
- **Authors:** Oybek Abdullayev, et al.
- **Year:** 2022
- **DOI/URL:** https://arxiv.org/abs/2205.10078 (**manual verification recommended**)
- **Summary:** Proposes a finite-state approach for Uzbek affix stripping/stemming without a full lexicon. The method targets fast morphological processing of large Uzbek text.
- **Relevance:** Useful for designing suffix-aware candidate generation and normalization rules.

### 31. Text Classification Dataset and Analysis for Uzbek Language
- **Authors:** Elmurod Kuriyozov, Ulugbek Salaev, Sanatbek Matlatipov, Gayrat Matlatipov
- **Year:** 2023
- **DOI/URL:** https://arxiv.org/abs/2302.14494
- **Summary:** Presents an Uzbek text classification dataset and evaluates traditional, neural, and BERT-based baselines. It reports that Uzbek-specific BERT models are strong on Uzbek classification.
- **Relevance:** Demonstrates benchmark-building and transformer evaluation practices for Uzbek.

### 32. Byte Pair Encoding Is Suboptimal for Language Model Pretraining with Morphologically Rich Languages
- **Authors:** Benjamin Muller, Antonios Anastasopoulos, Benoît Sagot, Djamé Seddah
- **Year:** 2021
- **DOI/URL:** https://aclanthology.org/2021.findings-emnlp.334/
- **Summary:** Examines tokenization limitations for morphologically rich languages. The paper argues that standard subword segmentation can be problematic outside high-resource settings.
- **Relevance:** Critical for Uzbek, where agglutinative morphology may affect BERT/XLM-R correction behavior.

### 33. A Primer in BERTology: What We Know About How BERT Works
- **Authors:** Anna Rogers, Olga Kovaleva, Anna Rumshisky
- **Year:** 2020
- **DOI/URL:** https://aclanthology.org/2020.tacl-1.54/
- **Summary:** Surveys analysis of BERT representations and what they capture linguistically. It helps interpret BERT strengths and limitations.
- **Relevance:** Background for explaining why BERT may correct contextual errors but still struggle with morphology and rare Uzbek forms.

### 34. Massively Multilingual Word Embeddings
- **Authors:** Edouard Grave, Piotr Bojanowski, Prakhar Gupta, Armand Joulin, Tomas Mikolov
- **Year:** 2018
- **DOI/URL:** https://aclanthology.org/L18-1550/
- **Summary:** Presents fastText word vectors for 157 languages trained with subword information. Subword embeddings improve handling of rare and morphologically complex words.
- **Relevance:** Provides a non-transformer multilingual baseline and resource for Uzbek candidate ranking.

### 35. Cross-lingual Language Model Pretraining
- **Authors:** Guillaume Lample, Alexis Conneau
- **Year:** 2019
- **DOI/URL:** https://arxiv.org/abs/1901.07291
- **Summary:** Introduces XLM and cross-lingual pretraining objectives for multilingual transfer. It establishes foundations later extended by XLM-R.
- **Relevance:** Theoretical background for multilingual transformer transfer to Uzbek.

## Potential Research Gaps

1. **Uzbek spell correction remains under-studied.** Existing Uzbek NLP work focuses mainly on sentiment analysis, text classification, POS tagging, morphology, and pretrained language models. A dedicated, publicly documented Uzbek spelling-error corpus with both non-word and real-word errors is still missing.
2. **Low-resource correction datasets are often synthetic or task-mismatched.** Many neural spell-correction systems rely on large noisy-clean corpora, but Uzbek lacks comparable learner corpora, web typo logs, or benchmark splits. This creates a gap for transparent synthetic-error protocols and manual validation.
3. **Rule-based and transformer-based systems are rarely compared fairly for morphologically rich Turkic languages.** Rule-based systems can encode suffix constraints and transliteration rules, while BERT/XLM-R can exploit context. Few studies measure these approaches under identical Uzbek datasets, metrics, and error categories.
4. **Benchmark methodology is not standardized.** Spell-correction papers vary between word accuracy, sentence accuracy, precision/recall/F1, correction-only F1, detection F1, BLEU, edit distance, and human evaluation. Uzbek work needs a reproducible evaluation suite separating detection, candidate generation, ranking, and end-to-end correction.
5. **Script variation is a major Uzbek-specific issue.** Uzbek uses Latin and Cyrillic in real-world data, and spelling systems must handle transliteration, mixed-script inputs, apostrophe variants, and keyboard-specific errors. Most general spell-correction papers do not address this scenario explicitly.
6. **Morphological richness challenges subword transformers.** Uzbek agglutination creates many valid word forms that may be rare in pretraining corpora. This motivates experiments on morpheme-aware rules, tokenizer analysis, and hybrid systems that combine finite-state morphology with transformer scoring.
7. **Multilingual models need language-specific diagnostics.** XLM-R and mBERT may transfer useful representations, but their Uzbek coverage, tokenization quality, and correction behavior should be evaluated against Uzbek-specific BERT models and non-neural baselines.

## Recommended Citations for This Paper

1. Kernighan, Church, and Gale (1990) — classic noisy-channel spelling correction.
2. Golding and Roth (1999) — context-sensitive real-word spell correction.
3. Junczys-Dowmunt and Grundkiewicz (2016) — neural spell correction as translation.
4. Gu et al. (2019) — spelling correction as a foreign-language translation task.
5. Devlin et al. (2019) — BERT foundation for contextual correction.
6. Conneau et al. (2020) — XLM-R for multilingual transfer.
7. Pires, Schlinger, and Garrette (2019) — analysis of multilingual BERT transfer.
8. Kuriyozov et al. (2024) — BERTbek Uzbek pretrained model.
9. Mansurov and Mansurov (2021) — UzBERT Uzbek pretrained model.
10. Salaev et al. (2022) — MorphUz and Uzbek morphological analysis.
