# -*- coding: utf-8 -*-
"""
Actor-Critic neural network for chess.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F

class ActorCriticNetwork(nn.Module):
    """
    A single network that outputs:
      - A policy (move distribution) over all possible moves
      - A value estimate (scalar)
    """
    def __init__(self, input_size=8*8*12, hidden_size=128, output_size=64*64*5):
        """
        Initialize the actor-critic network.
        
        Args:
            input_size (int): Size of the input state (default: 8*8*12 for chess board)
            hidden_size (int): Size of the hidden layers
            output_size (int): Size of the policy output (default: 64*64*5 for all possible moves)
        """
        super(ActorCriticNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        
        # Actor head (policy)
        self.policy_head = nn.Linear(hidden_size, output_size)
        
        # Critic head (value)
        self.value_head = nn.Linear(hidden_size, 1)
    
    def forward(self, x):
        """
        Forward pass through the network.
        
        Args:
            x (torch.Tensor): Input state tensor
            
        Returns:
            tuple: (policy_logits, value)
        """
        x = x.view(-1, 8*8*12)  # Flatten the input
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        
        policy_logits = self.policy_head(x)
        value = self.value_head(x)
        return policy_logits, value 