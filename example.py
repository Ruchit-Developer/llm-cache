from llm_cache.cache import SmartCache

# 1. Initialize the caching engine (creates a local SQLite DB automatically)
cache = SmartCache(db_path="llm_memory.db")

prompt = "Explain quantum computing in one sentence."

# 2. Intercept the request
cached_response = cache.check_cache(prompt)

if cached_response:
    print(f"CACHE HIT: {cached_response}")
else:
    print("CACHE MISS: Routing to LLM Provider...")
    
    # Simulate your expensive API call here (e.g., OpenAI or Gemini)
    # response = call_openai_api(prompt)
    expensive_response = "Quantum computing uses quantum bits to perform complex calculations exponentially faster than classical computers."
    
    # 3. Save the response to prevent future billing
    cache.save_to_cache(prompt, expensive_response)
    print(f"Response saved to memory.")
