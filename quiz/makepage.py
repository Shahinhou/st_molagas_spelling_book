import sys

def boiler(file):
    with open(file, 'w') as f:
        f.write('<html>\n<head>\n<title>Results</title>\n</head>\n<body>\n\n\n<h1>Results:</h1>\n')

def closer(file):
    with open(file, 'a') as f:
        f.write('</body>\n</html>\n')

def main():
    boiler(sys.argv[1])

if __name__=='__main__':
    main()
