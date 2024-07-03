import pandas as pd
from __global_paths import *

df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)

cols = ['grep_results0',
        'grep_results1',
        'grep_results2'
        ]
counts = df[cols].sum()

print(f"""
Datetime:     {counts[cols[0]]}
Arrow:        {counts[cols[1]]}
Pendulum:     {counts[cols[2]]}
"""
)
