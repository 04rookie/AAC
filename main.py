from gpt4all import GPT4All

# Load the model
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")  # Make sure the model file exists

# Define system prompt
# system_prompt = "<|system|>You are an AI assistant that provides short, conversational response options for AAC users. Here are the options your user has selected so far, if any conversation is about these options use the context from these options!: "
system_prompt = "<|system|>You are an AI assistant that provides short, conversational response options for AAC users. Here is the conversation so far, use it to guide your response: "
# Start interactive chat session
with model.chat_session():
    while True:
        user_input = input("You: ")  # Get user input
        
        if user_input.lower() == "exit":  # Exit condition
            print("Goodbye!")
            break

        # Construct prompt to get short response options
        prompt = f"{system_prompt}<|end|><|user|>{user_input}<|end|><|assistant|>Provide 10 short response options to choose from:<|end|>"

        # Generate response
        response = model.generate(prompt, max_tokens=100)

        # Print response options
        print("\nAI Response Options:")
        options = response.strip().split("\n")  # Split responses by newline if formatted that way
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option.strip()}")
            
        # Get user's choice
        choice = input("\nSelect a response option: ")
        # if choice not in ["1", "2", "3"]:
        #     print("Invalid choice. Please select 1, 2, or 3.")

        system_prompt = system_prompt + " " + "They said: " + user_input + " " + " you responded: " + options[int(choice) - 1]
        print(system_prompt)
        print("\n(Type 'exit' to quit)\n")