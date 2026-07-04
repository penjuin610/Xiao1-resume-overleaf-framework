#!/usr/bin/env python3
"""Deterministic helper for a local LaTeX resume engine.

This script is intentionally small and public-safe. It does not write resume
bullets, call AI APIs, use browsers, or compile LaTeX directly. It prepares
role folders, creates compact context packs, wraps scripts/build_resume.sh, and
returns concise JSON for an agent or shell workflow.
"""

from pathlib import Path
import argparse
import subprocess
import json
import re
import unicodedata
from datetime import datetime
import shutil
import difflib


ROOT = Path(__file__).resolve().parent
if ROOT.name == "scripts":
    ROOT = ROOT.parent

SOURCE_DIR = ROOT / "source"
ROLES_DIR = SOURCE_DIR / "roles"
ACTIVE_TEX = ROLES_DIR / "active.tex"
PRIVATE_DIR = ROOT / "private"
BUILD_SCRIPT = ROOT / "scripts" / "build_resume.sh"
OUTPUT_DIR = ROOT.parent / "resumes"
BUILD_DIR = ROOT / "output" / "build"
WRAPPER_LOG_DIR = ROOT / "output" / "resume_py_logs"
APPLICANT_SLUG = "Applicant_Name"

EDITABLE_SECTIONS = ["experience", "skills", "projects", "education", "profile"]
STOPWORDS = {
    "about", "above", "across", "after", "again", "against", "also", "and",
    "any", "are", "because", "been", "being", "between", "both", "but",
    "can", "company", "could", "does", "doing", "done", "each", "for",
    "from", "had", "has", "have", "here", "how", "into", "its", "job",
    "may", "more", "need", "not", "our", "out", "own", "role", "such",
    "than", "that", "the", "their", "them", "then", "there", "these",
    "they", "this", "through", "too", "use", "was", "were", "what",
    "when", "where", "who", "will", "with", "work", "you", "your",
}


def now_iso():
    return datetime.now().replace(microsecond=0).isoformat()


def emit(payload, status=0):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(status)


def read_text(path):
    return path.read_text(encoding="utf-8")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def ascii_fold(value):
    normalized = unicodedata.normalize("NFKD", value)
    return normalized.encode("ascii", "ignore").decode("ascii")


def slugify(value):
    slug = ascii_fold(value).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return re.sub(r"-+", "-", slug) or "role"


def role_key_for(company, role):
    return slugify(company + " " + role)


def safe_name_part(value, fallback):
    clean = ascii_fold(value).replace("&", "and")
    clean = re.sub(r"[^A-Za-z0-9]+", "_", clean).strip("_")
    return clean or fallback


def output_job_name(company, role):
    return f"{APPLICANT_SLUG}_{safe_name_part(company, 'Company')}_{safe_name_part(role, 'Role')}"


def current_role_key():
    if not ACTIVE_TEX.exists():
        return "baseline"
    match = re.search(r"\\renewcommand\{\\ResumeRoleKey\}\{([^}]+)\}", read_text(ACTIVE_TEX))
    return match.group(1) if match else "baseline"


def set_active_role(role_key):
    write_text(ACTIVE_TEX, f"\\renewcommand{{\\ResumeRoleKey}}{{{role_key}}}\n")


def role_dir(role_key):
    return ROLES_DIR / role_key


def load_json(path, fallback):
    if not path.exists():
        return fallback
    return json.loads(read_text(path))


def tokenize(text):
    words = re.findall(r"[a-z0-9][a-z0-9+.#/-]*", ascii_fold(text).lower())
    return {word.strip("-_/") for word in words if len(word.strip("-_/")) >= 3 and word.strip("-_/") not in STOPWORDS}


def flatten_entry(entry):
    parts = [entry.get("name", "")]
    parts.extend(str(value) for value in entry.get("fields", {}).values())
    parts.extend(entry.get("safe_themes", []))
    parts.extend(entry.get("placement_guidance", []))
    return "\n".join(parts)


def score_text(jd_tokens, text):
    tokens = tokenize(text)
    overlap = jd_tokens & tokens
    fuzzy_bonus = 0
    for token in jd_tokens:
        if len(token) >= 5 and difflib.get_close_matches(token, tokens, n=1, cutoff=0.88):
            fuzzy_bonus += 1
    return len(overlap) + fuzzy_bonus, sorted(overlap)


def compact_jd_summary(jd_text):
    lines = [line.strip(" \t-*•") for line in jd_text.splitlines()]
    lines = [line for line in lines if line]
    jd_tokens = tokenize(jd_text)
    signal_words = {
        "analysis", "analytics", "business", "data", "excel", "finance",
        "kpi", "model", "operations", "python", "reporting", "risk", "sql",
        "stakeholder", "strategy", "tableau",
    }
    scored = []
    for line in lines:
        line_tokens = tokenize(line)
        score = len(line_tokens & signal_words) + min(len(line_tokens & jd_tokens), 8) / 10
        if score > 0:
            scored.append((score, line))
    scored.sort(key=lambda item: (-item[0], len(item[1])))
    highlights = []
    for _, line in scored:
        if line not in highlights:
            highlights.append(line)
        if len(highlights) >= 10:
            break
    tools = []
    normalized = ascii_fold(jd_text).lower().replace(" ", "")
    for tool in ["Excel", "Python", "SQL", "Tableau", "Power BI", "Pandas", "VBA", "NLP"]:
        if tool.lower().replace(" ", "") in normalized:
            tools.append(tool)
    seniority = re.findall(r"(?i)(\b\d+\s*[-–]\s*\d+\s+years\b|\b\d+\+?\s+years\b|\bsenior\b|\banalyst\b|\bmanager\b|\binternship\b)", jd_text)
    return {
        "highlights": highlights,
        "keywords": sorted(jd_tokens)[:40],
        "tools": tools,
        "seniority": sorted(set(item.strip() for item in seniority))[:8],
    }


def rank_entries(profile, jd_tokens, key):
    ranked = []
    for entry in profile.get(key, []):
        score, matched = score_text(jd_tokens, flatten_entry(entry))
        ranked.append({
            "name": entry.get("name", ""),
            "fields": entry.get("fields", {}),
            "safe_themes": entry.get("safe_themes", []),
            "placement_guidance": entry.get("placement_guidance", []),
            "score": score,
            "matched_terms": matched[:12],
        })
    return sorted(ranked, key=lambda item: (-item["score"], item["name"]))


def baseline_preview(section):
    path = SOURCE_DIR / "content" / f"{section}.tex"
    if not path.exists():
        return ""
    lines = [line.rstrip() for line in read_text(path).splitlines() if line.strip()]
    return "\n".join(lines[:18])


def recommended_sections(summary):
    text = " ".join(summary["keywords"]).lower()
    sections = ["experience", "skills"]
    if re.search(r"project|portfolio|github|automation|python|model|analytics|research", text):
        sections.append("projects")
    if re.search(r"degree|gpa|education|certification|academic", text):
        sections.append("education")
    return sections


def init_job(args):
    jd_file = Path(args.jd_file).expanduser()
    if not jd_file.exists():
        emit({"ok": False, "error": "jd_file_not_found", "path": str(jd_file)}, 2)
    role_key = role_key_for(args.company, args.role)
    target = role_dir(role_key)
    target.mkdir(parents=True, exist_ok=True)
    jd_target = target / "jd.md"
    shutil.copyfile(jd_file, jd_target)
    metadata = {
        "company": args.company,
        "role": args.role,
        "role_key": role_key,
        "created_at": now_iso(),
        "jd_file": str(jd_target),
        "source_jd_file": str(jd_file),
    }
    write_text(target / "job.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    set_active_role(role_key)
    emit({"ok": True, "role_key": role_key, "role_dir": str(target), "jd_file": str(jd_target), "active_role": role_key})


def prepare_context(args):
    rdir = role_dir(args.role_key)
    jd_path = rdir / "jd.md"
    if not jd_path.exists():
        emit({"ok": False, "error": "jd_md_not_found", "path": str(jd_path)}, 2)
    profile = load_json(PRIVATE_DIR / "private-profile.compact.json", {})
    jd_text = read_text(jd_path)
    summary = compact_jd_summary(jd_text)
    jd_tokens = tokenize(jd_text)
    core = rank_entries(profile, jd_tokens, "core_experience")[:4]
    optional = [item for item in rank_entries(profile, jd_tokens, "optional_experience") if item["score"] > 0][:2]
    projects = [item for item in rank_entries(profile, jd_tokens, "projects") if item["score"] > 0][:3]
    rec_sections = recommended_sections(summary)

    lines = [
        "# Resume Context Pack",
        "",
        f"Generated: {now_iso()}",
        f"Role key: `{args.role_key}`",
        "",
        "## JD Signal",
        "",
        "### Core Responsibilities / Requirements",
    ]
    lines.extend(f"- {item}" for item in summary["highlights"])
    lines.extend(["", "### Keywords", ", ".join(summary["keywords"]) or "None extracted"])
    lines.extend(["", "### Tools Mentioned", ", ".join(summary["tools"]) or "No explicit tool list detected"])
    lines.extend(["", "### Seniority Signal", ", ".join(summary["seniority"]) or "No explicit seniority signal detected"])
    lines.extend(["", "## Relevant Confirmed Experience"])
    for item in core + optional:
        lines.extend(["", "### " + item["name"]])
        for key, value in item["fields"].items():
            lines.append(f"- {key}: {value}")
        lines.append("- Matched terms: " + (", ".join(item["matched_terms"]) or "default/core"))
        lines.append("- Safe themes: " + "; ".join(item["safe_themes"]))
        if item["placement_guidance"]:
            lines.append("- Placement guidance: " + " ".join(item["placement_guidance"]))
    lines.extend(["", "## Relevant Optional Projects"])
    if projects:
        for item in projects:
            lines.extend(["", "### " + item["name"]])
            for key, value in item["fields"].items():
                lines.append(f"- {key}: {value}")
            lines.append("- Matched terms: " + (", ".join(item["matched_terms"]) or "none"))
            lines.append("- Safe themes: " + "; ".join(item["safe_themes"]))
    else:
        lines.append("No project scored above zero.")
    lines.extend(["", "## Baseline Sections To Read Next"])
    lines.extend(f"- `source/content/{section}.tex`" for section in rec_sections)
    lines.extend(["", "## Baseline Section Previews"])
    for section in rec_sections:
        preview = baseline_preview(section)
        if preview:
            lines.extend(["", f"### {section}.tex", "```tex", preview, "```"])
    context_path = rdir / "context.md"
    write_text(context_path, "\n".join(lines).strip() + "\n")
    emit({
        "ok": True,
        "role_key": args.role_key,
        "context_path": str(context_path),
        "recommended_sections": rec_sections,
        "experience_candidates": [item["name"] for item in core + optional],
        "project_candidates": [item["name"] for item in projects],
    })


def activate(args):
    if args.role_key != "baseline" and not role_dir(args.role_key).exists():
        emit({"ok": False, "error": "role_key_not_found", "role_key": args.role_key}, 2)
    set_active_role(args.role_key)
    emit({"ok": True, "active_role": args.role_key})


def covered_sections(role_key):
    rdir = role_dir(role_key)
    if not rdir.exists():
        return []
    return [section for section in EDITABLE_SECTIONS if (rdir / f"{section}.tex").exists()]


def parse_build_output(text, company, role):
    parsed = {
        "pdf_path": str(OUTPUT_DIR / f"{output_job_name(company, role)}.pdf"),
        "pages": None,
        "strict_one_page": False,
        "warnings": None,
    }
    match = re.search(r"(?m)^PDF:\s*(.+)$", text)
    if match:
        parsed["pdf_path"] = match.group(1).strip()
    match = re.search(r"(?m)^Pages:\s*(\d+)$", text)
    if match:
        parsed["pages"] = int(match.group(1))
    match = re.search(r"(?m)^Strict one page:\s*(yes|no)$", text)
    if match:
        parsed["strict_one_page"] = match.group(1) == "yes"
    match = re.search(r"(?m)^Warnings/overflow lines:\s*(\d+)$", text)
    if match:
        parsed["warnings"] = int(match.group(1))
    return parsed


def summarize_error(text, max_lines=20):
    lines = [line.rstrip() for line in text.splitlines()]
    pattern = re.compile(r"(^!|Error|error|Warning|Overfull|Underfull|Missing|Undefined|not found|Fatal|PDF is not strictly one page)")
    signals = [line for line in lines if pattern.search(line)]
    return "\n".join((signals or lines)[-max_lines:]).strip()


def append_ledger(company, role, parsed):
    role_key = current_role_key()
    job_meta = load_json(role_dir(role_key) / "job.json", {}) if role_key != "baseline" else {}
    entry = {
        "timestamp": now_iso(),
        "company": company,
        "role": role,
        "role_key": role_key,
        "jd_file": job_meta.get("jd_file", ""),
        "pdf_path": parsed.get("pdf_path"),
        "page_count": parsed.get("pages"),
        "warning_count": parsed.get("warnings"),
        "strict_one_page": parsed.get("strict_one_page"),
        "covered_sections": covered_sections(role_key),
    }
    path = PRIVATE_DIR / "application-ledger.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")


def build(args):
    if not BUILD_SCRIPT.exists():
        emit({"ok": False, "error": "build_script_not_found", "path": str(BUILD_SCRIPT)}, 2)
    cmd = [str(BUILD_SCRIPT), "--company", args.company, "--role", args.role]
    if args.require_one_page:
        cmd.append("--require-one-page")
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=False)
    WRAPPER_LOG_DIR.mkdir(parents=True, exist_ok=True)
    wrapper_log = WRAPPER_LOG_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{output_job_name(args.company, args.role)}.log"
    write_text(wrapper_log, "COMMAND: " + " ".join(cmd) + "\n\nSTDOUT:\n" + result.stdout + "\n\nSTDERR:\n" + result.stderr)
    combined = result.stdout + "\n" + result.stderr
    parsed = parse_build_output(combined, args.company, args.role)
    if result.returncode == 0:
        append_ledger(args.company, args.role, parsed)
        emit({"ok": True, **parsed, "wrapper_log_path": str(wrapper_log)})
    latex_log = BUILD_DIR / f"{output_job_name(args.company, args.role)}.log"
    emit({
        "ok": False,
        "returncode": result.returncode,
        "error_summary": summarize_error(combined),
        "relevant_log_path": str(latex_log if latex_log.exists() else wrapper_log),
        "wrapper_log_path": str(wrapper_log),
        **parsed,
    }, result.returncode if result.returncode else 1)


def reset_baseline(_args):
    set_active_role("baseline")
    emit({"ok": True, "active_role": "baseline"})


def main():
    parser = argparse.ArgumentParser(description="Local resume workflow helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init-job")
    p.add_argument("--company", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--jd-file", required=True)
    p.set_defaults(func=init_job)

    p = sub.add_parser("prepare-context")
    p.add_argument("--role-key", required=True)
    p.set_defaults(func=prepare_context)

    p = sub.add_parser("activate")
    p.add_argument("--role-key", required=True)
    p.set_defaults(func=activate)

    p = sub.add_parser("build")
    p.add_argument("--company", required=True)
    p.add_argument("--role", required=True)
    p.add_argument("--require-one-page", action="store_true", default=True)
    p.set_defaults(func=build)

    p = sub.add_parser("reset-baseline")
    p.set_defaults(func=reset_baseline)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
