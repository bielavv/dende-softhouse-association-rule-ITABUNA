import pandas as pd
import re
import os

def limpar_item(item):
    
    if not isinstance(item, str):
        return ""
    
    palavras_remover = [
        'MIC', 'KIDS', 'BABY', 'FEM', 'MASC', 'UNISSEX', 'TAG', 'PARES',
        'NO', 'COM', 'C', 'DE', 'A', 'E', 'O', 'DA', 'DO', 'DAS', 'DOS',
        'PIMPOLHO', 'LA', 'MAYARA', 'LUZIANE', 'MICOL', 'DENGUINHO',
        'MINASREY', 'SELENE', 'DOM', 'MATHEUS', 'HAOS', 'MARANDS',
        'ITALICO', 'SERGIO', 'MODAS', 'DIFERENTE', 'MONTANHA', 'RUSSA'
    ]
    
    item = re.sub(r'[0-9]+', '', item)
    
    for palavra in palavras_remover:
        item = re.sub(rf'\b{palavra}\b', '', item, flags=re.IGNORECASE)
    
    item = re.sub(r'[^\w\s]', '', item)
    item = re.sub(r'\s+', ' ', item).strip()
    
    return item.lower()

def carregar_transacoes(caminho_arquivo=None):
    
    if caminho_arquivo is None:

        possiveis_caminhos = [
            "data/vendas_dataset.csv",
            "../data/vendas_dataset.csv",
            "../../data/vendas_dataset.csv",
            os.path.join(os.path.dirname(__file__), "../data/vendas_dataset.csv")
        ]
        
        for caminho in possiveis_caminhos:
            if os.path.exists(caminho):
                caminho_arquivo = caminho
                break
        
        if caminho_arquivo is None:
            raise FileNotFoundError("Não foi possível encontrar o arquivo vendas_dataset.csv")
    
    print(f"Carregando arquivo: {caminho_arquivo}")
    df = pd.read_csv(caminho_arquivo)
    transacoes = []
    transacoes_vazias = 0
    
    for _, row in df.iterrows():
        descricao = str(row['descricao_produtos'])
        
        if 'sem referencia' in descricao.lower():
            transacoes_vazias += 1
            continue

        itens_brutos = descricao.split(';')
        
        itens_limpos = []
        for item in itens_brutos:
            item_limpo = limpar_item(item)
            if len(item_limpo) > 2: 
                itens_limpos.append(item_limpo)
        
        itens_unicos = list(set(itens_limpos))
        
        if itens_unicos:
            transacoes.append(itens_unicos)
    
    print(f"Total de transações carregadas: {len(transacoes)}")
    print(f"Transações ignoradas (sem produto válido): {transacoes_vazias}")
    
    return transacoes