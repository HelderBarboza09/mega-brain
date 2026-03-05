"""
core/paths.py — Directory Contract (machine-readable)

Single Source of Truth for all output paths in the Mega Brain system.
Equivalent to aios-core's config.js PATHS object.

Usage:
    from core.paths import ROUTING, LOGS, ARTIFACTS
    output_path = ROUTING["audit_report"] / "AUDIT-REPORT.json"
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── TRACKED (L1/L2) ──────────────────────────────────────────────
CORE = ROOT / "core"
AGENTS = ROOT / "agents"
REFERENCE = ROOT / "reference"
BIN = ROOT / "bin"
SYSTEM = ROOT / "system"
PLANNING = ROOT / ".planning"
CLAUDE = ROOT / ".claude"
RULES = CLAUDE / "rules"
SKILLS = CLAUDE / "skills"
HOOKS = CLAUDE / "hooks"
COMMANDS = CLAUDE / "commands"

# ── GITIGNORED (L3 / Runtime) ────────────────────────────────────
LOGS = ROOT / "logs"
INBOX = ROOT / "inbox"
KNOWLEDGE = ROOT / "knowledge"
PROCESSING = ROOT / "processing"
ARTIFACTS = ROOT / "artifacts"
DATA = ROOT / ".data"
RESEARCH = ROOT / "research"

# ── STATE (Gitignored, high-frequency writes) ────────────────────
MISSION_CONTROL = CLAUDE / "mission-control"
SESSIONS = CLAUDE / "sessions"
JARVIS = CLAUDE / "jarvis"
RAG_INDEX = DATA / "rag_index"
KNOWLEDGE_GRAPH = DATA / "knowledge_graph"
TRASH = CLAUDE / "trash"

# ── OUTPUT ROUTING ───────────────────────────────────────────────
# Scripts MUST use these constants instead of hardcoding paths.
# New scripts: import from here. Existing scripts: migrate incrementally.
ROUTING = {
    # Audit & validation outputs
    "audit_report": ARTIFACTS / "audit",
    "layer_validation": LOGS,
    # Session & state
    "session_log": SESSIONS,
    "mission_state": MISSION_CONTROL,
    "pipeline_state": MISSION_CONTROL,
    "skill_index": MISSION_CONTROL,
    "autosave_state": MISSION_CONTROL,
    # Logs (append-only JSONL)
    "batch_log": LOGS / "batches",
    "handoff": LOGS / "handoffs",
    "cascade_log": LOGS,
    "tool_usage": LOGS,
    "quality_gaps": LOGS,
    "dossier_trigger": LOGS,
    "autonomous_log": LOGS,
    # Knowledge & RAG
    "rag_chunks": RAG_INDEX,
    "rag_vectors": RAG_INDEX,
    "graph": KNOWLEDGE_GRAPH,
    "memory_split": KNOWLEDGE / "dna" / "persons",
    "nav_map": KNOWLEDGE,
    # Processing pipeline
    "entity_registry": PROCESSING,
    "speakers": PROCESSING,
    "diarization": PROCESSING,
    "voice_embeddings": DATA / "voice_embeddings",
    # Agent outputs
    "sow_output": AGENTS / "sua-empresa" / "sow",
    "generated_skill": SKILLS,
    # Downloads
    "download": INBOX,
    # Trash (never delete, always move here)
    "trash": TRASH,
}

# ── PROHIBITED DIRECTORIES ───────────────────────────────────────
# New files MUST NOT be created in these directories.
PROHIBITED = [
    ROOT / "docs",  # Use REFERENCE instead
]
