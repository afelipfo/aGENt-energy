from genagents.genagents import GenerativeAgent

# Initialize a new agent
agent = GenerativeAgent()

# Update scratchpad
agent.update_scratch({
    "first_name": "Emma",
    "last_name": "Carter",
    "age": 38,
    "occupation": "Energy Regulation Consultant",
    "expertise": ["energy policy", "renewable energy regulations", "compliance standards"],
    "interests": ["sustainable energy", "environmental law", "industry trends"],
    "knowledge": "The Clean Air Act sets emission standards for power plants, updated in 2022. Renewable Portfolio Standards (RPS) require utilities to source a percentage of energy from renewables, varying by state. FERC oversees interstate electricity sales and grid reliability under Order 1000."
})

# Save the agent without memories for now
agent.save("agent_bank/populations/energy_reg_agent")
print("Energy regulation agent created and saved successfully!")