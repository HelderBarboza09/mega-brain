"""Tests for audit_layers.py classify_path function.

Converted from core/intelligence/validation/verify_classifications.py (38 spot checks)
into proper pytest parametrized tests.
"""
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "core" / "intelligence" / "validation"))

from audit_layers import classify_path

REPO_ROOT = PROJECT_ROOT


# -- L1: Core engine ---------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("core/tasks/HO-TP-001.md", "L1", "Core task file"),
    ("bin/cli.js", "L1", "CLI entry point"),
    (".claude/CLAUDE.md", "L1", "Claude integration"),
    ("docs/audit/AUDIT-REPORT.md", "L1", "Documentation"),
])
def test_l1_core_engine(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L1: Root project files --------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("package.json", "L1", "NPM package config"),
    ("package-lock.json", "L1", "NPM lockfile"),
    (".gitignore", "L1", "Git ignore rules"),
    (".npmignore", "L1", "NPM ignore rules"),
    (".env.example", "L1", "Environment template"),
    ("README.md", "L1", "Root documentation"),
    ("CONTRIBUTING.md", "L1", "Contribution guide"),
    ("QUICK-START.md", "L1", "Quick start guide"),
    ("requirements.txt", "L1", "Python dependencies"),
    (".gitattributes", "L1", "Git attributes"),
    (".gitleaks.toml", "L1", "Secret scanning config"),
])
def test_l1_root_files(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L1: GitHub ---------------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    (".github/workflows/publish.yml", "L1", "CI publish workflow"),
    (".github/CODEOWNERS", "L1", "Code ownership"),
    (".github/ISSUE_TEMPLATE/bug.md", "L1", "Issue template"),
])
def test_l1_github(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L1: Planning -------------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    (".planning/ROADMAP.md", "L1", "GSD roadmap"),
    (".planning/STATE.md", "L1", "GSD state"),
    (".planning/phases/09-layer-validation/09-01-PLAN.md", "L1", "Phase plan"),
])
def test_l1_planning(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L1: IDE configs ----------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    (".cursor/rules/mega-brain.md", "L1", "Cursor IDE rules"),
    (".windsurf/agents.yaml", "L1", "Windsurf agents"),
    (".antigravity/README.md", "L1", "Antigravity docs"),
])
def test_l1_ide_configs(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L1: Agents scaffold ------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("agents/boardroom/README.md", "L1", "Boardroom docs"),
    ("agents/constitution/BASE-CONSTITUTION.md", "L1", "Agent constitution"),
    ("agents/AGENT-INDEX.yaml", "L1", "Agent index"),
    ("agents/conclave/CONCLAVE-PROTOCOL.md", "L1", "Conclave protocol"),
])
def test_l1_agents_scaffold(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L1: Structure markers (.gitkeep) -----------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("inbox/.gitkeep", "L1", "Inbox structure marker"),
    ("agents/cargo/.gitkeep", "L1", "Cargo structure marker"),
    ("knowledge/.gitkeep", "L1", "Knowledge structure marker"),
])
def test_l1_structure_markers(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L2: Premium content ------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("agents/minds/some-agent/AGENT.md", "L2", "Mind clone agent"),
    ("agents/cargo/some-role/AGENT.md", "L2", "Cargo agent"),
    ("knowledge/external/dossiers/some-file.md", "L2", "Knowledge dossier"),
])
def test_l2_premium_content(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- L3: Personal data --------------------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("inbox/some-file.txt", "L3", "Inbox content"),
    ("logs/some-log.md", "L3", "Session log"),
    (".claude/sessions/SESSION-2026.md", "L3", "Claude session"),
])
def test_l3_personal_data(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- NEVER: Secrets and system files ------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    (".env", "NEVER", "Environment secrets"),
    ("credentials.json", "NEVER", "OAuth credentials"),
    (".mcp.json", "NEVER", "MCP config with tokens"),
    (".DS_Store", "NEVER", "macOS metadata"),
])
def test_never_secrets(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"


# -- DELETE: Obsolete and stale -----------------------------------------------

@pytest.mark.parametrize("rel_path,expected,desc", [
    ("some/path/finance-agent/file.md", "DELETE", "Obsolete finance agent"),
    ("artifacts/README 2.md", "DELETE", "Stale macOS duplicate"),
    ("knowledge/TAG-RESOLVER 2.json", "DELETE", "Stale macOS duplicate"),
])
def test_delete_obsolete(rel_path, expected, desc):
    layer, _ = classify_path(REPO_ROOT / rel_path, REPO_ROOT, is_file=True)
    assert layer == expected, f"{desc}: {rel_path} -> {layer}, expected {expected}"
