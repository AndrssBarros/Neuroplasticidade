import os
from pathlib import Path
import joblib
from transformers import pipeline
import spacy
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = os.path.join(BASE_DIR, "output", "model-best")

try:
    modelo_spacy = spacy.load(MODEL_PATH)
except Exception as e:
    print(f"[ERRO] Não foi possível carregar modelo_spacy: {e}")
    modelo_spacy = None

VECTORIZER_TFIDF_PATH = BASE_DIR / 'dados' / 'vectorizer_distorcao.pkl'
MODELO_TFIDF_PATH = BASE_DIR / 'dados' / 'modelo_distorcao.joblib'
MODELO_SEMANTICO_PATH = BASE_DIR / 'dados' / 'classificador_distorcao_semantico.pkl'
EMBEDDING_MODEL_PATH = BASE_DIR / 'dados' / 'modelo_bert_distorcao'

modelo_tfidf = joblib.load(MODELO_TFIDF_PATH) if os.path.exists(MODELO_TFIDF_PATH) else None
vectorizer_tfidf = joblib.load(VECTORIZER_TFIDF_PATH) if os.path.exists(VECTORIZER_TFIDF_PATH) else None
modelo_semantico = joblib.load(MODELO_SEMANTICO_PATH) if os.path.exists(MODELO_SEMANTICO_PATH) else None

try:
    embedder = SentenceTransformer(str(EMBEDDING_MODEL_PATH))
except Exception as e:
    print(f"[ERRO] Ao carregar embedder: {e}")
    embedder = None

try:
    emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)
except Exception as e:
    print(f"[ERRO] Falha ao carregar emotion_classifier: {e}")
    emotion_classifier = None
