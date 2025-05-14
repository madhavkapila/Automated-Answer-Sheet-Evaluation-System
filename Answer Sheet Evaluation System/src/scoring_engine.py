import os
import pandas as pd
from textblob import TextBlob
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from config.paths import PATHS

class ScoringEngine:
    def __init__(self):
        #Initialize with paths from config
        self.weights = self._load_data('weights')
        self.keywords = self._load_data('keywords')
        self.teacher_answers = self._load_answers('questions')
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def _load_data(self, path_key):
        path = PATHS[path_key]
        if not path or not os.path.exists(path):
            raise FileNotFoundError(f"Path not found: {path}")
        return pd.read_csv(path, encoding='latin1')

    def _load_answers(self, path_key):
        #Specialized answer loader with column renaming
        df = self._load_data(path_key)
        return df.rename(columns={'Question Number': 'Question_Number'})[['Question_Number', 'Answer']]#We are only interested in these two columns
        #Ensure the column names are consistent with the rest of the code

    def _get_weights(self, q_num):
        matches = self.weights[self.weights['question'] == q_num]
        if matches.empty:
            raise KeyError(f"No weights found for Q{q_num}")  # Changed to KeyError
        return matches.iloc[0]

    def _get_model_answer(self, q_num):
        matches = self.teacher_answers[self.teacher_answers['Question_Number'] == q_num]
        if matches.empty:
            raise KeyError(f"No model answer found for Q{q_num}")  # Changed to KeyError
        return matches['Answer'].values[0]

    # def _get_keywords(self, q_num):
    #     #Retrieve and clean keywords
    #     keywords = self.keywords[self.keywords['Question Number'] == q_num].iloc[:, 1:]
    #     return [
    #         str(kw).strip().lower()
    #         for col in keywords.values
    #         for kw in col
    #         if pd.notna(kw) and str(kw).strip()
    #     ]

    def _get_keywords(self, q_num):
        keywords = self.keywords[self.keywords['Question Number'] == q_num].iloc[:, 1:]
        return [
            ' '.join(str(kw).strip().lower().split())
            for col in keywords.values
            for kw in col
            if pd.notna(kw) and str(kw).strip()
        ]


    def calculate_grammar_score(self, text):
        #Calculate grammar score with error normalization
        if not text.strip():
            return 0.0

        blob = TextBlob(text)
        total_words = len(blob.words)
        if total_words == 0:
            return 0.0

        error_count = sum(
            1 for word in blob.words
            if word.spellcheck()[0][0].lower() != word.lower()
        )
        return 1 - (error_count / total_words)

    # def calculate_keyword_score(self, student_answer, q_num):
    #     #Calculate keyword match score
    #     target_keywords = self._get_keywords(q_num)
    #     if not target_keywords:
    #         return 0.0

    #     student_words = student_answer.lower().split()
    #     matches = sum(1 for kw in target_keywords if any(kw in word for word in student_words))
    #     return matches / len(target_keywords)

    def calculate_keyword_score(self, student_answer, q_num):
        target_keywords = self._get_keywords(q_num)
        if not target_keywords:
            return 0.0
    
        # Split student answer into words
        student_words = student_answer.lower().split()
    
        # Convert keywords to word sequences
        keyword_phrases = [kw.split() for kw in target_keywords]
    
        matches = 0
        for phrase in keyword_phrases:
            # Check for phrase using sliding window
            phrase_length = len(phrase)
            found = False
            for i in range(len(student_words) - phrase_length + 1):
                if student_words[i:i+phrase_length] == phrase:
                    found = True
                    break
            if found:
                matches += 1
    
        return matches / len(target_keywords)

    def calculate_semantic_score(self, student_answer, q_num):
        #Calculate semantic similarity score
        model_answer = self._get_model_answer(q_num)
        embeddings = self.model.encode([model_answer, student_answer])
        return cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    def calculate_total_score(self, student_answer, q_num):
        weights = self._get_weights(q_num)
    
        # Already correct - weights are normalized to 0-1 scale
        
        g = self.calculate_grammar_score(student_answer) * (weights['grammarwt']/100)
        k = self.calculate_keyword_score(student_answer, q_num) * (weights['Keywordswt']/100)
        s = self.calculate_semantic_score(student_answer, q_num) * (weights['similarityWt']/100)

        
        print(f'Question no. {q_num}')
        print(f'Grammar Score is {g} out of {weights["grammarwt"]/100.0}')
        print(f'Keyword Score is {k} out of {weights["Keywordswt"]/100.0}')
        print(f'Semantic Score is {s} out of {weights["similarityWt"]/100.0}')

        return (g + k + s)