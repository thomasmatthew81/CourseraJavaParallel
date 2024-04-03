def estimate_cost(prompt_tokens, completion_tokens, model):
    """
    Estimate the OpenAI API cost for GPT-4 models based on prompt and completion tokens.

    Args:
        prompt_tokens (int): The number of prompt tokens.
        completion_tokens (int): The number of completion tokens (output from the model).
        model (str): The identifier for the GPT-4 model ('gpt4', 'gpt4-32k', or 'gpt4-turbo').

    Returns:
        float: The estimated cost in USD.
    """
    # Define the pricing map based on the model
    price_map = {
        'gpt4': {'prompt': 0.03, 'completion': 0.06},        # For 'gpt4' model (8k context)
        'gpt4-32k': {'prompt': 0.06, 'completion': 0.12},    # For 'gpt4-32k' model (32k context)
        'gpt4-turbo': {'prompt': 0.01, 'completion': 0.03},  # For 'gpt4-turbo' model (128k context)
    }

    if model not in price_map:
        raise ValueError(f"Unsupported model: {model}")

    # Calculate the cost per token for prompt and completion
    prompt_price_per_token = price_map[model]['prompt'] / 1000
    completion_price_per_token = price_map[model]['completion'] / 1000

    # Calculate the total cost
    cost = (prompt_tokens * prompt_price_per_token) + (completion_tokens * completion_price_per_token)
    return cost

# Example usage:
prompt_tokens = 1500  # Number of tokens in the prompt
completion_tokens = 2000  # Number of tokens in the completion
model = 'gpt4'  # Identifier for the GPT-4 model
cost = estimate_cost(prompt_tokens, completion_tokens, model)
print(f"The estimated cost for using the OpenAI API with model '{model}' is: ${cost:.2f}")
