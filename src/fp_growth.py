class FPNode:

    def __init__(self, item, parent):
        self.item = item          
        self.parent = parent     
        self.children = {}       
        self.count = 1           
        self.next = None 

class FPTree:

    def __init__(self):
        self.root = FPNode(None, None)  
        self.header_table = {}         
    
    def inserir_transacao(self, transacao, contagem=1):

        node_atual = self.root
        
        for item in transacao:
            if item in node_atual.children:
                node_atual.children[item].count += contagem
                node_atual = node_atual.children[item]
            else:
  
                novo_node = FPNode(item, node_atual)
                node_atual.children[item] = novo_node
                node_atual = novo_node
                self._adicionar_header_table(item, novo_node)
    
    def _adicionar_header_table(self, item, node):
        if item in self.header_table:
            current = self.header_table[item]
            while current.next:
                current = current.next
            current.next = node
        else:
            self.header_table[item] = node        

def ordenar_por_frequencia(transacao, frequencias):

    return sorted(transacao, key=lambda x: frequencias[x], reverse=True)

def construir_fp_tree(transacoes, min_sup):

    frequencias = {}
    for trans in transacoes:
        for item in trans:
            frequencias[item] = frequencias.get(item, 0) + 1
    
    frequencias = {k: v for k, v in frequencias.items() if v >= min_sup}
    
    if not frequencias:
        return None, None
    
    transacoes_filtradas = []
    for trans in transacoes:
        trans_filtrada = [item for item in trans if item in frequencias]
        if trans_filtrada:
            trans_filtrada.sort(key=lambda x: frequencias[x], reverse=True)
            transacoes_filtradas.append(trans_filtrada)
    
    tree = FPTree()
    for trans in transacoes_filtradas:
        tree.inserir_transacao(trans)
    
    return tree, frequencias

def minerar_padroes(tree, frequencias, min_sup, prefixo=None):

    if prefixo is None:
        prefixo = set()
    
    padroes = []
    
    itens_ordenados = sorted(frequencias.keys(), key=lambda x: frequencias[x])
    
    for item in itens_ordenados:

        novo_padrao = prefixo.union({item})
        suporte = frequencias[item]
        padroes.append((novo_padrao, suporte))
        
        arvore_condicional = construir_arvore_condicional(tree, item, min_sup)
        
        if arvore_condicional:

            padroes.extend(minerar_padroes(
                arvore_condicional['tree'],
                arvore_condicional['freq'],
                min_sup,
                novo_padrao
            ))
    
    return padroes

def construir_arvore_condicional(tree, item, min_sup):

    caminhos = []
    node = tree.header_table.get(item)
    
    while node:
        caminho = []
        count = node.count
        node_atual = node.parent
        
        while node_atual and node_atual.item is not None:
            caminho.append(node_atual.item)
            node_atual = node_atual.parent
        
        if caminho:
            caminhos.append((caminho, count))
        
        node = node.next
    
    if not caminhos:
        return None
    
    novas_transacoes = []
    freq_condicional = {}
    
    for caminho, count in caminhos:
        for _ in range(count):

            novo_caminho = caminho.copy()
            novas_transacoes.append(novo_caminho)
            for item_caminho in novo_caminho:
                freq_condicional[item_caminho] = freq_condicional.get(item_caminho, 0) + 1
    
    freq_condicional = {k: v for k, v in freq_condicional.items() if v >= min_sup}
    
    if not freq_condicional:
        return None
    
    novas_transacoes_filtradas = []
    for trans in novas_transacoes:

        trans_filtrada = [item for item in trans if item in freq_condicional]
        if trans_filtrada:

            trans_filtrada.sort(key=lambda x: freq_condicional[x], reverse=True)
            novas_transacoes_filtradas.append(trans_filtrada)
    
    if not novas_transacoes_filtradas:
        return None
    

    nova_tree = FPTree()
    for trans in novas_transacoes_filtradas:
        if trans:
            nova_tree.inserir_transacao(trans)
    
    return {'tree': nova_tree, 'freq': freq_condicional}
