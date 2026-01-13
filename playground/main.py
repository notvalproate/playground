from playground.engine import load_scene, run_engine
from playground.scenes.brownian import BrownianScene

if __name__ == "__main__":
    load_scene(BrownianScene)
    run_engine()