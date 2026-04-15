"""Utilities for reading TLE files from CelesTrak.

Step 2: read and group TLE records (name, line1, line2).
"""
from typing import List, Dict, Optional


def read_tle_file(path: str) -> List[Dict[str, Optional[str]]]:
	"""Read a TLE file and return a list of entries.

	Each entry is a dict: {'name': Optional[str], 'line1': str, 'line2': str}.

	The function is robust to files that either include the satellite name
	(3-line blocks) or only contain the two TLE lines per satellite.
	"""
	entries: List[Dict[str, Optional[str]]] = []
	with open(path, "r", encoding="utf-8") as fh:
		raw_lines = [ln.rstrip('\n') for ln in fh]

	# remove purely empty lines but keep spacing-aware order
	lines = [ln for ln in (l.strip() for l in raw_lines) if ln != ""]

	i = 0
	n = len(lines)
	while i < n:
		# Case: two-line TLE starting with '1 ' and '2 '
		if lines[i].startswith('1 ') and i + 1 < n and lines[i+1].startswith('2 '):
			entries.append({'name': None, 'line1': lines[i], 'line2': lines[i+1]})
			i += 2
			continue

		# Case: three-line block: name, line1, line2
		if i + 2 < n and not lines[i].startswith(('1 ', '2 ')) and lines[i+1].startswith('1 ') and lines[i+2].startswith('2 '):
			entries.append({'name': lines[i], 'line1': lines[i+1], 'line2': lines[i+2]})
			i += 3
			continue

		# If we reach here, the file has an unexpected line; try to recover by skipping one line
		# This helps handle occasional headers or comments in CelesTrak dumps.
		i += 1

	return entries


if __name__ == '__main__':
	import sys

	if len(sys.argv) < 2:
		print('Usage: python dataHandling.py <tle-file>')
		sys.exit(1)

	tle_path = sys.argv[1]
	entries = read_tle_file(tle_path)
	print(f'Read {len(entries)} TLE entries from {tle_path}')
	if entries:
		e = entries[0]
		print('First entry:')
		print('Name:', e['name'])
		print('Line1:', e['line1'])
		print('Line2:', e['line2'])

