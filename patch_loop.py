import re, os, shutil
M = "/home/groups/usma_shared/scenarios/MARL_ayan/AI-SOAR4ZT/MARL4Safe-SOAR"
src = M + "/util/collect_loop_redobs.sh"
dst = M + "/util/collect_loop_flatrl.sh"
s = open(src).read()
tot = 0
subs = [
    (r'DATA=collected_data_redobs_q35_08b', 'DATA=collected_data_flatrl_c1'),
    (r'ARM=redobs_q35_08b', 'ARM=flatrl_c1'),
    (r'CKPT=deploy_checkpoints/F1\.8/F1\.8-Qwen3-RL-MultiDiscrete_final\.pt',
     'CKPT=deploy_checkpoints/FlatRL/FlatRL-C1_step_2000.pt'),
    (r'--planner llm', '--planner flat'),
    (r'(wait_llm_ok\(\) \{[^\n]*\n)', r'\1    return 0  # flat-RL: no LLM planner needed\n'),
]
for pat, rep in subs:
    s, c = re.subn(pat, rep, s)
    print("  %r -> %d" % (pat[:36], c))
    tot += c
open(dst, "w").write(s)
os.chmod(dst, 0o755)
print("WROTE", dst)
print("TOTAL: %d (expect 5)" % tot)
