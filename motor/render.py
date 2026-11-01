"""Shared helpers: easing, colour mix and a tiny Python syntax tokenizer (VS Code Dark+ colours)."""
import re
SYN = {"kw": (197, 134, 192), "str": (206, 145, 120), "fn": (220, 220, 170), "var": (156, 220, 254),
       "num": (181, 206, 168), "const": (86, 156, 214), "p": (212, 212, 212)}
def cl(x, a=0.0, b=1.0): return max(a, min(b, x))
def pr(t, a, d=0.35): return cl((t - a) / d)
def eo(x): return 1 - (1 - x) ** 3
def eback(x, s=1.7):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1
def mix(c, bg, a): return tuple(int(bg[i] + (c[i] - bg[i]) * a) for i in range(3))
TOK = re.compile(r"(f?'[^']*'|f?\"[^\"]*\")|(\b(?:import|as|from|def|return|and|or|not|for|in|if|elif|else|while|lambda|with|class|is|None|yield|on|SELECT|FROM|WHERE|LEFT|RIGHT|INNER|JOIN|ON|GROUP|ORDER|BY|DESC|ASC|AS|HAVING|LIMIT|WITH|COUNT|SUM|AND|OR)\b)|(\b(?:True|False)\b)|(\b\d+(?:\.\d+)?\b)|(\b[A-Za-z_]\w*(?=\())|(\b[A-Za-z_]\w*\b)|(\s+)|(.)")
def tokens(line):
    out = []
    for m in TOK.finditer(line):
        s = m.group(0)
        k = "str" if m.group(1) else "kw" if m.group(2) else "const" if m.group(3) else "num" if m.group(4) else \
            "fn" if m.group(5) else "var" if m.group(6) else "p"
        out.append((s, SYN[k]))
    return out
