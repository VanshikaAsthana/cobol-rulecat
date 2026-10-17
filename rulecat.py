import sys, json, re, os, pathlib, urllib.request

OLLAMA = "http://localhost:11434/api/generate"
MODEL = os.getenv("MODEL", "llama3.2")
CATALOG = "rules.json"
VERBS = ("MOVE","IF","EVALUATE","COMPUTE","PERFORM","ADD","SUBTRACT","MULTIPLY",
         "DIVIDE","STOP","DISPLAY","GO","END-","ELSE","WHEN")
CLOSE = {"IF": "END-IF", "EVALUATE": "END-EVALUATE"}

def load(path):
    out = []
    for n, raw in enumerate(pathlib.Path(path).read_text().splitlines(), 1):
        if raw[6:7] in ("*", "/"):
            continue
        out.append((n, raw[7:72].rstrip()))
    return out

def explain(code):
    prompt = ("Explain this COBOL business rule in 1-2 plain-English sentences. "
              "Reply with ONLY the explanation, no introduction. Describe only what the code "
              "does; do not assume currency, units or what the variables represent. "
              "If the logic itself is ambiguous, start with 'UNCLEAR:'.\n\n" + code)
    try:
        body = json.dumps({"model": MODEL, "prompt": prompt, "stream": False}).encode()
        req = urllib.request.Request(OLLAMA, body, {"Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=120))["response"].strip()
    except Exception:
        return "(LLM offline) " + " ".join(code.split())

def flags(kind, code, expl):
    f = []
    if kind == "IF" and "ELSE" not in code: f.append("no ELSE branch")
    if kind == "EVALUATE" and "WHEN OTHER" not in code: f.append("no WHEN OTHER")
    if "GO TO" in code: f.append("uses GO TO")
    if kind == "COMPUTE" and "ROUNDED" not in code and re.search(r"[/*]", code):
        f.append("arithmetic without ROUNDED")
    if "UNCLEAR" in expl.upper(): f.append("LLM unsure")
    return f

def extract(path):
    L = load(path); rules = []; para = None; i = 0; in_proc = False
    while i < len(L):
        n, t = L[i]; s = t.strip()
        if s.startswith("PROCEDURE DIVISION"): in_proc = True
        elif in_proc and re.fullmatch(r"[A-Z0-9-]+\.", t):
            para = t[:-1]
        kind = next((k for k in ("IF", "EVALUATE", "COMPUTE") if s.startswith(k + " ")), None)
        if not in_proc or not kind:
            i += 1; continue
        j = i
        if kind in CLOSE:
            depth = 0
            while j < len(L):
                w = L[j][1].strip()
                if w.startswith(kind + " "): depth += 1
                if w.startswith(CLOSE[kind]): depth -= 1
                if depth <= 0: break
                j += 1
        else:
            while (not L[j][1].rstrip().endswith(".") and j + 1 < len(L)
                   and not L[j + 1][1].strip().startswith(VERBS)):
                j += 1
        code = "\n".join(x[1] for x in L[i:j + 1])
        expl = explain(code)
        rules.append({"id": f"R{len(rules)+1:03d}", "file": path, "paragraph": para,
                      "lines": f"{L[i][0]}-{L[j][0]}", "kind": kind, "code": code,
                      "explanation": expl, "flags": flags(kind, code, expl)})
        i = j + 1
    json.dump(rules, open(CATALOG, "w"), indent=2)
    print(f"{len(rules)} rules saved to {CATALOG}")
    for r in rules: show(r)

def show(r):
    flag = f"  ⚠ {', '.join(r['flags'])}" if r["flags"] else ""
    print(f"\n[{r['id']}] {r['paragraph']} lines {r['lines']}{flag}\n  {r['explanation']}")

def search(q):
    words = q.lower().split()
    rules = json.load(open(CATALOG))
    scored = [(sum(w in (r["explanation"] + r["code"] + str(r["paragraph"])).lower()
                   for w in words), r) for r in rules]
    for s, r in sorted(scored, key=lambda x: -x[0]):
        if s: show(r)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "extract": extract(sys.argv[2])
    elif cmd == "search": search(" ".join(sys.argv[2:]))
    else: print("usage: python rulecat.py extract <file.cbl> | search <query>")
