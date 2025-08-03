import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

csv_path = 'dados/conversas_exportadas.csv'

try:
    df = pd.read_csv(csv_path, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(csv_path, encoding='utf-8-sig')

print("Colunas encontradas:", df.columns.tolist())
if 'texto' not in df.columns:
    raise ValueError("A coluna 'texto' não foi encontrada no CSV. Verifique o nome correto da coluna.")

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['texto'])

joblib.dump(vectorizer, 'dados/vectorizer.pkl')

print("✅ Arquivo vectorizer.pkl gerado com sucesso!")
