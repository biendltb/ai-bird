import sys
sys.path.insert(0, '/Users/biendltb/Desktop/Data/projects/ai_bird/src/GameInterface')

from EnvObserver import EnvObserver


def get_env_params():
    env = EnvObserver()
    env.scr_capture()

def main():
    get_env_params()
    return

if  __name__ == "__main__":
    main()