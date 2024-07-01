import pandas as pd
from __global_paths import *

df = pd.read_csv(SEPARATED_FILTERED_REPOS_PATH)

cols = ['grep_results0',
        'grep_results1',
        'grep_results2',
        'grep_results3',
        'grep_results4',
        'grep_results5',
        'grep_results6',
        'grep_results7'
        ]
counts = df[cols].sum()

print(f"""
Datetime:     {counts[cols[0]]}
Arrow:        {counts[cols[1]]}
Pendulum:     {counts[cols[2]]}
Maya:         {counts[cols[3]]}
Delorean:     {counts[cols[4]]}
Moment:       {counts[cols[5]]}
Whenever:     {counts[cols[6]]}
Heliclockter: {counts[cols[7]]}
"""
)
