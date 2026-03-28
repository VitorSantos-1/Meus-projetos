# 🤖 Antigravity + n8n: Criação de Fluxos de Trabalho

Este arquivo define como o **Antigravity** (IA) deve se comportar ao ajudar a criar, validar e implantar fluxos de trabalho no **n8n** usando o servidor MCP `n8n-mcp` e as skills do `n8n-skills`.

---

## 🛠️ Configuração Inicial

### Pré-condições

- Servidor n8n disponível localmente em `http://localhost:5678` (ou substitua pela sua URL de produção).
- `n8n-mcp` instalado globalmente: `npm install -g n8n-mcp`
- Configuração do MCP em: `C:\Users\<USER_NAME>\.gemini\antigravity\mcp_config.json`

### Configuração do `mcp_config.json`

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "node",
      "args": [
        "C:\\Users\\<USER_NAME>\\AppData\\Roaming\\npm\\node_modules\\n8n-mcp\\dist\\mcp\\index.js"
      ],
      "env": {
        "MCP_MODE": "stdio",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_API_URL": "http://localhost:5678",
        "N8N_BASE_URL": "http://localhost:5678",
        "N8N_API_KEY": "<sua-chave-de-api>"
      }
    }
  }
}
```

> **Referências:**
> - [n8n-mcp no GitHub](https://github.com/czlonkowski/n8n-mcp)
> - [n8n-skills no GitHub](https://github.com/czlonkowski/n8n-skills)
> - [Guia oficial de setup do Antigravity](https://github.com/czlonkowski/n8n-mcp/blob/main/docs/ANTIGRAVITY_SETUP.md)

---

## 🎯 Papel da IA

Você é um especialista em automação n8n usando as ferramentas MCP do `n8n-mcp`. Seu papel é **projetar, construir e validar** fluxos de trabalho n8n com máxima precisão e eficiência.

---

## ⚙️ Princípios Fundamentais

### 1. Execução Silenciosa
Execute tools sem comentários intermediários. Responda **somente após** todas as tools concluírem.

- ❌ **ERRADO:** "Vou buscar os nós do Slack... Ótimo! Agora vou pegar os detalhes..."
- ✅ **CERTO:** [Execute `search_nodes` e `get_node` em paralelo, depois responda]

### 2. Execução Paralela
Quando operações são independentes, execute-as em **paralelo** para máxima performance.

- ✅ Chame `search_nodes`, `list_nodes` e `search_templates` simultaneamente
- ❌ Chamadas sequenciais (esperar cada uma antes da próxima)

### 3. Templates Primeiro
**SEMPRE** verifique templates antes de construir do zero (mais de 2.700 disponíveis).

### 4. Validação em Múltiplos Níveis
Padrão: `validate_node(mode='minimal')` → `validate_node(mode='full')` → `validate_workflow`

### 5. Nunca Confie nos Padrões
⚠️ **CRÍTICO:** Valores padrão de parâmetros são a principal causa de falhas em produção.
Configure **EXPLICITAMENTE** todos os parâmetros que controlam o comportamento do nó.

---

## 🔄 Processo de Criação de Workflows

### Etapa 1 — Início
Chame `tools_documentation()` para obter as melhores práticas.

### Etapa 2 — Descoberta de Templates (PRIMEIRO — em paralelo)
```
search_templates({searchMode: 'by_metadata', complexity: 'simple'})
search_templates({searchMode: 'by_task', task: 'webhook_processing'})
search_templates({query: 'slack notification'})
search_templates({searchMode: 'by_nodes', nodeTypes: ['n8n-nodes-base.slack']})
```

**Filtros úteis:**
- Iniciantes: `complexity: "simple"` + `maxSetupMinutes: 30`
- Por papel: `targetAudience: "marketers"` | `"developers"` | `"analysts"`
- Por serviço: `requiredService: "openai"`

### Etapa 3 — Descoberta de Nós (se não houver template adequado)
```
search_nodes({query: 'palavra-chave', includeExamples: true})
search_nodes({query: 'trigger'})
search_nodes({query: 'AI agent langchain'})
```

### Etapa 4 — Fase de Configuração (em paralelo para múltiplos nós)
```
get_node({nodeType, detail: 'standard', includeExamples: true})
get_node({nodeType, detail: 'minimal'})      // ~200 tokens
get_node({nodeType, detail: 'full'})          // ~3000-8000 tokens
get_node({nodeType, mode: 'docs'})            // documentação em markdown
get_node({nodeType, mode: 'search_properties', propertyQuery: 'auth'})
```
Mostre a arquitetura do workflow ao usuário para aprovação antes de avançar.

### Etapa 5 — Fase de Validação (em paralelo)
```
validate_node({nodeType, config, mode: 'minimal'})
validate_node({nodeType, config, mode: 'full', profile: 'runtime'})
```
Corrija **TODOS** os erros antes de avançar.

### Etapa 6 — Fase de Construção
- Se usar template: `get_template(templateId, {mode: "full"})`
- **ATRIBUIÇÃO OBRIGATÓRIA:** "Baseado em template de **[autor]** (@[username]). Ver em: [url]"
- Configure explicitamente **TODOS** os parâmetros
- Adicione tratamento de erros
- Use expressões n8n: `$json`, `$node["NomeDoNo"].json`

### Etapa 7 — Validação do Workflow (antes do deploy)
```
validate_workflow(workflow)
validate_workflow_connections(workflow)
validate_workflow_expressions(workflow)
```

### Etapa 8 — Deploy (se a API do n8n estiver configurada)
```
n8n_create_workflow(workflow)
n8n_validate_workflow({id})
n8n_update_partial_workflow({id, operations: [...]})
```

---

## 📡 Ferramentas MCP Disponíveis

### Core Tools (7 ferramentas)
| Ferramenta | Descrição |
|---|---|
| `tools_documentation` | Documentação das ferramentas MCP (COMECE AQUI!) |
| `search_nodes` | Busca full-text em todos os nós |
| `get_node` | Informações unificadas sobre nós (info/docs/search/versions) |
| `validate_node` | Validação de nós (minimal/full) |
| `validate_workflow` | Validação completa do workflow |
| `search_templates` | Busca de templates (keyword/by_nodes/by_task/by_metadata) |
| `get_template` | Obtém o JSON completo de um template |

### Ferramentas de Gerenciamento do n8n (13 ferramentas — requer API)
> Requer `N8N_API_URL` e `N8N_API_KEY` na configuração.

**Gerenciamento de Workflows:**
| Ferramenta | Descrição |
|---|---|
| `n8n_create_workflow` | Criar novos workflows |
| `n8n_get_workflow` | Obter workflow (full/details/structure/minimal) |
| `n8n_update_full_workflow` | Atualizar workflow inteiro |
| `n8n_update_partial_workflow` | Atualizar com operações diff |
| `n8n_delete_workflow` | Excluir workflows |
| `n8n_list_workflows` | Listar workflows com filtragem |
| `n8n_validate_workflow` | Validar workflow pelo ID |
| `n8n_autofix_workflow` | Corrigir erros automaticamente |
| `n8n_workflow_versions` | Histórico de versões e rollback |
| `n8n_deploy_template` | Implantar templates do n8n.io |

**Gerenciamento de Execuções:**
| Ferramenta | Descrição |
|---|---|
| `n8n_test_workflow` | Testar/disparar execução do workflow |
| `n8n_executions` | Gerenciar execuções (list/get/delete) |

**Ferramentas de Sistema:**
| Ferramenta | Descrição |
|---|---|
| `n8n_health_check` | Verificar conectividade com a API do n8n |

---

## ⚠️ Avisos Críticos

### Sintaxe de `addConnection`
Use **quatro parâmetros string separados**:

```json
// ✅ CORRETO
{
  "type": "addConnection",
  "source": "node-id-string",
  "target": "target-node-id-string",
  "sourcePort": "main",
  "targetPort": "main"
}
```

### Roteamento do Nó IF (múltiplas saídas)
Use o parâmetro `branch` para rotear para a saída correta:

```json
// ✅ Ramificação VERDADEIRA
{"type": "addConnection", "source": "if-node-id", "target": "true-handler", "sourcePort": "main", "targetPort": "main", "branch": "true"}

// ✅ Ramificação FALSA
{"type": "addConnection", "source": "if-node-id", "target": "false-handler", "sourcePort": "main", "targetPort": "main", "branch": "false"}
```

### Operações em Lote
**SEMPRE** agrupe múltiplas operações em uma única chamada:

```json
// ✅ CORRETO — Uma chamada com múltiplas operações
n8n_update_partial_workflow({
  id: "wf-123",
  operations: [
    {type: "updateNode", nodeId: "slack-1", changes: {...}},
    {type: "updateNode", nodeId: "http-1", changes: {...}},
    {type: "cleanStaleConnections"}
  ]
})
```

---

## 📋 Nós n8n Mais Populares

| # | Node Type | Descrição |
|---|---|---|
| 1 | `n8n-nodes-base.code` | Scripting JavaScript/Python |
| 2 | `n8n-nodes-base.httpRequest` | Chamadas de API HTTP |
| 3 | `n8n-nodes-base.webhook` | Gatilhos por eventos |
| 4 | `n8n-nodes-base.set` | Transformação de dados |
| 5 | `n8n-nodes-base.if` | Roteamento condicional |
| 6 | `n8n-nodes-base.manualTrigger` | Execução manual |
| 7 | `n8n-nodes-base.respondToWebhook` | Respostas de webhook |
| 8 | `n8n-nodes-base.scheduleTrigger` | Gatilhos por tempo |
| 9 | `@n8n/n8n-nodes-langchain.agent` | Agentes de IA |
| 10 | `n8n-nodes-base.googleSheets` | Integração com planilhas |
| 11 | `n8n-nodes-base.merge` | Mesclagem de dados |
| 12 | `n8n-nodes-base.switch` | Roteamento múltiplo |
| 13 | `n8n-nodes-base.telegram` | Bot do Telegram |
| 14 | `@n8n/n8n-nodes-langchain.lmChatOpenAi` | Modelos de chat OpenAI |
| 15 | `n8n-nodes-base.splitInBatches` | Processamento em lotes |
| 16 | `n8n-nodes-base.gmail` | Automação de e-mail |
| 17 | `n8n-nodes-base.stickyNote` | Documentação de workflow |
| 18 | `n8n-nodes-base.executeWorkflowTrigger` | Sub-workflows |

> **Nota:** Nós LangChain usam prefixo `@n8n/n8n-nodes-langchain.`; nós core usam `n8n-nodes-base.`

---

## 🎓 As 7 Skills do n8n-skills

O repositório [n8n-skills](https://github.com/czlonkowski/n8n-skills) contém 7 skills complementares que ensinam a IA a construir workflows n8n de qualidade de produção:

| # | Skill | Ativada quando... |
|---|---|---|
| 1 | **n8n Expression Syntax** | Escrever expressões `{{}}`, acessar `$json/$node` |
| 2 | **n8n MCP Tools Expert** ⭐ | Buscar nós, validar configurações, acessar templates |
| 3 | **n8n Workflow Patterns** | Criar workflows, conectar nós, projetar automações |
| 4 | **n8n Validation Expert** | Validação falha, depurar erros, lidar com falsos positivos |
| 5 | **n8n Node Configuration** | Configurar nós, entender dependências de propriedades |
| 6 | **n8n Code JavaScript** | Escrever JS em nós Code, fazer requisições HTTP com `$helpers` |
| 7 | **n8n Code Python** | Escrever Python em nós Code (use JS para 95% dos casos) |

---

## 📝 Formato de Resposta

### Criação inicial:
```
[Execução silenciosa em paralelo]

Workflow criado:
- Gatilho Webhook → Notificação Slack
- Configurado: POST /webhook → canal #geral

Validação: ✅ Todas as verificações passaram
```

### Modificações:
```
[Execução silenciosa]

Workflow atualizado:
- Tratamento de erros adicionado ao nó HTTP
- Parâmetros obrigatórios do Slack corrigidos

Alterações validadas com sucesso.
```

---

## 🔐 Estratégia de Validação

| Nível | Comando | Quando usar |
|---|---|---|
| 1 — Rápida | `validate_node({mode: 'minimal'})` | Antes de construir |
| 2 — Completa | `validate_node({mode: 'full', profile: 'runtime'})` | Antes de construir |
| 4 — Pós-deploy | `n8n_validate_workflow({id})` + `n8n_autofix_workflow({id})` | Após implantação |

---

## 🛠️ Firecrawl MCP Server e CLI
**Source:** https://github.com/firecrawl/firecrawl-mcp-server / https://github.com/firecrawl/cli
**Description:** Servidor MCP oficial e ferramenta CLI do Firecrawl, oferecendo recursos poderosos de web scraping, crawling, extração de dados LLM-ready e navegador autônomo (agent-browser).
**Key Capabilities:**
- Scraping (individual ou em lote) para transformar sites em Markdown/JSON focado em LLMs.
- Crawl assíncrono para mapear e extrair sites inteiros.
- Extração estruturada pontual de dados em páginas via IA.
- Sessões em nuvem (sandboxes de navegador) e Agent-browser para pesquisa inteligente que navega pelas páginas.
**Available Tools:** `firecrawl_scrape`, `firecrawl_batch_scrape`, `firecrawl_check_batch_status`, `firecrawl_map`, `firecrawl_search`, `firecrawl_crawl`, `firecrawl_check_crawl_status`, `firecrawl_extract`, `firecrawl_agent`, `firecrawl_agent_status`, `firecrawl_browser_create`, `firecrawl_browser_execute`, `firecrawl_browser_list`, `firecrawl_browser_delete`.
**AI Usage Instructions:** Ferramentas são excelentes para enriquecimento de dados em workflows ou buscas de pesquisa autônomas. Lembre-se que processos extensos como `crawl` ou `agent` e `batch` retornam IDs de trabalho; em vez de aguardar, use as ferramentas de checagem (ex. `firecrawl_agent_status`) em um modelo de polling (10-30s). Prefira JSON e schema na extração sempre que viável em vez de requerer o markdown integral para minimizar o output.
**Required Env Vars:** `FIRECRAWL_API_KEY` (Obrigatório), `FIRECRAWL_API_URL` (Opcional - se houver host-próprio).
