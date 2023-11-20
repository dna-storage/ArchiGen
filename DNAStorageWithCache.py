import random
from DNAStorage import *

HOT_ONLY = 2
assert HOT_ONLY != True

RANDOM = 0 # conflict with RANDOM placement policy constant
LRU = 1
TWO_LRU = 2

CACHE_LABELS = {False: "no cache", True: "cache", HOT_ONLY: "cache hot_only"}

class DNAStorageWithCache(DNAStorage):

	def update_lru(self, hit_index):
		hit_lru = self.read_cache_lru[hit_index]
		for i in range(len(self.read_cache_lru)):
			if i == hit_index:
				self.read_cache_lru[i] = 0
			elif self.read_cache_lru[i] <= hit_lru:
				self.read_cache_lru[i] += 1

	def increment_lru(self, replace_index):
		for i in range(len(self.read_cache_lru)):
			if i != replace_index:
				self.read_cache_lru[i] += 1

	def __init__(self, years, grouping, blocks_per_pool, n_samples, resynth_threshold, resynth_samples, zipf20, writes, seed, n_samples_hot, resynth_samples_hot, cache_mode, cache_size):
		super().__init__(years, grouping, blocks_per_pool, n_samples, resynth_threshold, resynth_samples, zipf20, writes, seed, n_samples_hot, resynth_samples_hot)
		
		TOTAL_CACHE_SIZE = cache_size
		
		self.read_cache = cache_mode
		self.READ_CACHE_SIZE = cache_size

		# write_cache = cache
		self.write_cache = False
		self.WRITE_CACHE_SIZE = TOTAL_CACHE_SIZE - self.READ_CACHE_SIZE
		# write_cache = WRITE_CACHE_SIZE > 0

		# oracle
		self.READ_CACHE_HOT_ONLY = cache_mode == HOT_ONLY
		self.WRITE_CACHE_HOT_ONLY = False
		
		self.CACHE_REPLACEMENT_POLICY = LRU

		print("*** CONFIG: read_cache", self.read_cache, "cache_size", self.READ_CACHE_SIZE, "***")


		# Following for read cache
		self.read_cache_block = [-1] * self.READ_CACHE_SIZE
		self.read_cache_lru = [i for i in range(self.READ_CACHE_SIZE)]
		
		self.write_cache_block = [-1] * self.WRITE_CACHE_SIZE

		self.read_set = set()

		### STATS ###
		self.total_accesses = 0
		self.hits = 0
		self.write_hits = 0
		self.hot_hits = 0
		self.cold_hits = 0

		### Shoud be part of write() method, but we don't model year-to-year writes yet ###
		if self.write_cache:
			# this will mostly leave lastest block in the cache?
			# for block in writes:
			# 	install = True
			# 	# RANDOM replacement policy for now
			# 	evicted = random.sample(range(WRITE_CACHE_SIZE), k=1)[0]
				
			# 	if install:
			# 		write_cache_block[evicted] = block

			if self.WRITE_CACHE_HOT_ONLY:
				self.write_cache_block = random.sample(zipf20, k=self.WRITE_CACHE_SIZE)
			else:
				self.write_cache_block = random.sample(writes, k=self.WRITE_CACHE_SIZE)
		print("write_cache", self.write_cache_block)

	def read(self, year, block):
		self.total_accesses += 1
		if self.write_cache and block in self.write_cache_block:
			self.write_hits += 1
		elif self.read_cache and block in self.read_cache_block:
			self.hits += 1

			if block in self.zipf20:
				self.hot_hits +=1
			else:
				self.cold_hits += 1

			if self.CACHE_REPLACEMENT_POLICY == LRU or self.CACHE_REPLACEMENT_POLICY == TWO_LRU:
				hit_index = self.read_cache_block.index(block)
				self.update_lru(hit_index)
		else:
			super().read(year, block)

			# we cache only one block (only it is amplified out of whole pool)
			if self.read_cache and (not self.READ_CACHE_HOT_ONLY or block in self.zipf20):
				install = True
				if self.CACHE_REPLACEMENT_POLICY == LRU:
					evicted = self.read_cache_lru.index(max(self.read_cache_lru))
					# updating lru
					self.read_cache_lru[evicted] = 0
					self.increment_lru(evicted)
					
				elif self.CACHE_REPLACEMENT_POLICY == TWO_LRU:
					assert 0, "Check TWO_LRU implementation"
					if block in self.read_set:
						evicted = self.read_cache_lru.index(max(self.read_cache_lru))
						# updating lru
						read_cache_lru[evicted] = 0
						self.increment_lru(evicted)
						
						self.read_set.remove(block)
					else:
						# first read
						self.read_set.add(block)													
						install = False
				else:
					evicted = random.sample(range(self.READ_CACHE_SIZE), k=1)[0]
				
				if install:
					self.read_cache_block[evicted] = block


