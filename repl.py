from finasistant_app.agents.agent import assistant_workflow

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in assistant_workflow.stream({"messages": ("user", user_input)}, debug=True):
        for value in event.values():
            print("Assistant:", value)