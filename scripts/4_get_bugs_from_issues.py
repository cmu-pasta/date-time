from __global_paths import *
import subprocess

subprocess.run(f"head -n 1 {ISSUES_PATH} > {BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
subprocess.run(f"grep -E '(bug|fix|wrong)' {ISSUES_PATH} >> {BUGS_PATH}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)