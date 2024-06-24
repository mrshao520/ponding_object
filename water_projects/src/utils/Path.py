import sys
import os

# 绝对路径
current_path, filename = os.path.split(os.path.abspath(sys.argv[0]))
current_path = current_path.replace('\\', '/')