import functools
import sys
import re

name = sys.argv[1]


with open(name) as f:
  stuff = f.read().splitlines();
  
#make it throw exception for 'q'
def yaynay(prompt, indent=0):
  while True:
    ans = input(f'{" "*indent}{prompt}  (y/n)\n{" "*indent}')
    if ans in ['y', 'n']:
      return ans == 'y'
    print('invalid answer')
  

cache = {}
try:
  with open(name + '_cache') as f:
    if yaynay('Answer cache found. Use it?'):
      for l in f.read().splitlines():
        fields = [x.replace(r'\ ', ' ') for x in re.findall(r'(?:\\ |[^ ])+', l)]
        x, y, v = fields
        cache[(x, y)] = int(v)
except FileNotFoundError:
  pass


def cmp(x, y):
  if (x, y) in cache:
    return cache[(x, y)]
  #return 1 if len(x) > len(y) else -1
  if yaynay(f'Is "{x}" easier than "{y}"?', 1):
    #v walrus?
    cache[(x, y)] = 1
    return 1
  cache[(x, y)] = -1
  return -1

for l in sorted(stuff, key=functools.cmp_to_key(cmp)):
  print(l)

if yaynay('Save answer cache?'):
  with open(name + '_cache', 'w') as f:
    rs = lambda x: x.replace(' ', r'\ ')
    for k, v in cache.items():
      x, y = k
      f.write(f'{rs(x)} {rs(y)} {v}\n')
  
  
  

