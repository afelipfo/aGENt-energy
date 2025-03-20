from genagents.genagents import GenerativeAgent

# Load the energy regulation agent
agent = GenerativeAgent(agent_folder="agent_bank/populations/energy_reg_agent")
print("Agent Scratchpad:", agent.scratch)

# Categorical Response
questions = {"Are renewable energy mandates effective?": ["Yes", "No", "It depends"]}
response = agent.categorical_resp(questions)
print("Categorical Response:", response["responses"])

# Numerical Response
questions = {"On a scale of 1 to 10, how strict are current energy regulations?": [1, 10]}
response = agent.numerical_resp(questions, float_resp=False)
print("Numerical Response:", response["responses"])

# Open-Ended Question
dialogue = [("Interviewer", "What are the key challenges in energy regulation today?")]
response = agent.utterance(dialogue)
print("Open-Ended Response:", response)