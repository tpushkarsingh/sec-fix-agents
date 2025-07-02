from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

# Print all keys and values from the .env file
print("Environment variables loaded from .env:")
for key, value in os.environ.items():
    print(f"{key}: {value}")