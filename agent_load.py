from genagents.genagents import GenerativeAgent

# Load the agent
agent = GenerativeAgent(agent_folder="agent_bank/populations/my_agent")
print("Agent Scratchpad:", agent.scratch)  # Check if this contains data