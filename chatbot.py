from openai import OpenAI
import time
import pyttsx3

# Set your OpenAI API key
openai_api_key = "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"
client = OpenAI(api_key=openai_api_key)

messages = []
system_msg = "permanent_chatbot"  # Set your desired chatbot type here
messages.append({"role": "system", "content": system_msg})

print("Assistant Friday is ready!")

response_count = 0
start_time = time.time()

engine = pyttsx3.init()  # Initialize text-to-speech engine

while True:
    user_input = input("-----------------------------------------------------------------\nYou: ")
    if user_input.lower() == "quit()":
        break

    response_count += 1
    if response_count > 2:
        elapsed_time = time.time() - start_time
        if elapsed_time < 60:
            print("Please wait for 1 minute before the next response.")
            time.sleep(60 - elapsed_time)
            start_time = time.time()
            response_count = 0

    # Ensure the 'prompt' parameter is present
    prompt = f"You are a helpful assistant.\nUser: {user_input}\n"
    
    response = client.completions.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=150,
    )
    
    assistant_reply = response["choices"][0]["message"]["content"]

    # Split the assistant's reply into multiple lines if more than 100 characters
    words = assistant_reply.split()
    formatted_reply = ""
    line_length = 0
    for word in words:
        if line_length + len(word) > 100:
            formatted_reply += "\n"
            line_length = 0
        formatted_reply += word + " "
        line_length += len(word) + 1

    messages.append({"role": "assistant", "content": assistant_reply})
    print("Friday:", formatted_reply + "\n")

    # Ask the user whether to speak the assistant's response
    speak_response = input("Do you want Alex to speak the response? (Y/N): ")
    if speak_response.lower() == "y":
        engine.say(formatted_reply)
        engine.runAndWait()
