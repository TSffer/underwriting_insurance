import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infrastructure.core import InsuranceChatbot

def main():
    print("Initializing Insurance Policy Assistant Chatbot...")
    bot = InsuranceChatbot()
    bot.train_model()
    
    print("\nChatbot ready! Type 'salir' to exit.")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("Tú: ")
            if user_input.lower() in ['salir', 'exit', 'quit']:
                print("Hasta luego!")
                break
                
            response = bot.handle_message(user_input)
            # The actions currently print to stdout, so response might be None or return value
            if response:
                print(f"Bot: {response}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
