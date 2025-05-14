import argparse


def get_args():
    parse = argparse.ArgumentParser()
    parse.add_argument('--username', type=str, default=None)
    args = parse.parse_args()
    if not args.username:
        parse.print_help()
        exit()
        
    return args