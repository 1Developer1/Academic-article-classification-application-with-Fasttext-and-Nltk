import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import fasttext
import fasttext.util
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from text_processing.models import Article  
from sklearn.metrics import precision_score, recall_score



class TextVectorizer:
    def __init__(self, model_path, articles_dir):
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()
        self.model_path = model_path
        self.model = fasttext.load_model(model_path)
        self.articles_dir = articles_dir
        self.article_texts = self._load_articles()

    def _load_articles(self):
        article_texts = []
        for filename in os.listdir(self.articles_dir):
            if filename.endswith(".txt"):
                with open(os.path.join(self.articles_dir, filename), 'r', encoding='utf-8') as file:
                    article_text = file.read()
                    article_texts.append((filename, article_text))  # Dosya adı ve metni birlikte sakla
        return article_texts

    def preprocess_text(self, text):
        tokens = word_tokenize(text)
        clean_tokens = [word.lower() for word in tokens if word.lower() not in self.stop_words and word.lower() not in string.punctuation]
        stemmed_tokens = [self.ps.stem(word) for word in clean_tokens]
        return ' '.join(stemmed_tokens)  

    def get_vector(self, text):
        if self.model:
            return self.model.get_sentence_vector(text)
        else:
            print("Model not loaded!")
            return None

    def get_interest_vectors(self, interests):
        interest_vectors = []
        for interest in interests:
            interest_vector = self.get_vector(interest)
            interest_vectors.append(interest_vector)
        return interest_vectors

    def calculate_similarity(self, interest_vectors,article_vectors):
        average_vector = np.mean(interest_vectors, axis=0)
        similarities = cosine_similarity(np.array([average_vector]), np.array(article_vectors))[0]
        return similarities

    def get_top_n_articles(self, similarities, article_texts, n=5):
        similarities = np.array(similarities)  
        top_indices = similarities.argsort()[-n:][::-1]  
        top_articles = []
        for idx in top_indices:
            filename, content, _ = article_texts[idx]  
            similarity_percentage = similarities[idx] * 100
            top_articles.append((filename, content, similarity_percentage))
        return top_articles

    
    def get_article_vectors(self):
        article_data = []
        for filename, text in self.article_texts:
            processed_text = self.preprocess_text(text)
            vector = self.get_vector(processed_text)
            article_data.append((filename, text, vector))
        return article_data
    
    
    def get_query_vector(self, query):
        processed_query = self.preprocess_text(query)
        query_vector = self.get_vector(processed_query)
        return query_vector
    
    def calculate_query_similarity(self, query_vector, article_vectors):
        similarities = cosine_similarity(np.array([query_vector]), np.array(article_vectors))[0]
        return similarities.tolist()
    
    def save_articles_to_database(self):
        # TextVectorizer sınıfının bir örneği oluşturulur
        articles_dir = "C:/Users/XMG/Desktop/python/Metin İşleme/krapivin-2009-pre-master/krapivin-2009-pre-master/src/all_docs_abstacts_refined/all_docs_abstacts_refined"
        model_path = "C:/Users/XMG/Desktop/python/Metin İşleme/cc.en.300.bin"
        text_processor = TextVectorizer(model_path, articles_dir)
        
        # Makale verileri alınır
        article_data = text_processor.get_article_vectors()
    
        # Her bir makale verisi veritabanına kaydedilir
        for filename, content, vector in article_data:
            # Save each article and its vector to the database
            article = Article(filename=filename, content=content, vector=np.array(vector).tobytes())
            article.save()





