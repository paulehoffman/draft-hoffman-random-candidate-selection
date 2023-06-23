#!/usr/bin/env python3

# Program to randomly select some candidates from a group
#  See draft-hoffman-genarea-reandom-candidate-selection

import hashlib, sys
from pathlib import Path

# Helper function to turn a UTF-8 string into its hex representation
def hexify(in_str):
  return "".join([hex(c)[2:] for c in in_str.encode("utf8")])

# Santity check the input files given on the command line
if len(sys.argv) == 1:
  exit("Must give the name of the candidate file, and possibly " + \
    "the selection file, on the command line. Exiting.")
candidate_path = Path(sys.argv[1])
if not candidate_path.exists():
  exit(f"The file {str(candidate_path)} does not exist. Exiting.")
try:
  candidate_f = candidate_path.open(mode="rt", encoding="utf8")
except:
  exit("The candidates file do not appear to be in UTF-8. Exiting.")
candidate_lines = candidate_f.read().splitlines()
# See if there is a second file for selecting
if len(sys.argv) == 3:
  run_including_selection = True
  selection_path = Path(sys.argv[2])
  if not selection_path.exists():
    exit(f"The file {str(selection_path)} does not exist. Exiting.")
  try:
    selection_f = selection_path.open(mode="rt", encoding="utf8")
  except:
    exit("The selection file does not appear to be UTF-8. Exiting.")
  selection_lines = selection_f.read().splitlines()
  # Extract D and S from the selection file
  S_str = selection_lines[0]
  try:
    S = int(S_str)
  except:
    print(f"The first line of the selection file, '{S_str}', " + \
      "is not an integer. Exiting.")
  D_str = selection_lines[1]
  D_hex = hexify(D_str)
else:
  run_including_selection = False

# Get the candidates information
C_info = []
for C_str in candidate_lines:
  C_hex = hexify(C_str)
  if run_including_selection:
    C_with_D_str = C_str + D_str
    C_with_D_hex = hexify(C_with_D_str)
    C_with_D_hash = hashlib.sha256(C_with_D_hex.encode("utf-8"))
    C_info.append([C_str, C_hex, C_with_D_str, C_with_D_hex, \
      C_with_D_hash.hexdigest()])
  else:
    C_info.append([C_str, C_hex])

# Print the results
if run_including_selection:
  print(f"S is {S}")
  print(f"D is \"{D_str}\"")
  print(f" U+{D_hex}\n")
  print("Candidate information, sorted by hash of name including D")
  selected = []
  for this_info in sorted(C_info, key=lambda a: a[4], reverse=True):
    if S > 0:
      selected.append(this_info[0])
      S -= 1
    print(f"{this_info[2]}")
    print(f" U+{this_info[3]}")
    print(f" {this_info[4]}")
  print("\nSelected:\n    " + "\n    ".join(selected))
else:
  for this_info in C_info:
    print(f"{this_info[0]}")
    print(f" U+{this_info[1]}")
