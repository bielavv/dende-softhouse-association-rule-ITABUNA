from src.fp_growth import construir_fp_tree, minerar_padroes
from src.regras import gerar_regras

transacoes_teste = [
    ['leite', 'pao', 'ovos'],
    ['leite', 'pao'],
    ['leite', 'manteiga'],
    ['pao', 'manteiga'],
    ['leite', 'pao', 'manteiga'],
    ['leite', 'ovos']
]

print("="*50)
print("TESTE COM CONJUNTO PEQUENO DE DADOS")
print("="*50)

print("\nTransações:")
for i, t in enumerate(transacoes_teste, 1):
    print(f"{i}: {t}")

freq = {}
for t in transacoes_teste:
    for item in t:
        freq[item] = freq.get(item, 0) + 1

print("\nFrequência dos itens:")
for item, count in sorted(freq.items(), key=lambda x: x[1], reverse=True):
    print(f"  {item}: {count} ocorrências")

min_sup = 2 
tree, freq_dict = construir_fp_tree(transacoes_teste, min_sup)

print("\nPadrões frequentes encontrados:")
padroes = minerar_padroes(tree, freq_dict, min_sup)
for padrao, sup in padroes:
    print(f"  {padrao}: suporte = {sup}")

regras = gerar_regras(padroes, transacoes_teste, min_confianca=0.5)
print("\nRegras geradas:")
for r in regras:
    print(f"  {r['antecedente']} → {r['consequente']}")
    print(f"    Sup: {r['suporte']:.2f}, Conf: {r['confianca']:.2f}, Lift: {r['lift']:.2f}")