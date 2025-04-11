import random
from robo_knights.environment.chess_env import ChessEnv
from robo_knights.agents.chess_agent import ChessAgent

def train_agents(num_episodes=10, save_path_agent1="agent1.pth", save_path_agent2="agent2.pth"):
    """
    Train two chess agents to play against each other.
    
    Args:
        num_episodes (int): Number of episodes to train for
        save_path_agent1 (str): Path to save the first agent's model
        save_path_agent2 (str): Path to save the second agent's model
        
    Returns:
        tuple: (agent1, agent2) The trained agents
    """
    agent1 = ChessAgent(lr=1e-3)
    agent2 = ChessAgent(lr=1e-3)
    env = ChessEnv()
    
    for episode in range(num_episodes):
        state = env.reset()
        agent1.rewards = []
        agent2.rewards = []
        
        done = False
        turn_white = True
        while not done:
            if turn_white:
                legal_moves = env.get_legal_moves()
                move = agent1.select_action(state, legal_moves)
            else:
                legal_moves = env.get_legal_moves()
                move = agent2.select_action(state, legal_moves)
            
            # Fallback for invalid moves
            if move not in env.get_legal_moves():
                move = random.choice(env.get_legal_moves())
            
            next_state, reward, done = env.step(move)
            
            # White's perspective reward
            if turn_white:
                agent1.rewards.append(reward)
                agent2.rewards.append(-reward)
            else:
                agent2.rewards.append(-reward)
                agent1.rewards.append(reward)
            
            state = next_state
            turn_white = not turn_white
        
        agent1.finish_episode()
        agent2.finish_episode()
        if episode % 100 == 0:
            print(f"Episode {episode+1}/{num_episodes} done.")
    
    # Save final models after training
    agent1.save_model(save_path_agent1)
    agent2.save_model(save_path_agent2)
    
    return agent1, agent2 