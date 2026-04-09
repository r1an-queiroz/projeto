import time


# =========================
# CLASSE PEDIDO
# =========================
class Pedido:
    def __init__(self, id_pedido, nome_cliente, itens, prioridade):
        self.id = id_pedido
        self.nome_cliente = nome_cliente
        self.itens = itens  # lista de itens
        self.prioridade = prioridade  # normal ou urgente

    def quantidade_itens(self):
        return len(self.itens)

    def __str__(self):
        return (
            f"ID: {self.id} | Cliente: {self.nome_cliente} | "
            f"Itens: {self.itens} | Qtd: {self.quantidade_itens()} | "
            f"Prioridade: {self.prioridade}"
        )


# =========================
# FILA FIFO
# =========================
class FilaPedidos:
    def __init__(self):
        self.fila = []

    def enfileirar(self, pedido):
        self.fila.append(pedido)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self.fila.pop(0)
        return None

    def esta_vazia(self):
        return len(self.fila) == 0

    def mostrar_fila(self):
        if self.esta_vazia():
            print("\nFila vazia.")
        else:
            print("\n=== FILA ATUAL ===")
            for pedido in self.fila:
                print(pedido)

    def listar(self):
        return self.fila.copy()


# =========================
# PILHA DE AÇÕES
# =========================
class PilhaHistorico:
    def __init__(self):
        self.pilha = []

    def push(self, acao, pedido):
        self.pilha.append((acao, pedido))

    def pop(self):
        if not self.esta_vazia():
            return self.pilha.pop()
        return None

    def esta_vazia(self):
        return len(self.pilha) == 0

    def mostrar_historico(self):
        if self.esta_vazia():
            print("\nHistórico vazio.")
        else:
            print("\n=== HISTÓRICO DE AÇÕES ===")
            for acao, pedido in reversed(self.pilha):
                print(f"{acao} -> {pedido}")


# =========================
# ÁRVORE BST
# =========================
class NoBST:
    def __init__(self, pedido):
        self.pedido = pedido
        self.esquerda = None
        self.direita = None


class ArvoreBST:
    def __init__(self):
        self.raiz = None

    def inserir(self, pedido):
        self.raiz = self._inserir(self.raiz, pedido)

    def _inserir(self, no, pedido):
        if no is None:
            return NoBST(pedido)

        if pedido.id < no.pedido.id:
            no.esquerda = self._inserir(no.esquerda, pedido)
        elif pedido.id > no.pedido.id:
            no.direita = self._inserir(no.direita, pedido)
        return no

    def buscar(self, id_pedido):
        return self._buscar(self.raiz, id_pedido)

    def _buscar(self, no, id_pedido):
        if no is None:
            return None
        if id_pedido == no.pedido.id:
            return no.pedido
        if id_pedido < no.pedido.id:
            return self._buscar(no.esquerda, id_pedido)
        return self._buscar(no.direita, id_pedido)

    def em_ordem(self):
        resultado = []
        self._em_ordem(self.raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no:
            self._em_ordem(no.esquerda, resultado)
            resultado.append(no.pedido)
            self._em_ordem(no.direita, resultado)

    def pre_ordem(self):
        resultado = []
        self._pre_ordem(self.raiz, resultado)
        return resultado

    def _pre_ordem(self, no, resultado):
        if no:
            resultado.append(no.pedido)
            self._pre_ordem(no.esquerda, resultado)
            self._pre_ordem(no.direita, resultado)

    def pos_ordem(self):
        resultado = []
        self._pos_ordem(self.raiz, resultado)
        return resultado

    def _pos_ordem(self, no, resultado):
        if no:
            self._pos_ordem(no.esquerda, resultado)
            self._pos_ordem(no.direita, resultado)
            resultado.append(no.pedido)


# =========================
# RECURSÃO
# =========================
def contar_pedidos(lista):
    if len(lista) == 0:
        return 0
    return 1 + contar_pedidos(lista[1:])


def busca_recursiva(lista, id_pedido, indice=0):
    if indice >= len(lista):
        return None
    if lista[indice].id == id_pedido:
        return lista[indice]
    return busca_recursiva(lista, id_pedido, indice + 1)


def somar_total_itens(lista, indice=0):
    if indice >= len(lista):
        return 0
    return lista[indice].quantidade_itens() + somar_total_itens(lista, indice + 1)


# =========================
# ORDENAÇÃO
# =========================
def bubble_sort(lista, chave):
    nova_lista = lista.copy()
    n = len(nova_lista)

    for i in range(n):
        for j in range(0, n - i - 1):
            if chave(nova_lista[j]) > chave(nova_lista[j + 1]):
                nova_lista[j], nova_lista[j + 1] = nova_lista[j + 1], nova_lista[j]

    return nova_lista


def quick_sort(lista, chave):
    if len(lista) <= 1:
        return lista.copy()

    pivo = lista[0]
    menores = [x for x in lista[1:] if chave(x) <= chave(pivo)]
    maiores = [x for x in lista[1:] if chave(x) > chave(pivo)]

    return quick_sort(menores, chave) + [pivo] + quick_sort(maiores, chave)


def comparar_ordenacoes(lista, chave):
    inicio_bubble = time.time()
    ordenado_bubble = bubble_sort(lista, chave)
    fim_bubble = time.time()

    inicio_quick = time.time()
    ordenado_quick = quick_sort(lista, chave)
    fim_quick = time.time()

    tempo_bubble = fim_bubble - inicio_bubble
    tempo_quick = fim_quick - inicio_quick

    return ordenado_bubble, ordenado_quick, tempo_bubble, tempo_quick


# =========================
# FUNÇÕES AUXILIARES
# =========================
def reconstruir_bst(lista_pedidos):
    arvore = ArvoreBST()
    for pedido in lista_pedidos:
        arvore.inserir(pedido)
    return arvore


def ler_itens():
    itens = input("Digite os itens do pedido separados por vírgula: ").strip()
    lista_itens = [item.strip() for item in itens.split(",") if item.strip()]
    return lista_itens


def adicionar_pedido(fila, historico, todos_pedidos, arvore):
    try:
        id_pedido = int(input("ID do pedido: "))
    except ValueError:
        print("ID inválido. Digite apenas números.")
        return arvore

    # Verifica se já existe ID
    for pedido in todos_pedidos:
        if pedido.id == id_pedido:
            print("Já existe um pedido com esse ID.")
            return arvore

    nome_cliente = input("Nome do cliente: ").strip()
    itens = ler_itens()
    prioridade = input("Prioridade (normal/urgente): ").strip().lower()

    if prioridade not in ["normal", "urgente"]:
        prioridade = "normal"

    novo_pedido = Pedido(id_pedido, nome_cliente, itens, prioridade)

    fila.enfileirar(novo_pedido)
    historico.push("Pedido adicionado", novo_pedido)
    todos_pedidos.append(novo_pedido)
    arvore.inserir(novo_pedido)

    print("\nPedido adicionado com sucesso!")
    return arvore


def atender_pedido(fila, historico, todos_pedidos):
    pedido = fila.desenfileirar()

    if pedido is None:
        print("\nNão há pedidos na fila.")
        return

    historico.push("Pedido removido", pedido)
    print("\nPedido atendido/removido:")
    print(pedido)


def desfazer_acao(fila, historico, todos_pedidos):
    ultima_acao = historico.pop()

    if ultima_acao is None:
        print("\nNenhuma ação para desfazer.")
        return

    acao, pedido = ultima_acao

    if acao == "Pedido adicionado":
        # remove da fila
        for i, p in enumerate(fila.fila):
            if p.id == pedido.id:
                fila.fila.pop(i)
                break

        # remove da lista geral
        for i, p in enumerate(todos_pedidos):
            if p.id == pedido.id:
                todos_pedidos.pop(i)
                break

        print("\nÚltima ação desfeita: pedido adicionado removido do sistema.")

    elif acao == "Pedido removido":
        fila.fila.insert(0, pedido)
        # garante que já exista em todos_pedidos, então não adiciona novamente
        print("\nÚltima ação desfeita: pedido removido voltou para a fila.")


def mostrar_pedidos(lista):
    if not lista:
        print("\nNenhum pedido encontrado.")
        return

    for pedido in lista:
        print(pedido)


def menu_ordenacao(todos_pedidos):
    if not todos_pedidos:
        print("\nNão há pedidos cadastrados.")
        return

    print("\nOrdenar por:")
    print("1 - Nome do cliente")
    print("2 - Quantidade de itens")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        chave = lambda p: p.nome_cliente.lower()
        criterio = "Nome do cliente"
    elif opcao == "2":
        chave = lambda p: p.quantidade_itens()
        criterio = "Quantidade de itens"
    else:
        print("Opção inválida.")
        return

    bubble, quick, tempo_bubble, tempo_quick = comparar_ordenacoes(todos_pedidos, chave)

    print(f"\n=== BUBBLE SORT ({criterio}) ===")
    mostrar_pedidos(bubble)

    print(f"\n=== QUICK SORT ({criterio}) ===")
    mostrar_pedidos(quick)

    print("\n=== COMPARAÇÃO DE TEMPO ===")
    print(f"Bubble Sort: {tempo_bubble:.10f} segundos")
    print(f"Quick Sort : {tempo_quick:.10f} segundos")

    if tempo_bubble < tempo_quick:
        print("Bubble Sort foi mais rápido.")
    elif tempo_quick < tempo_bubble:
        print("Quick Sort foi mais rápido.")
    else:
        print("Os dois tiveram tempos muito próximos.")


def menu_bst(arvore):
    if arvore.raiz is None:
        print("\nA árvore está vazia.")
        return

    print("\n1 - Buscar pedido por ID")
    print("2 - Mostrar em ordem (in-order)")
    print("3 - Mostrar pré-ordem (pre-order)")
    print("4 - Mostrar pós-ordem (post-order)")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        try:
            id_pedido = int(input("Digite o ID: "))
        except ValueError:
            print("ID inválido.")
            return

        pedido = arvore.buscar(id_pedido)
        if pedido:
            print("\nPedido encontrado:")
            print(pedido)
        else:
            print("\nPedido não encontrado.")

    elif opcao == "2":
        print("\n=== PERCURSO EM ORDEM ===")
        mostrar_pedidos(arvore.em_ordem())

    elif opcao == "3":
        print("\n=== PERCURSO PRÉ-ORDEM ===")
        mostrar_pedidos(arvore.pre_ordem())

    elif opcao == "4":
        print("\n=== PERCURSO PÓS-ORDEM ===")
        mostrar_pedidos(arvore.pos_ordem())

    else:
        print("Opção inválida.")


def menu_recursao(todos_pedidos):
    if not todos_pedidos:
        print("\nNão há pedidos cadastrados.")
        return

    print("\n1 - Contar total de pedidos")
    print("2 - Buscar pedido por ID")
    print("3 - Somar total de itens de todos os pedidos")
    opcao = input("Escolha: ").strip()

    if opcao == "1":
        total = contar_pedidos(todos_pedidos)
        print(f"\nTotal de pedidos: {total}")

    elif opcao == "2":
        try:
            id_pedido = int(input("Digite o ID: "))
        except ValueError:
            print("ID inválido.")
            return

        pedido = busca_recursiva(todos_pedidos, id_pedido)
        if pedido:
            print("\nPedido encontrado:")
            print(pedido)
        else:
            print("\nPedido não encontrado.")

    elif opcao == "3":
        total_itens = somar_total_itens(todos_pedidos)
        print(f"\nTotal de itens em todos os pedidos: {total_itens}")

    else:
        print("Opção inválida.")


# =========================
# MENU PRINCIPAL
# =========================
def main():
    fila = FilaPedidos()
    historico = PilhaHistorico()
    todos_pedidos = []
    arvore = ArvoreBST()

    while True:
        print("\n" + "=" * 45)
        print(" SISTEMA DE GERENCIAMENTO DE PEDIDOS ")
        print("=" * 45)
        print("1 - Adicionar pedido")
        print("2 - Atender pedido")
        print("3 - Mostrar fila")
        print("4 - Buscar / Percursos BST")
        print("5 - Ordenar pedidos")
        print("6 - Desfazer ação")
        print("7 - Funções recursivas")
        print("8 - Mostrar histórico")
        print("9 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            arvore = adicionar_pedido(fila, historico, todos_pedidos, arvore)

        elif opcao == "2":
            atender_pedido(fila, historico, todos_pedidos)

        elif opcao == "3":
            fila.mostrar_fila()

        elif opcao == "4":
            arvore = reconstruir_bst(todos_pedidos)
            menu_bst(arvore)

        elif opcao == "5":
            menu_ordenacao(todos_pedidos)

        elif opcao == "6":
            desfazer_acao(fila, historico, todos_pedidos)
            arvore = reconstruir_bst(todos_pedidos)

        elif opcao == "7":
            menu_recursao(todos_pedidos)

        elif opcao == "8":
            historico.mostrar_historico()

        elif opcao == "9":
            print("\nSaindo do sistema...")
            break

        else:
            print("\nOpção inválida. Tente novamente.")


# =========================
# EXECUÇÃO
# =========================
if __name__ == "__main__":
    main()