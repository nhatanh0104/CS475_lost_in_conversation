"""
CS475 Project: Evaluation Sandbox (Task 2.3)
Evaluates GSM8K numerical answers and HumanEval code snippets.
"""

import re
import multiprocessing

def evaluate_math(predicted_text, gold_answer):
    """
    Extracts the last numeric value from generated text and compares with gold target.
    """
    cleaned_pred = predicted_text.replace(",", "")
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", cleaned_pred)
    if not numbers:
        return 0.0
    pred_val = numbers[-1].rstrip(".")
    gold_val = str(gold_answer).strip().replace(",", "")
    try:
        return 1.0 if float(pred_val) == float(gold_val) else 0.0
    except ValueError:
        return 1.0 if pred_val == gold_val else 0.0

def _run_code(code_str, test_str, result_queue):
    global_scope = {}
    try:
        exec(code_str, global_scope)
        exec(test_str, global_scope)
        result_queue.put(1.0)
    except Exception:
        result_queue.put(0.0)

def evaluate_code_sandbox(code_str, test_str, timeout=3):
    """
    Executes Python code with unit test assertions inside an isolated process with timeout.
    """
    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=_run_code, args=(code_str, test_str, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return 0.0
    return q.get() if not q.empty() else 0.0
