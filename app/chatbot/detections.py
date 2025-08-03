from transformers import pipeline
from deep_translator import GoogleTranslator
from app.modelos_carregados import modelo_tfidf, vectorizer_tfidf, modelo_semantico, embedder, modelo_spacy
from scipy.sparse import csr_matrix  

# Pipeline de emoção carregado
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

def detectar_emocao(mensagem: str) -> str:
    """Detecta a emoção da mensagem traduzindo para o inglês e usando modelo pré-treinado."""
    try:
        print("[INFO] Iniciando detecção de emoção...")
        mensagem_en = GoogleTranslator(source='auto', target='en').translate(mensagem)
        print(f"[INFO] Mensagem traduzida para inglês: {mensagem_en}")
        
        resultado = emotion_classifier(mensagem_en)
        return resultado[0][0]['label']
    except Exception as e:
        print(f"[ERRO detectar_emocao] {e}")
        return "Desconhecida"

def detectar_distorcao(texto: str, modo: str = "combinado", limiar: float = 0.6) -> str:
    """
    Detecta distorção cognitiva com base no modo:
    - 'semantico': Usa Sentence-BERT + Regressão Logística
    - 'tfidf': Usa TF-IDF + Regressão Logística
    - 'combinado': Usa semântico, depois spaCy, depois heurística
    """
    try:
        texto = texto.strip().lower()
        
        if modo == "semantico":
            if modelo_semantico is None or embedder is None:
                return "Modelo semântico indisponível"
            embedding = embedder.encode([texto])
            proba = modelo_semantico.predict_proba(embedding)[0]
            if max(proba) < limiar:
                return "Desconhecida"
            return modelo_semantico.classes_[proba.argmax()]
        
        elif modo == "tfidf":
            if modelo_tfidf is None or vectorizer_tfidf is None:
                return "Modelo TF-IDF indisponível"
            resultado = modelo_tfidf.predict([texto])[0]
            proba = modelo_tfidf.predict_proba([texto])[0]
            if max(proba) < limiar:
                return "Desconhecida"
            return resultado
        
        elif modo == "combinado":
            # 1. Semântico
            if modelo_semantico and embedder:
                embedding = embedder.encode([texto])
                proba = modelo_semantico.predict_proba(embedding)[0]
                if max(proba) >= limiar:
                    return modelo_semantico.classes_[proba.argmax()]
            
            # 2. spaCy
            if modelo_spacy:
                doc = modelo_spacy(texto)
                acima = {k: v for k, v in doc.cats.items() if v >= limiar}
                if acima:
                    mais_provavel = max(acima, key=acima.get)
                    return mais_provavel
            
            # 3. Heurística
            heuristica = detectar_distorcao_heuristica(texto)
            if heuristica:
                return heuristica
            
            return "Desconhecida"

        else:
            return "Modo inválido"
    
    except Exception as e:
        print(f"[ERRO detectar_distorcao] {e}")
        return "Desconhecida"

def detectar_distorcao_heuristica(texto: str) -> str:
    # Exemplo simples (você pode melhorar com lógica NLP)
    heuristicas = {
        "sempre": "generalização",
        "nunca": "pensamento tudo ou nada",
        "ninguém gosta": "leitura mental",
        "culpa é minha": "personalização",
    }
    for chave, distorcao in heuristicas.items():
        if chave in texto.lower():
            return distorcao
    return None
 