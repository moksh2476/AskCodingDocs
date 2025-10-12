from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key="")

# List available models
models = client.models.list()

# Print the first few model IDs to confirm it's working
for model in models.data[:5]:
    print(model.id)
