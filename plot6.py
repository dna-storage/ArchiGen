import matplotlib.pyplot as plt
import pandas as pd

from plot_common import *

def stats(rebuild_requests):
	time_to_first_rebuild = min(y for y in range(len(rebuild_requests)) if rebuild_requests[y] > 0)
	if time_to_first_rebuild == None:
		time_to_first_rebuild = -1

	total_rebuilt_blocks = rebuild_requests[-1]

	return time_to_first_rebuild, total_rebuilt_blocks

# fig3, ax = plt.subplots(figsize=(2*ONE_COL_WIDTH, 5))
fig, ax = plt.subplots()

df = pd.read_csv("fig6_rebuild_requests.csv")
df.columns=["Year", "0.5% C + R", "0.5% C + DH", "0.5% C + HT", "0.5% C + R (HO)", r"0.5% C + HT $8 \times$", "1.0% C + R"]

df.drop(["0.5% C + R (HO)"], axis=1).plot(ax=ax, x=0, logy=True, style=[None, '--', '--', '--', None])


ax.set(ylabel='Rebuilt Blocks')

# ax1.set_title('(A)')
# ax2.set_title('(B)')
# ax3.set_title('(C)')
ax.legend()
ax.set_yscale('symlog')
# ax.set_ylim(-1)

plt.tight_layout(pad=0.25)

fig.figure.savefig("fig6.pdf")

# for rebuild_requests in [
# 							rebuild_requests_random_cache_05_mean,
# 							rebuild_requests_distribute_hot_cache_mean,
# 							rebuild_requests_hot_together_cache_mean,
# 							rebuild_requests_hot_together_8x_cache_mean,
# 							rebuild_requests_random_cache_hot_only_mean,
# 							rebuild_requests_random_cache_1_mean
# 						]:
# 	print(stats(rebuild_requests))