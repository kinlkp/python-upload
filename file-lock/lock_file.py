import fcntl
import time

"""
process 1
"""

file="/tmp/abc.txt"

with open(file, "a") as f:
  fcntl.flock(f.fileno(), fcntl.LOCK_EX)
  f.write("1\n")
  print("sleep 10")
  time.sleep(10)
  fcntl.flock(f.fileno(), fcntl.LOCK_UN)

"""
process 2
"""

with open(file, "a") as f:
  fcntl.flock(f.fileno(), fcntl.LOCK_EX)
  f.write("2\n")
  print("sleep 10")
  time.sleep(10)
  fcntl.flock(f.fileno(), fcntl.LOCK_UN)
