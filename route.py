#!/usr/bin/env python3
"""inference-hub router — providers/*.md を読み、capability で選ぶ。実行はしない。

stdlib only. 使い方:
    python3 route.py list [--capability C] [--viable-only]
    python3 route.py pick --capability C [--max-ram-gb N] [--prefer local|remote]
    python3 route.py show <name>
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROVIDERS = HERE / "providers"


def parse_frontmatter(text: str) -> dict:
    """`---` で囲まれた key: value ブロックだけを読む。yaml 非依存。

    値は str / list(str) / bool / int に正規化する。
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    out: dict = {}
    key = None
    for raw in lines[1:]:
        if raw.strip() == "---":
            break
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t", "-")) and key:
            # ネスト/配列の継続行
            val = raw.strip().lstrip("-").strip()
            if isinstance(out.get(key), list):
                out[key].append(_cast(val))
            continue
        if ":" not in raw:
            continue
        k, v = raw.split(":", 1)
        key = k.strip()
        v = v.strip()
        if v == "":
            out[key] = []
        elif v.startswith("[") and v.endswith("]"):
            out[key] = [_cast(x.strip().strip("'\"")) for x in v[1:-1].split(",") if x.strip()]
        else:
            out[key] = _cast(v.strip("'\""))
    return out


def _cast(v: str):
    low = v.lower()
    if low in ("true", "yes"):
        return True
    if low in ("false", "no"):
        return False
    try:
        return int(v)
    except ValueError:
        return v


def load() -> list[dict]:
    if not PROVIDERS.is_dir():
        return []
    items = []
    for path in sorted(PROVIDERS.glob("*.md")):
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta.get("name"):
            continue
        meta["_path"] = str(path)
        meta["capability"] = meta.get("capability") or []
        meta["viable"] = bool(meta.get("viable", False))
        items.append(meta)
    return items


def _caps(p: dict) -> set[str]:
    c = p.get("capability")
    if isinstance(c, str):
        return {c}
    return set(c or [])


def cmd_list(args) -> int:
    rows = load()
    if args.capability:
        rows = [p for p in rows if args.capability in _caps(p)]
    if args.viable_only:
        rows = [p for p in rows if p["viable"]]
    if not rows:
        print("(該当なし)")
        return 1
    for p in rows:
        mark = "OK " if p["viable"] else "NG "
        print(f"{mark}{p['name']:<18} {','.join(sorted(_caps(p))):<22} "
              f"on={p.get('runs_on','?'):<7} ram>={p.get('min_ram_gb','?')}GB  {p.get('title','')}")
        if not p["viable"] and p.get("blocked_reason"):
            print(f"    └ {p['blocked_reason']}")
    return 0


def cmd_pick(args) -> int:
    rows = [p for p in load() if p["viable"] and args.capability in _caps(p)]
    if args.max_ram_gb is not None:
        rows = [p for p in rows if int(p.get("min_ram_gb") or 0) <= args.max_ram_gb]
    if args.prefer:
        want = args.prefer
        rows = [p for p in rows if p.get("runs_on") == want] or rows
    if not rows:
        print(f"capability={args.capability} で実行可能な provider は無い。")
        print("→ providers/*.md を確認するか、route.py list で block 理由を見る。")
        return 1
    # local 優先（latency/コスト）、同条件なら min_ram_gb 昇順
    rows.sort(key=lambda p: (0 if p.get("runs_on") == "local" else 1, int(p.get("min_ram_gb") or 0)))
    best = rows[0]
    print(f"pick: {best['name']}")
    print(f"  on={best.get('runs_on')}  endpoint={best.get('endpoint','-')}")
    print(f"  delegate={best.get('delegate','-')}")
    if best.get("startup"):
        print(f"  startup: {best['startup']}")
    if best.get("reachability"):
        print(f"  reachability: {best['reachability']}")
    if len(rows) > 1:
        print(f"  alt: {', '.join(p['name'] for p in rows[1:])}")
    return 0


def cmd_show(args) -> int:
    for p in load():
        if p["name"] == args.name:
            print(Path(p["_path"]).read_text(encoding="utf-8"))
            return 0
    print(f"unknown provider: {args.name}", file=sys.stderr)
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(prog="route.py")
    sub = ap.add_subparsers(dest="cmd", required=True)

    l = sub.add_parser("list")
    l.add_argument("--capability")
    l.add_argument("--viable-only", action="store_true")
    l.set_defaults(fn=cmd_list)

    p = sub.add_parser("pick")
    p.add_argument("--capability", required=True)
    p.add_argument("--max-ram-gb", type=int)
    p.add_argument("--prefer", choices=["local", "remote"])
    p.set_defaults(fn=cmd_pick)

    s = sub.add_parser("show")
    s.add_argument("name")
    s.set_defaults(fn=cmd_show)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
