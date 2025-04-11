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

## Resources

- [Chess Piece Images](https://commons.wikimedia.org/wiki/Category:SVG_chess_pieces)
- [The Actor-Critic Reinforcement Learning algorithm](https://medium.com/intro-to-artificial-intelligence/the-actor-critic-reinforcement-learning-algorithm-c8095a655c14)
