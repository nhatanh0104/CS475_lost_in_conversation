"""
CS475 Project: 4-Turn Fixed Conversation Matrix Runner (Task 2.4)
Executes dialogue regimes (Early, Mid, Late, Uniform) over GSM8K and Code datasets.
"""

import json
import os
from pacing import generate_pacing
from evaluator import evaluate_math, evaluate_code_sandbox
from llm_client import ModelClient

def run_experiment(dataset_path, is_code=False, sample_limit=20):
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)[:sample_limit]
        
    client = ModelClient(use_local=True)
    regimes = ["not-sharded", "uniform", "early", "mid", "late"]
    results = {r: [] for r in regimes}

    for idx, item in enumerate(data):
        shards = item.get("shards_6", item.get("shards", []))[:6]
        gold = str(item.get("answer", item.get("gold_answer", "")))
        gold = gold.split("####")[-1].strip().replace(",", "")
        test_case = item.get("test", "")

        for regime in regimes:
            turns = generate_pacing(shards, regime=regime)
            dialogue_history = []
            turn_lengths = []

            for turn_content in turns:
                dialogue_history.append({"role": "user", "content": turn_content})
                response = client.generate(dialogue_history, temperature=0.0)
                dialogue_history.append({"role": "assistant", "content": response})
                turn_lengths.append(len(response))

            final_response = dialogue_history[-1]["content"]
            if is_code:
                score = evaluate_code_sandbox(final_response, test_case)
            else:
                score = evaluate_math(final_response, gold)

            results[regime].append({
                "id": idx,
                "score": score,
                "turn_lengths": turn_lengths
            })
            print(f"[{regime.upper()}] Case {idx+1}/{len(data)} -> Score: {score}")

    os.makedirs("results", exist_ok=True)
    out_file = f"results/{'code' if is_code else 'math'}_matrix.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {out_file}")

if __name__ == "__main__":
    if os.path.exists("data_filtered/gsm8k_filtered_6shards.json"):
        print("Starting 50% Matrix Evaluation on GSM8K...")
        run_experiment("data_filtered/gsm8k_filtered_6shards.json", is_code=False, sample_limit=30)
