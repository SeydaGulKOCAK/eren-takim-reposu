import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/beyza/eren-takim-reposu/install/my_swarm_pkg'
