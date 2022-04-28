# Bombus Simulator

## Requirements

* Keras
* pygame
* matplotlib
* numpy

## Usage

run `main_simulator.py`

## Simulator Intro

To automatically controll and optimize bombus flying, we use __reinforcement learning__ to train the model. The optimizing algorithm we use is __deep Q-Learning__ based on Keras or Pytorch. Besides, to visualize the progress, we use pygame to vividly show the simulator process and matplotlib to display the optimizing result of every epoch.

## File Intro

* `Model` saved dnn model
* `game.py` pygame section
* `main_simulator.py` run file
* `Map_generator.py` generate items and elements used in pygame
* `Model_keras.py` some DNNs embedded in deep Q-Learning, keras version
* `Model_torch` torch version
* `RL.py` reinforcement learning section
* `utils.py` some functions used in other files
