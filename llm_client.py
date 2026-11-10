import os
from openai import OpenAI

class ModelClient:
    def __init__(self, use_local=True):
        self.use_local = use_local
        self.prompt_tokens = 0
        self.completion_tokens = 0
        
        if self.use_local:
            # Connects directly to our vLLM server running on the L40S GPU
            self.client = OpenAI(
                base_url="http://127.0.0.1:8000/v1",
                api_key="none"
            )
            self.model_name = "meta-llama/Llama-3.1-8B-Instruct"
        else:
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is missing!")
            self.client = OpenAI(api_key=api_key)
            self.model_name = "gpt-4o-mini"

    def generate(self, messages, temperature=0.7, max_tokens=1024):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        usage = response.usage
        if usage:
            self.prompt_tokens += usage.prompt_tokens
            self.completion_tokens += usage.completion_tokens
        return response.choices[0].message.content

    def get_cost_summary(self):
        cost = (self.prompt_tokens / 1e6 * 0.15) + (self.completion_tokens / 1e6 * 0.60)
        return {
            "model": self.model_name,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "estimated_cost_usd": round(cost, 6)
        }