import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

df = pd.read_csv('dados/conversas_exportadas.csv', encoding='utf-8-sig')

print("Colunas detectadas:", df.columns.tolist())

coluna_texto = [col for col in df.columns if 'texto' in col.lower()]
if not coluna_texto:
    raise ValueError("Coluna 'texto' não foi encontrada. Verifique as colunas do CSV.")
coluna_texto = coluna_texto[0]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df[coluna_texto])

joblib.dump(vectorizer, 'dados/vectorizer.pkl')
print("✅ Arquivo vectorizer.pkl gerado com sucesso!")