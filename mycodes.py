from data.app import start
import ctypes
# import yaml

# with open('config.yaml', 'r') as stream:
#     settings = yaml.safe_load(stream)

ctypes.windll.shcore.SetProcessDpiAwareness(1)

def main():
    start()

if __name__ == '__main__':
    main()
