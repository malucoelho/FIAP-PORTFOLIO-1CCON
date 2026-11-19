"""Neighborhood Action Dashboard - protótipo textual (Fases 1, 2 e 3).
Dados 100% fictícios, sem informação pessoal."""
from collections import deque

CATEGORIAS = ["iluminação", "acessibilidade", "limpeza", "espaços coletivos"]
STATUS = ["aberta", "em análise", "concluída"]
# Significado: aberta = registrada, ainda não examinada;
# em análise = equipe examinando; concluída = demanda encerrada.
DIA_ATUAL = 10  # dia simulado

# id, categoria, descrição, bairro, local genérico, dia abertura, status, dia conclusão
DADOS = [
    ("001", "iluminação", "Poste apagado", "Centro", "Praça Central", 1, "concluída", 6),
    ("002", "iluminação", "Lâmpada piscando", "Jardim Norte", "Av. das Flores", 2, "em análise", None),
    ("003", "acessibilidade", "Rampa sem acabamento", "Centro", "Calçada da escola", 2, "concluída", 8),
    ("004", "limpeza", "Lixo acumulado", "Vila Sul", "Esquina da Rua 5", 3, "aberta", None),
    ("005", "espaços coletivos", "Banco quebrado", "Jardim Norte", "Praça das Flores", 3, "em análise", None),
    ("006", "acessibilidade", "Falta de piso tátil", "Vila Sul", "Ponto de ônibus", 4, "aberta", None),
    ("007", "limpeza", "Bueiro entupido", "Centro", "Rua do Comércio", 4, "concluída", 9),
    ("008", "iluminação", "Trecho sem iluminação", "Vila Sul", "Ciclovia", 5, "aberta", None),
    ("009", "espaços coletivos", "Grama alta", "Centro", "Praça Central", 5, "em análise", None),
    ("010", "limpeza", "Caçamba cheia", "Jardim Norte", "Feira livre", 6, "aberta", None),
    ("011", "acessibilidade", "Calçada irregular", "Jardim Norte", "Av. das Flores", 7, "em análise", None),
    ("012", "espaços coletivos", "Playground enferrujado", "Vila Sul", "Parquinho", 8, "aberta", None),
    ("013", "", "Buraco na rua", "Centro", "Rua do Comércio", 8, "aberta", None),  # inválido (sem categoria)
    ("014", "iluminação", "Poste inclinado", "Centro", "Praça Central", 9, "aberta", None),
]

# ---------- Estruturas de dados ----------
ocorrencias = []        # LISTA: todas as ocorrências válidas (percorrer/listar)
por_id = {}             # DICIONÁRIO: acesso direto por código
fila_nao_examinadas = deque()  # FILA (FIFO): abertas, por ordem de registro
pilha_eventos = []      # PILHA (LIFO): últimas atualizações (topo = fim)
historico = []          # lista com todo o histórico
hierarquia = {}         # bairro -> categoria -> [códigos]
rejeitadas = []         # registros inconsistentes


# ---------- Validação ----------
def validar(reg, novo=True):
    """Retorna lista de erros. Regras booleanas (AND/OR/NOT):
    - inválido se NOT categoria OR categoria fora do padrão
    - inválido se NOT descrição OR NOT local
    - código duplicado só importa em cadastro novo (novo AND código em por_id)"""
    erros = []
    if not reg["categoria"]:
        erros.append("categoria ausente")
    elif reg["categoria"] not in CATEGORIAS:
        erros.append("categoria desconhecida")
    if not reg["descricao"] or not reg["local"] or not reg["bairro"]:
        erros.append("descrição, bairro ou local ausente")
    if reg["status"] not in STATUS:
        erros.append("situação desconhecida")
    if novo and reg["id"] in por_id:
        erros.append("código já existe")
    return erros


def registrar_evento(cod, de, para, dia):
    ev = {"id": cod, "de": de, "para": para, "dia": dia}
    historico.append(ev)
    pilha_eventos.append(ev)  # push


def indexar(reg):
    ocorrencias.append(reg)
    por_id[reg["id"]] = reg
    hierarquia.setdefault(reg["bairro"], {}).setdefault(reg["categoria"], []).append(reg["id"])


def carregar():
    for cod, cat, desc, bairro, local, ab, st, conc in DADOS:
        reg = {"id": cod, "categoria": cat, "descricao": desc, "bairro": bairro,
               "local": local, "abertura": ab, "status": st, "conclusao": conc}
        erros = validar(reg)
        if erros:
            rejeitadas.append((cod, erros))
            continue
        indexar(reg)
        if st == "aberta":
            fila_nao_examinadas.append(cod)
        else:  # histórico simulado
            registrar_evento(cod, "aberta", "em análise", ab + 2)
            if st == "concluída":
                registrar_evento(cod, "em análise", "concluída", conc)
    # ordena o histórico inicial por dia, para a pilha ficar em ordem cronológica
    historico.sort(key=lambda ev: ev["dia"])
    pilha_eventos[:] = historico


# ---------- Funções de interface ----------
def listar(lista):
    if not lista:
        print("Nenhuma ocorrência encontrada.")
        return
    print(f"{'COD':<5}{'CATEGORIA':<19}{'LOCAL':<22}{'STATUS'}")
    for r in lista:
        print(f"{r['id']:<5}{r['categoria']:<19}{r['local']:<22}{r['status']}")


def buscar():
    cod = input("Código: ").strip().zfill(3)
    r = por_id.get(cod)
    if r is None:
        print("Registro não encontrado.")
    else:
        for k, v in r.items():
            print(f"  {k}: {v}")


def filtrar():
    cat = input("Categoria (Enter p/ todas): ").strip().lower()
    st = input("Status (Enter p/ todos): ").strip().lower()
    if cat and cat not in CATEGORIAS or st and st not in STATUS:
        print("Filtro inválido.")
        return
    res = []
    for r in ocorrencias:
        if (not cat or r["categoria"] == cat) and (not st or r["status"] == st):
            res.append(r)
    listar(res)


def cadastrar():
    prox = str(max([int(c) for c in [d[0] for d in DADOS]] + [int(r["id"]) for r in ocorrencias]) + 1).zfill(3)
    reg = {"id": prox,
           "categoria": input(f"Categoria {CATEGORIAS}: ").strip().lower(),
           "descricao": input("Descrição: ").strip(),
           "bairro": input("Bairro (fictício): ").strip(),
           "local": input("Local genérico: ").strip(),
           "abertura": DIA_ATUAL, "status": "aberta", "conclusao": None}
    erros = validar(reg)
    if erros:
        print("Cadastro recusado:", "; ".join(erros))
        return
    indexar(reg)
    fila_nao_examinadas.append(prox)
    print(f"Ocorrência {prox} cadastrada.")


def mudar_status(cod, novo):
    r = por_id.get(cod)
    if r is None:
        print("Registro não encontrado.")
        return
    if novo not in STATUS:
        print("Situação desconhecida.")
        return
    ordem = STATUS.index
    if not (ordem(novo) > ordem(r["status"])):  # NOT avançar
        print("Mudança inválida: só é possível avançar a situação.")
        return
    if r["status"] == "aberta" and cod in fila_nao_examinadas:
        fila_nao_examinadas.remove(cod)
    registrar_evento(cod, r["status"], novo, DIA_ATUAL)
    r["status"] = novo
    if novo == "concluída":
        r["conclusao"] = DIA_ATUAL
    print(f"Ocorrência {cod} agora está '{novo}'.")


def atualizar():
    mudar_status(input("Código: ").strip().zfill(3), input(f"Nova situação {STATUS}: ").strip().lower())


def proxima_da_fila():
    if not fila_nao_examinadas:
        print("Fila vazia: nada a examinar.")
        return
    cod = fila_nao_examinadas[0]
    print(f"Examinando a ocorrência {cod} (a mais antiga da fila).")
    mudar_status(cod, "em análise")


def ultimos():
    if not pilha_eventos:
        print("Sem eventos.")
    for ev in reversed(pilha_eventos[-5:]):  # topo primeiro
        print(f"Dia {ev['dia']}: ocorrência {ev['id']} {ev['de']} -> {ev['para']}")


def hierarquia_view():
    for bairro, cats in hierarquia.items():
        print(bairro)
        for cat, ids in cats.items():
            print(f"  └ {cat}: {', '.join(ids)}")


def indicadores():
    total = len(ocorrencias)
    # Matriz categoria x status (lista de listas)
    matriz = [[0] * len(STATUS) for _ in CATEGORIAS]
    for r in ocorrencias:
        matriz[CATEGORIAS.index(r["categoria"])][STATUS.index(r["status"])] += 1
    print(f"\nTotal de ocorrências válidas: {total}")
    print("Regra: proporção = quantidade / total * 100\n")
    print(f"{'categoria':<19}" + "".join(f"{s:<12}" for s in STATUS) + "total   %")
    for i, cat in enumerate(CATEGORIAS):
        t = sum(matriz[i])
        print(f"{cat:<19}" + "".join(f"{n:<12}" for n in matriz[i]) + f"{t:<8}{t / total * 100:.0f}%")
    print("\nPor situação:")
    for j, s in enumerate(STATUS):
        q = sum(matriz[i][j] for i in range(len(CATEGORIAS)))
        print(f"  {s}: {q} ({q / total * 100:.0f}%)")
    tempos = [r["conclusao"] - r["abertura"] for r in ocorrencias if r["conclusao"] is not None]
    pend = sum(1 for r in ocorrencias if r["status"] != "concluída")
    print(f"\nPendências (não concluídas): {pend}")
    if tempos:
        print(f"Tempo médio até conclusão = soma({sum(tempos)}) / {len(tempos)} = {sum(tempos) / len(tempos):.1f} dias simulados")
    mais = max(range(len(CATEGORIAS)), key=lambda i: sum(matriz[i]))
    print(f"\nConclusão: '{CATEGORIAS[mais]}' é a categoria mais frequente e {pend} de {total} "
          f"demandas seguem pendentes, sugerindo foco em reduzir a fila de abertas.")
    if rejeitadas:
        print("\nRegistros rejeitados na carga:", rejeitadas)


MENU = """
=== Neighborhood Action Dashboard ===
1 Listar   2 Buscar por código   3 Filtrar   4 Cadastrar
5 Atualizar status   6 Examinar próxima da fila   7 Últimos eventos
8 Indicadores   9 Hierarquia   0 Sair"""
ACOES = {"1": lambda: listar(ocorrencias), "2": buscar, "3": filtrar, "4": cadastrar,
         "5": atualizar, "6": proxima_da_fila, "7": ultimos, "8": indicadores, "9": hierarquia_view}

if __name__ == "__main__":
    carregar()
    print(f"Carregadas {len(ocorrencias)} ocorrências; {len(rejeitadas)} rejeitada(s) pela validação.")
    while True:
        print(MENU)
        op = input("Opção: ").strip()
        if op == "0":
            break
        ACOES.get(op, lambda: print("Opção inválida."))()
