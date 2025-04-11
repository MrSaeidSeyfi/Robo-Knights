# -*- coding: utf-8 -*-
"""
Chess agent implementation.
"""

import torch
import torch.nn.functional as F
import torch.optim as optim
import random

from robo_knights.models.actor_critic import ActorCriticNetwork
from robo_knights.utils.move_utils import move_to_index, index_to_move

class ChessAgent:
    """
    Chess agent that uses an actor-critic network to play chess.
    """
    def __init__(self, lr=1e-3, gamma=0.99):
        """
        Initialize the chess agent.
        
        Args:
            lr (float): Learning rate for the optimizer
            gamma (float): Discount factor for future rewards
        """
        self.gamma = gamma
        # Output size now 64*64*5 = 20480 (same indexing approach as before).
        self.model = ActorCriticNetwork(output_size=64*64*5)
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        
        # For storing transitions
        self.saved_log_probs = []
        self.saved_values = []
        self.rewards = []
    
    def select_action(self, state, legal_moves):
        """
        Select an action based on the current state and legal moves.
        
        Args:
            state (numpy.ndarray): Current state of the board
            legal_moves (list): List of legal chess.Move objects
            
        Returns:
            chess.Move: The selected move
        """
        state_tensor = torch.FloatTensor(state.flatten()).unsqueeze(0)
        policy_logits, value = self.model(state_tensor)
        
        # Mask invalid moves
        mask = torch.zeros(policy_logits.shape[1])
        move_indices = [move_to_index(m) for m in legal_moves if m is not None]
        for idx in move_indices:
            if idx is not None and 0 <= idx < mask.numel():
                mask[idx] = 1
        
        masked_logits = policy_logits + torch.log(mask.unsqueeze(0) + 1e-10)
        probs = F.softmax(masked_logits, dim=1)
        
        dist = torch.distributions.Categorical(probs)
        action_idx = dist.sample()
        
        log_prob = dist.log_prob(action_idx)
        self.saved_log_probs.append(log_prob)
        
        # Save the value estimate at this time-step
        self.saved_values.append(value.squeeze(0))
        
        chosen_move = index_to_move(action_idx.item())
        return chosen_move
    
    def finish_episode(self):
        """
        Finish the current episode and update the model.
        """
        # Compute returns
        R = 0
        returns = []
        for r in reversed(self.rewards):
            R = r + self.gamma * R
            returns.insert(0, R)
        returns = torch.tensor(returns)
        
        # Normalize returns
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # Calculate losses
        policy_loss = []
        value_loss = []
        for log_prob, value_est, ret in zip(self.saved_log_probs, self.saved_values, returns):
            advantage = ret - value_est.item()
            
            # Policy loss = -log_prob * advantage
            policy_loss.append(-log_prob * advantage)
            
            # Value loss = MSE(advantage)
            value_loss.append(F.smooth_l1_loss(value_est, torch.tensor([ret])))
        
        self.optimizer.zero_grad()
        (torch.stack(policy_loss).sum() + torch.stack(value_loss).sum()).backward()
        self.optimizer.step()
        
        # Clear buffers
        self.saved_log_probs = []
        self.saved_values = []
        self.rewards = []
    
    def save_model(self, path):
        """
        Save the model to a file.
        
        Args:
            path (str): Path to save the model to
        """
        torch.save(self.model.state_dict(), path)
    
    def load_model(self, path):
        """
        Load the model from a file.
        
        Args:
            path (str): Path to load the model from
        """
        self.model.load_state_dict(torch.load(path, weights_only=True)) 