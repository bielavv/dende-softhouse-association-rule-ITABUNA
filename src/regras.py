def suporte(conjunto, transacoes):
    if not conjunto:
        return 0
    contagem = 0
    for trans in transacoes:
        if conjunto.issubset(set(trans)):
            contagem += 1
    return contagem / len(transacoes)

def confianca(antecedente, consequente, transacoes):
    ambos = antecedente.union(consequente)
    sup_ambos = suporte(ambos, transacoes)
    sup_ant = suporte(antecedente, transacoes)
    if sup_ant == 0:
        return 0
    return sup_ambos / sup_ant

def lift(antecedente, consequente, transacoes):
    conf = confianca(antecedente, consequente, transacoes)
    sup_conseq = suporte(consequente, transacoes)
    if sup_conseq == 0:
        return 0
    return conf / sup_conseq

def gerar_regras(padroes_frequentes, transacoes, min_confianca=0.6):

    regras = []
    
    for conjunto, sup_conjunto in padroes_frequentes:
        if len(conjunto) < 2:
            continue
        
        itens = list(conjunto)
        for i in range(1, len(itens)):
            from itertools import combinations
            for ant in combinations(itens, i):
                antecedente = set(ant)
                consequente = conjunto - antecedente
                
                conf = confianca(antecedente, consequente, transacoes)
                if conf >= min_confianca:
                    lift_val = lift(antecedente, consequente, transacoes)
                    regras.append({
                        'antecedente': antecedente,
                        'consequente': consequente,
                        'suporte': sup_conjunto / len(transacoes),
                        'confianca': conf,
                        'lift': lift_val
                    })
    
    regras.sort(key=lambda x: x['lift'], reverse=True)
    return regras