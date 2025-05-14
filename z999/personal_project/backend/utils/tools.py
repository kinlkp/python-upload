import re

def match_regex(pattern, source):
    result = re.match(pattern, source)
    return result

def print_exception(path, err):
    print(f"Exception raised at {path}: {repr(err)}")