from playground.engine import load_scene, run_engine
from playground.scenes.brownian import BrownianScene
from playground.scenes.cars import CarsScene

if __name__ == "__main__":
    # load_scene(BrownianScene)
    load_scene(CarsScene)
    run_engine()