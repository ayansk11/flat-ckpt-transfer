import re
RPS = "/root/red-agent/scripts/red_policy_service.py"
s = open(RPS).read()
# FlatRL-C1 has an 11-way action type_head; F1.8 is 10. The deployed AgentConfig
# sets no num_action_types (defaults to 10, correct for F1.8/llm). Add a
# planner-conditional num_action_types so the flat policy loads its 11-way head.
pat = r'(use_multidiscrete_action=True,[^\n]*\n)'
rep = r'\1                num_action_types=(11 if self.planner == "flat" else 10),\n'
s, c = re.subn(pat, rep, s)
print("num_action_types add ->", c)
assert c == 1, "expected exactly 1 insertion"
open(RPS, "w").write(s)
import py_compile; py_compile.compile(RPS, doraise=True); print("compile OK")
