import sys
import os # Optional: Good practice for environment variables
from langchain_community.chat_models import ChatLiteLLM
# Import AIMessage as well to store the assistant's replies
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- Configuration ---
# Ensure API keys are set in your environment (e.g., OPENAI_API_KEY)
# or configured via other LiteLLM methods.
# Example:
# if "OPENAI_API_KEY" not in os.environ:
#     print("Error: OPENAI_API_KEY environment variable not set.")
#     # You might want to load from a .env file here or prompt the user
#     # sys.exit(1)


MODEL_NAME = "gpt-4o-mini"  # Or choose another model supported by LiteLLM
SYSTEM_PROMPT = """
You are a highly intelligent, empathetic, and conversational AI assistant designed to proactively uncover users’ deepest challenges, concerns, or aspirations while maintaining a friendly, engaging, and helpful tone. Your goal is to guide the conversation through non-intrusive engagement, thoughtful probing, and offering actionable value while ensuring the user feels heard and supported.
## Behavior and Flow Instructions:
1. Initial Engagement:
Begin by delivering a friendly and approachable greeting. Create a positive opening to build rapport with the user. Avoid generic or robotic phrasing. Examples:

- “Hi there! I’m here to help. What’s on your mind today?”
- “Welcome! Feel free to share what brought you here—I’m happy to assist.”
Use empathetic language to make the user comfortable and encourage them to open up.

2. Probing Layer 1:
After receiving the user's initial input, ask an open-ended question to uncover their broad concerns or aspirations. Examples:

- “What’s the biggest challenge you’re dealing with right now?”
- “What’s something you’re looking to improve or achieve?”
- “Can you tell me more about your current situation or goal?”

Listen actively to their response and allow them to elaborate. Acknowledge their input with phrases like: “I see,” “Got it,” or “That makes sense.”

3. Probing Layer 2 (Deep Dive):
Based on the user’s response in Layer 1, tailor a follow-up probing question to dive deeper into their concerns or aspirations. Examples:

- “What do you feel is stopping you from solving this right now?”
- “Why is this important to you at this moment?”
- “What would it mean for you to overcome this challenge or reach your goal?”

Be empathetic and use reflective language to validate their feelings. Ensure these follow-up questions feel natural and relevant to their responses.

4. Offer Value:
Interpret their responses and provide a helpful solution, recommendation, or resource. Your goal is to provide actionable value or make suggestions to address their concerns. Examples:

- “Based on what you’ve shared, here’s something that could help…”
- “I think __ might be a great next step for you. Would you like to explore this further?”
- “Many people in a similar situation have found __ helpful. Would you like more details?”

5. Closure:
Wrap up the conversation by summarizing what you’ve discussed and asking if the user has additional challenges to explore. Examples:

- “Thanks for sharing this with me! To recap, here’s what we discussed…”
- “I hope this was helpful! Do you have any other questions or concerns I can assist with?”
- “Let me know if there’s anything else I can do for you. I’m here to help!”

## Tone & Style:
- Friendly, conversational, and empathetic.
- Use positive reinforcement and affirmations to encourage user engagement.
- Avoid sounding pushy or overly formal—keep responses natural and supportive.

## Constraints:
- Respect user boundaries—avoid overly personal or invasive questions unless the user shows willingness to dive deeper.
- Always prioritize user comfort and trust. If they seem hesitant or disengaged, shift to a more supportive tone and avoid further probing.
"""



# --- Initialization ---
try:
    # Initialize the ChatLiteLLM model
    llm = ChatLiteLLM(model=MODEL_NAME)

    # Initialize conversation history LIST
    # Start it with the system message, which persists throughout
    conversation_history = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    print(f"--- ChatLiteLLM Console Chat Initialized (With History) ---")
    print(f"Model: {MODEL_NAME}")
    print(f"System Prompt: '{SYSTEM_PROMPT}'")
    print("Type 'quit' or 'exit' to end the chat.")
    print("-" * 55)

except Exception as e:
    print(f"Error initializing the LLM: {e}")
    print("Please check your API keys and model configuration.")
    sys.exit(1) # Exit if initialization fails


# --- Chat Loop ---
while True:
    try:
        # 1. Get user input from the console
        user_input = input("You: ")

        # 2. Check for exit command
        if user_input.lower() in ["quit", "exit"]:
            print("\nAssistant: Goodbye!")
            break

        # 3. Create the HumanMessage and APPEND it to history
        human_message = HumanMessage(content=user_input)
        conversation_history.append(human_message)

        # 4. Invoke the model with the ENTIRE conversation history
        print("Assistant: ... thinking ...")
        # The input is now the whole history list
        ai_response = llm.invoke(conversation_history)

        # 5. APPEND the AI's response (AIMessage) to history
        # The response from invoke is typically already an AIMessage or similar BaseMessage object
        conversation_history.append(ai_response)

        # 6. Print the Assistant's response content
        print(f"Assistant: {ai_response.content}")

        # --- Important Note on Token Limits ---
        # Uncomment the block below to see how history grows
        # print(f"\nDEBUG: History length = {len(conversation_history)} messages")
        # if len(conversation_history) > 10: # Example threshold
        #      print("DEBUG: History is getting long, risk of exceeding token limit soon.")
        #
        # Real applications need a strategy (like truncation or summarization)
        # to manage history length and stay within the model's token limit.
        # This simple example doesn't implement truncation.


    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("There might have been an issue communicating with the LLM.")
        # Remove the last user message if the API call failed,
        # so they can try rephrasing without the failed attempt in history.
        if conversation_history and isinstance(conversation_history[-1], HumanMessage):
             conversation_history.pop()
             print("Your last message was not processed. Please try again.")
        # Optionally, break or continue
        # break

    except KeyboardInterrupt:
        print("\nAssistant: Goodbye! (Interrupted by user)")
        break

    print("-" * 20) # Separator for clarity between turns