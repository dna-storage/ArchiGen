import matplotlib.pyplot as plt
import pandas as pd

from plot_common import *

# python3.11 sim.py zipf1_80/zipf1_80_hint.txt fig1 zipf1_80/zipf1_80_hint.txt
N_SAMPLES = 200

fig, ax = plt.subplots()

df = pd.read_csv("fig3_block_reads.csv")
df.columns=["Block ID", "Low-Density System", "Medium-Density System", "High-Density System"]
df.plot(ax=ax, x=0)

ax.set(xlabel='Block ID (sorted from most to least accessed)', ylabel='Total Reads')
# ax.set_xticklabels([])
ax.axhline(y=N_SAMPLES, ls='--', linewidth=0.5, color=new_black) #, label="Initial # of copies"

ax.legend()
# ax.set_yscale('log')

plt.tight_layout(pad=0.25)
fig.figure.savefig("fig3a.pdf")

###############################################################################

fig, ax = plt.subplots()

df = pd.read_csv("fig3_rebuild_requests.csv")
df.columns=["Year", "Low-Density System", "Medium-Density System", "High-Density System"]

df.plot(ax=ax, x=0, logy=True)

# ax.set_box_aspect(1) # makes plot square

ax.set(xlabel='Year', ylabel='Rebuilt Blocks')
ax.legend()
ax.set_yscale('symlog')
# ax.set_ylim(-1)

plt.tight_layout(pad=0.25)

fig.figure.savefig("fig3b.pdf")