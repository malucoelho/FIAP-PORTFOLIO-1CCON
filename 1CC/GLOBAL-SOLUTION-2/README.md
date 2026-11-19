# Neighborhood Action Dashboard

**Equipe:** Equipe Joma
**Integrantes (RM):** maria luiza coelho inocencio - rm: 576414

## 1. Comunidade simulada, problema e público
Três bairros fictícios (Centro, Jardim Norte e Vila Sul) com demandas de iluminação, acessibilidade, limpeza e conservação de espaços coletivos. Hoje os relatos são dispersos e os moradores não acompanham o andamento. O painel organiza as ocorrências e mostra indicadores simples. Beneficia moradores, associações de bairro e quem acompanha as demandas. Todos os dados são fictícios.

## 2. Como executar
Dentro da pasta `1CC/GLOBAL-SOLUTION-2`, execute:
```
python src/sistema.py
```
Os dados (14 registros, dos quais 13 válidos) são inicializados no próprio código (lista `DADOS`). Cada linha tem: código, categoria, descrição, bairro, local genérico, dia de abertura, status e dia de conclusão. Campos obrigatórios: categoria, descrição, bairro, local e status. O código é gerado automaticamente. A data é simulada em dias (dia atual = 10).

**Status:** `aberta` = registrada e ainda não examinada; `em análise` = em exame pela equipe; `concluída` = demanda encerrada.

## 3. Estruturas de dados e justificativas
| Estrutura | Uso | Por quê |
|---|---|---|
| Lista `ocorrencias` | guarda todos os registros válidos | permite percorrer e listar |
| Dicionário `por_id` | acesso por código | busca direta, sem varrer a lista |
| Fila (`deque`) | ocorrências abertas por ordem de registro | a mais antiga é examinada primeiro (FIFO) |
| Pilha (lista, push/topo) | últimos eventos de status | o evento mais recente é consultado primeiro (LIFO) |
| Hierarquia bairro → categoria → códigos | visão organizada por local | mostra onde cada tipo de problema se concentra |
| Matriz categoria × status | base dos indicadores | resume as quantidades em tabela |

## 4. Regras lógicas
- **Cadastro:** recusado se faltar categoria, descrição, bairro ou local, se a categoria não for do padrão ou se o código já existir.
- **Expressão booleana de validação:** `not categoria or categoria not in CATEGORIAS`. Se a categoria for vazia ou fora do padrão, o registro é recusado. Por isso o registro 013 (sem categoria) é rejeitado na carga.
- **Filtro (AND):** `(not cat or r["categoria"] == cat) and (not st or r["status"] == st)`. O registro passa se atender aos dois filtros informados; filtro vazio significa "todos".
- **Atualização (NOT):** `not (ordem(novo) > ordem(atual))` recusa a mudança, pois a situação só pode avançar (aberta → em análise → concluída). Situação desconhecida e código inexistente geram mensagem clara.
- **Entrada inválida (OR):** `cat and cat not in CATEGORIAS or st and st not in STATUS` recusa filtros inexistentes.

## 5. Indicadores
- Proporção = quantidade ÷ total × 100, por categoria e por status.
- Pendências = ocorrências com status diferente de `concluída`.
- Tempo médio = soma(dia de conclusão − dia de abertura) ÷ nº de concluídas.

Com os dados simulados (13 ocorrências válidas na carga inicial), 10 das 13 demandas estão pendentes (6 abertas e 4 em análise). Isso sugere que o gargalo está em examinar as demandas abertas, não em concluí-las.

## 6. Exemplo de uso
1. **Cadastro (opção 4):** informar categoria, descrição, bairro e local → `Ocorrência 015 cadastrada.`
2. **Consulta (opção 2):** código `004` mostra o registro; código inexistente → `Registro não encontrado.`
3. **Alteração (opção 5):** código `004`, nova situação `em análise` → `Ocorrência 004 agora está 'em análise'.` e o evento entra no histórico.
4. **Indicadores (opção 8)** e **saída (opção 0).**

## 7. Acessibilidade, inclusão e privacidade
Mensagens em linguagem simples e menu numerado, com tabela em texto puro legível por leitores de tela. Nenhum dado pessoal é coletado; os locais são genéricos e os dados, fictícios.

## 8. Vídeo
https://youtu.be/8JxXk_odOqk?si=AzlED2W-liidOWW5

## 9. Conclusões, limitações e aprendizados
**Aprendizados**
- Cada estrutura de dados tem uma função: lista para percorrer, dicionário para acessar por código, fila para respeitar a ordem de chegada, pilha para o evento mais recente, hierarquia e matriz para organizar e resumir.
- Validar antes de guardar evita erros; as condições com `and`, `or` e `not` definem cada mensagem do sistema.
- Regras claras de status e um histórico simples facilitam o acompanhamento.
- Indicadores simples mostram onde está o gargalo: examinar as demandas abertas.
- Usamos IA como apoio, mas só entendemos o resultado ao testar cada opção e conferir as contas.

**Limitações:** dados fictícios, sem persistência (as alterações somem ao fechar), apenas terminal e sem integração com órgãos públicos. Em uma versão futura, os registros poderiam ser gravados em arquivo.
