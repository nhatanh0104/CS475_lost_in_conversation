"""
CS475 Project: Information Pacing Generator
Partitions a list of atomic shards into a fixed 4-turn schedule.
"""

def generate_pacing(shards, regime="early"):
    """
    shards: List of strings representing atomic constraints (at least 6).
    regime: Pacing strategy ('early', 'mid', 'late', or 'uniform').
    Returns a list of 4 conversational turns.
    """
    if len(shards) < 6:
        raise ValueError("Each instance must contain at least 6 shards.")
    
    s = shards[:6]
    
    if regime == "early":
        # Turn 1: 3 shards | Turn 2: 1 shard | Turn 3: 1 shard | Turn 4: 1 shard
        splits = [s[0:3], [s[3]], [s[4]], [s[5]]]
    elif regime == "mid":
        # Turn 1: 1 shard | Turn 2: 3 shards | Turn 3: 1 shard | Turn 4: 1 shard
        splits = [[s[0]], s[1:4], [s[4]], [s[5]]]
    elif regime == "late":
        # Turn 1: 1 shard | Turn 2: 1 shard | Turn 3: 1 shard | Turn 4: 3 shards
        splits = [[s[0]], [s[1]], [s[2]], s[3:6]]
    elif regime == "uniform":
        # Turn 1: 2 shards | Turn 2: 2 shards | Turn 3: 1 shard | Turn 4: 1 shard
        splits = [s[0:2], s[2:4], [s[4]], [s[5]]]
    elif regime == "not-sharded":
        # All shards in one turn
        splits = [s]  
    else:
        raise ValueError(f"Unknown regime: {regime}")
        
    dialogue_turns = []
    for turn_idx, group in enumerate(splits, start=1):
        formatted_turn = f"[Turn {turn_idx}] Revealed Constraints:\n" + "\n".join([f"  - {shard}" for shard in group])
        dialogue_turns.append(formatted_turn)
        
    return dialogue_turns

if __name__ == "__main__":
    sample_shards = [
        "Shard 1: Calculate the total profit from house flipping",
        "Shard 2: Initial purchase price is 80,000 USD",
        "Shard 3: Renovation costs equal 50,000 USD",
        "Shard 4: House value increased by 150 percent",
        "Shard 5: Closing fees and agent commissions are neglected",
        "Shard 6: Return the final net profit as an integer"
    ]
    
    print("=== TESTING EARLY-BURST PACING SCHEDULE (T=4) ===")
    turns = generate_pacing(sample_shards, regime="early")
    for turn in turns:
        print(turn)
