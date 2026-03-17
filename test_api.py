from fastapi import FastAPI
import uvicorn
from openai import OpenAI

app = FastAPI()

# Initialize OpenAI client
client = OpenAI()

@app.get("/")
def home():
    return {"message": "Test OK"}

# Your OpenAI test as an API endpoint
@app.get("/test-openai")
def test_openai():
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say hello"}]
    )
    return {"response": response.choices[0].message.content}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)