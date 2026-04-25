#!/usr/bin/env python3
"""
Simple chatbot using Sieve.
Run with: python3 chat.py
"""

from sieve import route

print("=" * 50)
print("SIEVE CHAT")
print("=" * 50)
print("Type your questions. Type 'quit' to exit.")
print("Watch how different questions use different models!\n")

total_cost = 0.0
message_count = 0

while True:
    # Get user input
    user_input = input("You: ").strip()
    
    # Check for exit
    if user_input.lower() in ['quit', 'exit', 'q']:
        print(f"\n--- Session Summary ---")
        print(f"Messages: {message_count}")
        print(f"Total cost: ${total_cost:.6f}")
        print("Goodbye!")
        break
    
    # Skip empty input
    if not user_input:
        continue
    
    # Get response from router
    try:
        response = route(user_input)
        
        # Track stats
        total_cost += response.cost_usd
        message_count += 1
        
        # Show response with metadata
        print(f"\nAI: {response.content}")
        print(f"    [Model: {response.model_used} | Tier: {response.tier} | Cost: ${response.cost_usd:.6f}]")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")
