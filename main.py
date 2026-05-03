import sys
sys.path.append('src')

from preprocessamento import carregar_transacoes
from fp_growth import construir_fp_tree, minerar_padroes
from regras import gerar_regras

def main():
    print("="*60)
    print("FP-GROWTH - REGRAS DE ASSOCIAÇÃO")
    print("Equipe: Itabuna")
    print("="*60)
    
    print("\n1. Carregando transações...")
    transacoes = carregar_transacoes('data/vendas_dataset.csv')
    print(f"   Total: {len(transacoes)} transações válidas")
    
    min_sup_absoluto = int(len(transacoes) * 0.005)  # 0.5%
    min_confianca = 0.3
    
    print(f"\n2. Parâmetros:")
    print(f"   Suporte mínimo: {min_sup_absoluto} transações (0.5%)")
    print(f"   Confiança mínima: {min_confianca * 100}%")
    
    print("\n3. Construindo FP-Tree...")
    tree, frequencias = construir_fp_tree(transacoes, min_sup_absoluto)
    
    if tree is None:
        print("   Nenhum item frequente encontrado!")
        return
    
    print(f"   Itens frequentes encontrados: {len(frequencias)}")
    
    print("\n4. Minerando padrões frequentes...")
    padroes = minerar_padroes(tree, frequencias, min_sup_absoluto)
    print(f"   Padrões frequentes encontrados: {len(padroes)}")
    
    print("\n5. Gerando regras de associação...")
    regras = gerar_regras(padroes, transacoes, min_confianca)
    print(f"   Regras geradas: {len(regras)}")
    
    print("\n6. Top 20 regras (por Lift):")
    print("-"*80)
    
    for i, regra in enumerate(regras[:20], 1):
        ant = ', '.join(sorted(regra['antecedente']))
        cons = ', '.join(sorted(regra['consequente']))
        print(f"{i:2d}. {{{ant}}} → {{{cons}}}")
        print(f"    Sup: {regra['suporte']:.4f} | Conf: {regra['confianca']:.4f} | Lift: {regra['lift']:.2f}")
        print()
    
    with open('regras_encontradas.txt', 'w', encoding='utf-8') as f:
        f.write("REGRAS DE ASSOCIAÇÃO - FP-GROWTH\n")
        f.write("="*60 + "\n\n")
        for regra in regras:
            ant = ', '.join(sorted(regra['antecedente']))
            cons = ', '.join(sorted(regra['consequente']))
            f.write(f"{{{ant}}} → {{{cons}}}\n")
            f.write(f"Suporte: {regra['suporte']:.4f}\n")
            f.write(f"Confiança: {regra['confianca']:.4f}\n")
            f.write(f"Lift: {regra['lift']:.2f}\n")
            f.write("-"*40 + "\n")
    
    print("\n Regras salvas em 'regras_encontradas.txt'")

if __name__ == "__main__":
    main()