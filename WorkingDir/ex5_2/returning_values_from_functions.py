# returning_values_from_functions.py

def parse_line(line):

    if not '=' in line:
        return None

    return tuple(line.split('='))


def main():
    
    result_tuple = parse_line('email=guido@python.org')
    print(result_tuple)

if __name__ == '__main__':
    main()