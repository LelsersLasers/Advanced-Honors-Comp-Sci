"""
	Description: proof its half even/odd swaps for Sienna
	Author: Millan Kumar
	Date: 12/08/2023
"""

def permutations(n):
	"""returns a list of permutations of the numbers 1 to n"""
	if n == 1:
		return [[1]]
	else:
		perms = []
		for perm in permutations(n - 1):
			for i in range(n):
				perms.append(perm[:i] + [n] + perm[i:])
		return perms
	
def count_swaps(perm):
	"""returns the smallest number of swaps required to sort a permutation"""
	n = len(perm)
	visited = [False] * n
	swaps = 0
	for i in range(n):
		if not visited[i]:
			j = i
			cycle_size = 0
			while not visited[j]:
				visited[j] = True
				j = perm[j] - 1
				cycle_size += 1
			swaps += cycle_size - 1
	return swaps

def main():
	perms = permutations(4)
	print(f"Number of permutations: {len(perms)}")

	swaps = [count_swaps(perm) for perm in perms]
	swaps_dict = {}
	for i in range(len(perms)):
		swaps_dict[swaps[i]] = swaps_dict.get(swaps[i], 0) + 1
	swaps_dict = dict(sorted(swaps_dict.items(), key=lambda x: x[0]))

	print(f"Number of swaps: {swaps_dict}")

if __name__ == "__main__":
	main()