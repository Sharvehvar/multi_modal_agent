import os
from dotenv import load_dotenv
from agent import MultiModalAgent
from PIL import Image

def main():
    load_dotenv()
    
    # Initialize the multi-modal agent
    agent = MultiModalAgent(api_key=os.getenv("GOOGLE_API_KEY"))
    
    print("Multi-Modal Agent (Windows Version)")
    print("Enter 'exit' to quit\n")
    
    while True:
        print("\nEnter your input (text or image path):")
        user_input = input("> ").strip()
        
        if user_input.lower() in ['exit', 'quit']:
            break
            
        try:
            # Check if input is an image path
            if user_input.lower().endswith(('.png', '.jpg', '.jpeg')):
                image = Image.open(user_input)
                print("Enter an optional prompt (or press Enter to describe the image):")
                prompt = input("> ").strip()
                response = agent.process_image(image, prompt if prompt else None)
            else:
                response = agent.process_text(user_input)
                
            print("\nAgent Response:")
            print(response)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()