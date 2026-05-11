
import sys
sys.path.append('src')

from preprocessamento import carregar_transacoes
from fp_growth import construir_fp_tree, minerar_padroes
from regras import gerar_regras

def main():
    print("="*60)
    print("TESTE COM AMOSTRA DO DATASET REAL")
    print("="*60)
    
    transacoes_completas = carregar_transacoes('data/vendas_dataset.csv')
    tamanho_amostra = 50
    transacoes = transacoes_completas[:tamanho_amostra]
    print(f"   Usando amostra de {tamanho_amostra} transações para teste")
    
    print("\n2. Exemplo das 3 primeiras transações da amostra:")
    for i, trans in enumerate(transacoes[:3], 1):
        print(f"   {i}: {trans[:5]}...") 
    
    min_sup_absoluto = 2  
    min_confianca = 0.5   
    
    print(f"\n3. Parâmetros do teste:")
    print(f"   Suporte mínimo absoluto: {min_sup_absoluto} transações")
    print(f"   Confiança mínima: {min_confianca * 100}%")
    
    print("\n4. Construindo FP-Tree com a amostra...")
    tree, frequencias = construir_fp_tree(transacoes, min_sup_absoluto)
    
    if tree is None:
        print("   Nenhum item frequente encontrado com esse suporte mínimo!")
        return
    
    print(f"   Itens frequentes encontrados: {len(frequencias)}")
    print("   Itens frequentes (primeiros 10):")
    for i, (item, freq) in enumerate(sorted(frequencias.items(), key=lambda x: x[1], reverse=True)[:10], 1):
        print(f"      {i}. '{item}': {freq} ocorrências")
    
    print("\n5. Minerando padrões frequentes...")
    padroes = minerar_padroes(tree, frequencias, min_sup_absoluto)
    print(f"   Padrões frequentes encontrados: {len(padroes)}")
    
    if padroes:
        print("   Exemplos de padrões frequentes (primeiros 10):")
        for i, (padrao, sup) in enumerate(padroes[:10], 1):
            print(f"      {i}. {padrao}: suporte = {sup}")
    
    print("\n6. Gerando regras de associação...")
    regras = gerar_regras(padroes, transacoes, min_confianca)
    print(f"   Regras geradas: {len(regras)}")
    
    if regras:
        print("\n7. Regras encontradas (ordenadas por Lift):")
        print("-"*70)
        for i, regra in enumerate(regras[:10], 1):
            ant = ', '.join(sorted(regra['antecedente']))
            cons = ', '.join(sorted(regra['consequente']))
            print(f"\n   Regra {i}:")
            print(f"      {{{ant}}} → {{{cons}}}")
            print(f"      Suporte: {regra['suporte']:.4f} ({regra['suporte']*100:.2f}%)")
            print(f"      Confiança: {regra['confianca']:.4f} ({regra['confianca']*100:.2f}%)")
            print(f"      Lift: {regra['lift']:.2f}")
    else:
        print("\n   Nenhuma regra encontrada com a confiança mínima de 50%")
        print("   Tente diminuir o min_confianca ou aumentar o número de transações na amostra")
    
    print("\n" + "="*60)
    print("Fim do teste com amostra do dataset")
    print("="*60)

if __name__ == "__main__":
    main()