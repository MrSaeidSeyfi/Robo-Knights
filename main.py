#!/usr/bin/env python
"""
Robo-Knights: A Chess Reinforcement Learning Framework
Main entry point for the application.
"""

import argparse
import os
import sys
import time
import random
import torch
import chess
import pygame

from robo_knights.environment import ChessEnv
from robo_knights.utils import ChessVisualizer, MetricsTracker
from robo_knights.agents.chess_agent import ChessAgent

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Robo-Knights Chess AI")
    parser.add_argument("--mode", choices=["train", "play", "visualize"], 
                        default="play", help="Operation mode")
    parser.add_argument("--model1", type=str, default="models/agent1.pth",
                        help="Path to first agent model")
    parser.add_argument("--model2", type=str, default="models/agent2.pth",
                        help="Path to second agent model")
    parser.add_argument("--episodes", type=int, default=100,
                        help="Number of episodes for training")
    return parser.parse_args()

def create_random_agent():
    class RandomAgent:
        def select_action(self, state, legal_moves):
            return random.choice(list(legal_moves))
    return RandomAgent()

def train_agents(env, episodes=100):
    """Train chess agents."""
    print(f"Training agents for {episodes} episodes...")
    
    agent1 = ChessAgent()
    agent2 = ChessAgent()
    metrics = MetricsTracker()
    
    for episode in range(episodes):
        state = env.reset()
        metrics.start_game()
        done = False
        
        while not done:
            current_agent = agent1 if env.board.turn else agent2
            legal_moves = list(env.board.legal_moves)
            
            if legal_moves:
                move = current_agent.select_action(state, legal_moves)
                if move in legal_moves:
                    metrics.log_move(move, env.board)
                    state, reward, done, info = env.step(move)
                    current_agent.rewards.append(reward)
            else:
                done = True
        
        # End episode
        if env.board.is_checkmate():
            winner = "white" if not env.board.turn else "black"
        else:
            winner = None
        
        metrics.end_game(winner)
        agent1.finish_episode()
        agent2.finish_episode()
        
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1}/{episodes} complete")
    
    # Save trained models
    agent1.save_model("models/agent1.pth")
    agent2.save_model("models/agent2.pth")
    print("Training complete!")

def play_game(env, model1_path, model2_path):
    """Play a game between two agents."""
    print(f"Playing game with models: {model1_path} and {model2_path}")
    
    # Create agents
    try:
        agent1 = ChessAgent()
        agent2 = ChessAgent()
        
        if os.path.exists(model1_path):
            agent1.load_model(model1_path)
        else:
            print(f"No model found at {model1_path}, using random agent")
            agent1 = create_random_agent()
        
        if os.path.exists(model2_path):
            agent2.load_model(model2_path)
        else:
            print(f"No model found at {model2_path}, using random agent")
            agent2 = create_random_agent()
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Using random agents")
        agent1 = create_random_agent()
        agent2 = create_random_agent()
    
    # Play game
    state = env.reset()
    metrics = MetricsTracker()
    metrics.start_game()
    done = False
    
    while not done:
        current_agent = agent1 if env.board.turn else agent2
        legal_moves = list(env.board.legal_moves)
        
        if legal_moves:
            move = current_agent.select_action(state, legal_moves)
            if move in legal_moves:
                metrics.log_move(move, env.board)
                state, _, done, _ = env.step(move)
                print(env.board)
                time.sleep(0.5)
        else:
            done = True
    
    # End game
    if env.board.is_checkmate():
        winner = "white" if not env.board.turn else "black"
    else:
        winner = None
    
    metrics.end_game(winner)
    print(f"Game complete! Winner: {winner if winner else 'Draw'}")
    print(f"Total moves: {metrics.get_current_metrics()['total_moves']}")

def visualize_game(env, model1_path, model2_path):
    """Visualize a game between two agents."""
    print(f"Visualizing game with models: {model1_path} and {model2_path}")
    
    # Create visualizer
    visualizer = ChessVisualizer(window_size=800)
    
    # Create agents
    try:
        agent1 = ChessAgent()
        agent2 = ChessAgent()
        
        if os.path.exists(model1_path):
            agent1.load_model(model1_path)
        else:
            print(f"No model found at {model1_path}, using random agent")
            agent1 = create_random_agent()
        
        if os.path.exists(model2_path):
            agent2.load_model(model2_path)
        else:
            print(f"No model found at {model2_path}, using random agent")
            agent2 = create_random_agent()
    except Exception as e:
        print(f"Error loading models: {e}")
        print("Using random agents")
        agent1 = create_random_agent()
        agent2 = create_random_agent()
    
    # Play game
    state = env.reset()
    metrics = MetricsTracker()
    metrics.start_game()
    done = False
    selected_square = None
    running = True
    
    while running and not done:
        # Draw board
        visualizer.draw_board(env.board, selected_square)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Make move
        current_agent = agent1 if env.board.turn else agent2
        legal_moves = list(env.board.legal_moves)
        
        if legal_moves:
            move = current_agent.select_action(state, legal_moves)
            if move in legal_moves:
                metrics.log_move(move, env.board)
                state, _, done, _ = env.step(move)
                time.sleep(0.5)
        else:
            done = True
    
    # End game
    if env.board.is_checkmate():
        winner = "white" if not env.board.turn else "black"
    else:
        winner = None
    
    metrics.end_game(winner)
    
    # Show final position
    visualizer.draw_board(env.board)
    time.sleep(2)
    visualizer.close()
    
    print(f"Game complete! Winner: {winner if winner else 'Draw'}")
    print(f"Total moves: {metrics.get_current_metrics()['total_moves']}")

def main():
    """Main entry point."""
    args = parse_args()
    
    # Create environment
    env = ChessEnv()
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Run the selected mode
    if args.mode == "train":
        train_agents(env, args.episodes)
    elif args.mode == "play":
        play_game(env, args.model1, args.model2)
    elif args.mode == "visualize":
        visualize_game(env, args.model1, args.model2)
    
    print("Done!")

if __name__ == "__main__":
    main() 