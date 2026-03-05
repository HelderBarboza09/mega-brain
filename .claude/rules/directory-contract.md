# Directory Contract — Mega Brain

> **Versão:** 1.0.0
> **Source of Truth:** `core/paths.py`
> **Enforcement:** `.claude/hooks/directory_contract_guard.py` (PreToolUse, WARN)
> **Keywords:** "directory", "output", "path", "onde salvar", "where to save"

---

## Diretórios e Propósito

| Diretório | Categoria | O Que Pertence | Git |
|-----------|-----------|----------------|-----|
| `core/` | Engine | tasks, workflows, intelligence, paths.py | Tracked |
| `agents/` | Knowledge Agents | conclave, cargo, minds | Tracked |
| `reference/` | Documentation | guides, protocols, templates | Tracked |
| `bin/` | CLI Tools | npm executables | Tracked |
| `system/` | System Config | JARVIS state, DNA, soul | Tracked |
| `.planning/` | GSD Plans | phases, roadmap, state | Tracked |
| `.claude/` | Config + Runtime | hooks, skills, commands, rules | Tracked |
| `artifacts/` | Generated Output | audit reports, validation | Gitignored |
| `logs/` | Session Logs | batches, JSONL audit trails | Gitignored |
| `inbox/` | Raw Materials | L3 personal content | Gitignored |
| `knowledge/` | Knowledge Base | L3 dna, dossiers, playbooks | Gitignored |
| `research/` | Ad-hoc Analysis | L3 blueprints, deep-dives | Gitignored |
| `processing/` | Pipeline Artifacts | speakers, entities, diarization | Gitignored |
| `.data/` | Indexes | RAG, knowledge graph, embeddings | Gitignored |

## Output Routing (quem escreve onde)

| Script/Hook | Escreve Em | Constante em paths.py |
|-------------|------------|----------------------|
| `audit_layers.py` | `artifacts/audit/` | `ROUTING["audit_report"]` |
| `validate_layers.py` | `artifacts/audit/` | `ROUTING["audit_report"]` |
| `session_autosave_v2.py` | `.claude/sessions/` | `ROUTING["session_log"]` |
| `skill_indexer.py` | `.claude/mission-control/` | `ROUTING["skill_index"]` |
| `post_batch_cascading.py` | `logs/batches/` | `ROUTING["batch_log"]` |
| `stop_hook_completeness.py` | `logs/handoffs/` | `ROUTING["handoff"]` |
| `chunker.py` | `.data/rag_index/` | `ROUTING["rag_chunks"]` |
| `graph_builder.py` | `.data/knowledge_graph/` | `ROUTING["graph"]` |
| `memory_splitter.py` | `knowledge/dna/persons/` | `ROUTING["memory_split"]` |
| `sow_generator.py` | `agents/sua-empresa/sow/` | `ROUTING["sow_output"]` |
| `organized_downloader.py` | `inbox/` | `ROUTING["download"]` |

## Proibições

- **`docs/`** — PROIBIDO para novos arquivos. Usar `reference/` em vez disso.
- **Novos top-level dirs** — Não criar diretórios na raiz sem atualizar este contrato.
- **Hardcoded paths** — Novos scripts DEVEM importar de `core/paths.py`.

## Como Usar

```python
from core.paths import ROUTING, ARTIFACTS

# Correto: usar constante
output = ROUTING["audit_report"] / "report.json"

# Errado: hardcodar path
output = Path("docs/audit/report.json")  # PROIBIDO
```
