import random

RANDOM = 0
DISTRIBUTE_HOT = 1
HOT_TOGETHER = 2

LABELS = {RANDOM: "Random", DISTRIBUTE_HOT: "Distrubute Hot", HOT_TOGETHER: "Hot Together"}

class DNAStorage:

	def __init__(self, years, grouping, blocks_per_pool, n_samples, resynth_threshold, resynth_samples, zipf20, writes, seed, n_samples_hot, resynth_samples_hot):
		# random.seed(seed)

		''' block_pools[block] = pool '''
		self.block_pools = [None] * len(writes)

		''' pools[pool] = [blocks] '''
		self.pools = [] 

		### CONSTANTS ###
		self.zipf20 = zipf20
		self.resynth_threshold = resynth_threshold
		self.resynth_samples = resynth_samples
		self.resynth_samples_hot = resynth_samples_hot

		print("*** CONFIG: ", blocks_per_pool, LABELS[grouping], "N_SAMPLES_HOT =", n_samples_hot, "***")

		self.write(grouping, writes, blocks_per_pool)

		# Start all blocks with same number of samples 
		self.block_samples = [n_samples] * len(writes)
		
		self.hot_blocks_and_cold_neighbors = set()
		if n_samples_hot:

			for block in zipf20:
				for neighbour in self.pools[self.block_pools[block]]:
					self.hot_blocks_and_cold_neighbors.add(neighbour)

			# change number of samples for blocks residing in pools with hot blocks
			for block in self.hot_blocks_and_cold_neighbors:
				self.block_samples[block] = n_samples_hot


		### STATS ###
		self.block_reads = [0] * len(writes)
		self.rebuild_requests = [0] * years



	def write(self, grouping, all_blocks, blocks_per_pool):
		n_blocks = len(all_blocks)
		n_zipf20 = len(self.zipf20)

		# we rely on in-order pop() in population step
		if grouping == HOT_TOGETHER:
			# just put zipf20 blocks to the tail, since pools are populated in order
			print("zipf20")
			remaining80 = list(set(all_blocks) - set(self.zipf20))
			shuffled_blocks = random.sample(remaining80, k=n_blocks - n_zipf20) + random.sample(self.zipf20, k=n_zipf20)

		elif grouping == DISTRIBUTE_HOT:
			# TODO: Refactor
			hot = random.sample(self.zipf20, k=n_zipf20)

			remaining80 = list(set(all_blocks) - set(self.zipf20))
			cold = random.sample(remaining80, k=n_blocks - n_zipf20)

			cold_per_hot = (n_blocks - n_zipf20) // n_zipf20

			shuffled_blocks = []
			while cold:
				for _ in range(cold_per_hot):
					shuffled_blocks.append(cold.pop())
				if hot:
					shuffled_blocks.append(hot.pop())

			while hot:
				shuffled_blocks.append(hot.pop())

		else:
			# assert not zipf20
			shuffled_blocks = random.sample(all_blocks, k=n_blocks)
		assert(len(shuffled_blocks) == n_blocks)
		# print("shuffled_blocks", shuffled_blocks)

		''' Populating pools '''
		while shuffled_blocks:
			new_pool = len(self.pools) # index of the last element

			self.pools.append(list())

			is_last_block_hot = False

			for j in range(blocks_per_pool):
				# if we have finished all hot blocks, don't fill it with cold blocks, move to next pool
				if grouping == HOT_TOGETHER and ((is_last_block_hot and shuffled_blocks[-1] not in self.zipf20) or not shuffled_blocks):
					break

				new_block = shuffled_blocks.pop()

				if new_block in self.zipf20:
					is_last_block_hot = True

				self.block_pools[new_block] = new_pool
				self.pools[new_pool].append(new_block)
			assert len(self.pools[new_pool]) == blocks_per_pool or grouping == HOT_TOGETHER, f"{len(pools[new_pool])} {BLOCKS_PER_POOL}"
			# print("pool", new_pool, pools[new_pool])

		for i in range(len(self.pools)):
				c = 0
				for block in self.pools[i]:
					if block in self.zipf20:
						c += 1
				print("pool", i, "has", c, "hot blocks out of total", len(self.pools[i]))
			# print(block_pools)

	def read(self, year, block):
	
		for neighbour in self.pools[self.block_pools[block]]:
			self.block_samples[neighbour] -= 1
			self.block_reads[neighbour] += 1						

			if self.block_samples[neighbour] <= self.resynth_threshold:
				if self.resynth_samples:
					# Now that samples are resynthesized, number of samples never reach 0, so plot with number of samples is useless?
					if self.resynth_samples_hot and neighbour in self.hot_blocks_and_cold_neighbors:
						self.block_samples[neighbour] += self.resynth_samples_hot
					else:
						self.block_samples[neighbour] += self.resynth_samples
				else:
					assert False, "resynth_samples is not set"
				self.rebuild_requests[year] += 1