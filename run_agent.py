from genagents.genagents import GenerativeAgent

# Initialize a new agent
agent = GenerativeAgent()

# Update the agent's scratchpad with personal information
agent.update_scratch({
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "occupation": "Software Engineer",
    "interests": ["reading", "hiking", "coding"]
})

# Ask a categorical question
questions = {
    "Do you enjoy outdoor activities?": ["Yes", "No", "Sometimes"]
}
response = agent.categorical_resp(questions)
print("Categorical Response:", response["responses"])

# Ask a numerical question
num_questions = {
    "On a scale of 1 to 10, how much do you enjoy coding?": [1, 10]
}
num_response = agent.numerical_resp(num_questions, float_resp=False)
print("Numerical Response:", num_response["responses"])

# Ask an open-ended question
dialogue = [
    ("Interviewer", "Tell me about your favorite hobby."),
]
open_response = agent.utterance(dialogue)
print("Open-Ended Response:", open_response)

# Save the agent for later use
agent.save("my_agent")