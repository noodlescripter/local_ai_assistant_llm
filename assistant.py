import speech_recognition as sr
import pyttsx3
import time
import openai
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

class CustomAssistant:
    def __init__(self, wake_word="assistant"):
        # Initialize core components
        self.wake_word = wake_word
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        
        # Configure OpenAI
        # if not self.openai_api_key:
        #     raise ValueError("OpenAI API key not found in environment variables")
        # openai.api_key = self.openai_api_key
        
        # Configure voice settings
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Female voice
        self.engine.setProperty('rate', 150)  # Speaking rate
        self.engine.setProperty('volume', 0.9)  # Volume level
        
        # Adjust recognition settings
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000
        
        # Initialize conversation history
        self.conversation_history = []
        
    def speak(self, text):
        """Convert text to speech with error handling"""
        try:
            print(f"Assistant: {text}")
            #self.engine.say(text)
            #self.engine.runAndWait()
            os.system(f'echo "{text}" | ./piper --model voice.onnx --output_raw | aplay -r 22050 -f S16_LE -t raw -')
            
        except Exception as e:
            print(f"Speech error: {e}")
            
    async def get_openai_response(self, text):
        """Get responsea from OpenAI API"""
        try:
            # Add user message to conversation history
        #     self.conversation_history.append({"role": "user", "content": text})
            
        #     response = openai.chat.completions.create(
        #         model="gpt-4o-mini",
        #         messages=self.conversation_history,
        #         max_tokens=150,
        #         temperature=0.7,
        #     )
            
        #     # Extract and store assistant's response
        #     assistant_response = response.choices[0].message.content
        #     self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
        #     # Limit conversation history to last 10 messages to prevent token limit issues
        #     if len(self.conversation_history) > 10:
        #         self.conversation_history = self.conversation_history[-10:]
                
        #     return assistant_response
            
        # except Exception as e:
        #     print(f"OpenAI API error: {e}")
        #     return "I apologize, but I'm having trouble generating a response right now."
            url = "http://local-cloud:11434/api/generate"
    
        # Request with timeout and proper model name
            response = requests.post(
                url,
                json={
                    "model": "llama3.2",  # or your specific model
                    "prompt": "Keep the ans short on whatever asked here: "+text,
                    "max_tokens": 30,
                    "stream": False
                },
                timeout=30  # Add timeout
            )

            # Check status code
            response.raise_for_status()

            # Validate response structure
            response_data = response.json()
            print(response_data['response'])
            return response_data['response']

        except Exception as e:
            print(f"API error: {e}")
            return "I apologize, but I'm having trouble generating a response right now. Are you sure your local language model is running? Please check and try again."
            
    async def generate_response(self, text):
        """Generate a contextual responseusing OpenAI"""
        # Convert text to lowercase for easier matching
        text = text.lower()
        
        # Remove wake word from the text
        text = text
        
        if not text:
            return "I'm listening, how can I help?"
            
        # Get response from OpenAI
        response = await self.get_openai_response(text)
        return response
        
    async def listen_and_respond(self):
        """Main listening and response loop"""
        with sr.Microphone() as source:
            print("\nListening for wake word...")
            
            try:
                self.recognizer.energy_threshold = 500  # Default is 4000, lower = more sensitive
                self.recognizer.dynamic_energy_threshold = False  # Disable dynamic adjustment
            
                # Optional: Increase dynamic range
                self.recognizer.dynamic_energy_adjustment_ratio = 2.5
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                
                # Attempt to recognize speech
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                # Check for wake word
                if any(wake_word in text for wake_word in self.wake_word):
                    # Visual feedback
                    print("\nWake word detected! Listening for command...")
                    
                    # Acknowledge wake word
                    self.speak("I'm listening")
                    
                    # Listen for the actual command
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"Command heard: {command}")
                    
                    self.speak("Please wait while I get an answer")
                    
                    # Generate and speak response
                    response = await self.generate_response(command)
                    self.speak(response)
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Could not connect to speech recognition service")
            except Exception as e:
                print(f"Error: {e}")

async def main():
    # Initialize assistant with custom wake word
    wake_word = ["shit", "deep", "hey", "hi", "sheet", "sit", "dip"]  # Change this to your preferred wake word
    assistant = CustomAssistant(wake_word)
    
    # Welcome message
    assistant.speak(f"Hello! I'm your AI assistant. Say '{wake_word}' to activate me.")
    
    # Main loop
    try:
        while True:
            await assistant.listen_and_respond()
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())