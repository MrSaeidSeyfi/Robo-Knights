# Robo-Knights

A Chess Reinforcement Learning Framework

## Overview

Robo-Knights is a Python-based framework for training and visualizing chess AI agents using reinforcement learning. The project implements an actor-critic architecture for chess agents and provides tools for training, visualization, and metrics tracking.


## Project Structure

```
Robo-Knights/
├── src/
│   └── robo_knights/
│       ├── agents/
│       │   ├── __init__.py
│       │   └── chess_agent.py      # Chess agent implementation
│       ├── environment/
│       │   ├── __init__.py
│       │   └── chess_env.py        # Chess environment
│       ├── models/
│       │   ├── __init__.py
│       │   └── actor_critic.py     # Actor-critic neural network
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── move_utils.py       # Chess move utilities
│       │   ├── visualization.py    # Chess board visualization
│       │   └── metrics.py          # Game metrics tracking
│       └── __init__.py
├── models/                         # Directory for saved agent models
├── pieces/                         # Chess piece images
├── logs/                          # Game logs and metrics
├── main.py                        # Main entry point
├── setup.py                       # Package setup file
```

## Usage

### Running the Project

The project supports three main modes of operation:

1. **Training Mode**
```bash
python main.py --mode train --episodes 100
```
This will train two agents against each other for the specified number of episodes and save their models.

2. **Play Mode**
```bash
python main.py --mode play --model1 models/agent1.pth --model2 models/agent2.pth
```
This will run a game between two agents using the specified model files.

3. **Visualization Mode**
```bash
python main.py --mode visualize --model1 models/agent1.pth --model2 models/agent2.pth
```
This will run a game with a graphical interface showing the chess board and moves.

### Model Management

- Models are saved in the `models/` directory
- Default model paths are `models/agent1.pth` and `models/agent2.pth`
- If a model file is not found, the system will automatically use a random agent instead
- You can use different models by specifying their paths with the `--model1` and `--model2` arguments
- To train new models, use the training mode and they will be saved automatically

Example of using custom model paths:
```bash
python main.py --mode play --model1 models/custom_agent.pth --model2 models/opponent.pth
```

## Results


https://github.com/user-attachments/assets/1c212c11-6c38-4bb9-9c30-2a69424a3db6


 
## Resources

- [Chess Piece Images](https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces)
- [The Actor-Critic Reinforcement Learning algorithm](https://medium.com/intro-to-artificial-intelligence/the-actor-critic-reinforcement-learning-algorithm-c8095a655c14)
