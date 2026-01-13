from playground.engine.loop import load_scene, run_engine
from playground.scenes.brownian.scene import BrownianScene

if __name__ == "__main__":
    load_scene(BrownianScene)
    run_engine()