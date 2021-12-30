from data.app import start
import yaml

with open('config.yaml', 'r') as stream:
    settings = yaml.safe_load(stream)

def main():
    start()

if __name__ == '__main__':
    main()
