# Playground
Just a simple playground to quickly render something and try out something you want to simulate.
> WIP: Still need to integrate a physics engine and asset loading

# Setup
- Make sure you have Python installed, then just run:
```bash
pip install venv
python -m venv venv
./venv/Scripts/activate
```

# Usage
## 1. To Create a New Scene:
```bash
python -m create_scene test
```
Your scene will be created in `playground/scenes/test`

## 2. Edit scene.py:
You can modify and create the scene as you wish in `scene.py`

## 3. Run the scene:
Import the scene and load it in the main function in `main.py`. You can load multiple scenes to play after each other in the specified order.
```python
from playground.engine.loop import load_scene, run_engine
from playground.scenes.test.scene import TestScene

if __name__ == "__main__":
    load_scene(TestScene)
    run_engine()
```
Then run:
```bash
python -m playground.main
```
