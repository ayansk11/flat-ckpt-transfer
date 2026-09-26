import re, shutil, sys
def patch(path, subs):
    s = open(path).read()
    shutil.copy(path, path + ".preflat.bak")
    tot = 0
    for pat, rep in subs:
        s, c = re.subn(pat, rep, s)
        print("  %s: %r -> %d" % (path.split("/")[-1], pat[:34], c))
        tot += c
    open(path, "w").write(s)
    return tot
AG = "/root/red-agent/CybORG/adversary/core/agent.py"
RPS = "/root/red-agent/scripts/red_policy_service.py"
n = patch(AG, [
    (r'raise RuntimeError\("LLM planner required[^"]*"\)',
     'return self._heuristic_plan(shared_state), {"heuristic": True}'),
])
n += patch(RPS, [
    (r'choices=\[\s*"llm"\s*,\s*"rules"\s*,\s*"smoke"\s*\]',
     'choices=["llm", "rules", "smoke", "flat"]'),
    (r'use_llm_planner=True,', 'use_llm_planner=(self.planner != "flat"),'),
    (r'use_intent_conditioning=True,', 'use_intent_conditioning=(self.planner != "flat"),'),
    (r'if self\.planner == "llm":', 'if self.planner in ("llm", "flat"):'),
])
print("TOTAL SUBS: %d (expect 5)" % n)
sys.exit(0 if n == 5 else 2)
