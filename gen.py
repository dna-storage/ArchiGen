import sys
import random

YEARS = 30
SEED = 5678
# SEED = 91011 # outside hint
READS_PER_YEAR = 500
N_BLOCKS = 10000

random.seed(SEED)

WRITES_PER_YEAR = 10000
WRITE_MAX_YEAR = 1

if len(sys.argv) < 3:
	print("Usage: output_file skew [scrubbing]")

YEARLY = 1
SCRUBBING = None
if len(sys.argv) == 4:
	assert(int(sys.argv[3]) == YEARLY)
	SCRUBBING = int(sys.argv[3])
	print("SCRUBBING =", SCRUBBING)

with open(sys.argv[1], "w") as f:
	if sys.argv[2] == "uniform":
		write_last = 0

		for y in range(YEARS):
			if y < WRITE_MAX_YEAR:
				print([], file=f)
				for _ in range(WRITES_PER_YEAR):
					print("w", write_last, "x", file=f)
					write_last += 1	

			for _ in range(READS_PER_YEAR):
				print("r", random.randrange(N_BLOCKS), file=f)
	else:
		a = 0.2
		if sys.argv[2] == "20/80":
			b = 0.8
		elif sys.argv[2] == "20/95":
			b = 0.95
		elif sys.argv[2] == "10/95":	
			a = 0.1
			b = 0.95
		elif sys.argv[2] == "15/80":	
			a = 0.15
			b = 0.80
		elif sys.argv[2] == "10/80":	
			a = 0.10
			b = 0.80
		elif sys.argv[2] == "5/80":	
			a = 0.05
			b = 0.80
		elif sys.argv[2] == "1/80":	
			a = 0.01
			b = 0.80
		else:
			print("error")
			exit(1)

		print(a, "fraction blocks generates", b, "fraction of reads")

		a_blocks = random.sample(range(N_BLOCKS), k=int(N_BLOCKS * a))
		remaining80 = list(set(range(N_BLOCKS)) - set(a_blocks))
		
		print("generating", N_BLOCKS, "blocks with", len(a_blocks), "hot and", len(remaining80), "cold")

		print("a_blocks", sorted(a_blocks))

		chosen_a_blocks = set()

		write_last = 0

		for y in range(YEARS):
			# f.write(f"YEAR={y}\n")
			if y < WRITE_MAX_YEAR:
				print("Year", y, "printing writes")
				print(a_blocks, file=f)
				for _ in range(WRITES_PER_YEAR):
					out = f"w {write_last} {'h' if write_last in a_blocks else 'c'}\n"
					f.write(out)
					
					write_last += 1	

			print("Year", y, "printing hot reads")
			for _ in range(int(READS_PER_YEAR * b)):
				choice = random.choice(a_blocks)
				chosen_a_blocks.add(choice)

				out = f"r {choice}\n"
				f.write(out)

			print("Year", y, "printing cold reads")
			for _ in range(READS_PER_YEAR - int(READS_PER_YEAR * b)):
				# doesn't consider blocks in a_blocks
				out = f"r {random.choice(remaining80)}\n"
				f.write(out)

			if SCRUBBING == YEARLY:
				print("Year", y, "printing scrubbing")
				for i in range(N_BLOCKS):
					out = f"s {i}\n"
					f.write(out)

			print()

		print("chosen_a_blocks", len(chosen_a_blocks) / len(a_blocks), chosen_a_blocks)

with open(sys.argv[1]) as f:
	real_lines = sum(1 for _ in f)
	projected_lines = YEARS * (READS_PER_YEAR) + WRITE_MAX_YEAR * (1 + WRITES_PER_YEAR) + YEARS * (N_BLOCKS if SCRUBBING == YEARLY else 0)
	assert real_lines == projected_lines, f"{real_lines} != {projected_lines}"