"""
CS475 Extension: 4-Turn Fixed Conversation Pacing Simulator
Inherits structure from Microsoft lost_in_conversation simulators.
"""

from pacing import generate_pacing

class PacingSimulator:
    def __init__(self, model_client, regime="uniform"):
        self.client = model_client
        self.regime = regime

    def run_conversation(self, shards):
        """
        Runs a strict 4-turn dialogue delivering 6 shards according to self.regime.
        Returns the conversation history and turn character lengths.
        """
        turns = generate_pacing(shards, regime=self.regime)
        history = []
        turn_lengths = []

        for turn_idx, content in enumerate(turns, start=1):
            history.append({"role": "user", "content": content})
            response = self.client.generate(history, temperature=0.0)
            history.append({"role": "assistant", "content": response})
            turn_lengths.append(len(response))

        return {
            "regime": self.regime,
            "final_response": history[-1]["content"],
            "history": history,
            "turn_lengths": turn_lengths
        }
