import argparse

parser = argparse.ArgumentParser(description='Description of this program')
parser.add_argument('arg1', help='Help of arg1')
parser.add_argument('arg2', help='Help of arg2')
parser.add_argument('--arg3')
parser.add_argument('--arg4', '-a')

args = parser.parse_args()

print('arg1={}'.format(args.arg1))
print('arg2={}'.format(args.arg2))
print('arg3={}'.format(args.arg3))
print('arg4={}'.format(args.arg4))
