import speech_recognition as sr
import requests
import asyncio
import os

class CustomAssistant:
    def __init__(self, wake_word="assistant"):
        self.wake_word = wake_word
        self.recognizer = sr.Recognizer()
        self.conversation_history = []
        
    def speak(self, text):
        """Print and speak the response"""
        print(f"Assistant: {text}")
        piper_dir = os.path.join(os.getcwd(), "piper", "piper")
        #os.system(f'echo "{text} | ./piper/piper --model voice.onnx --output-raw | aplay -r 22050 -f S16_LE -t raw -"')
        os.system(f'echo "{text}" | ./piper --model voice.onnx --output_raw | aplay -r 22050 -f S16_LE -t raw -')
            
    async def get_openai_response(self, text):
        """Get response from API"""
        try:
            url = "http://local-cloud:11434/api/generate"
    
            response = requests.post(
                url,
                json={
                    "model": "llama3.2",
                    "prompt": "Keep the ans short on whatever asked here: "+text,
                    "max_tokens": 30,
                    "stream": False
                },
                timeout=30
            )

            response.raise_for_status()
            response_data = response.json()
            return response_data['response']

        except Exception as e:
            print(f"API error: {e}")
            self.speak("Error: Unable to get response. Please check if your local language model is running. Please try again")
            return "Error: Unable to get response. Please check if your local language model is running."
            
    async def generate_response(self, text):
        """Generate a contextual response"""
        text = text.lower()
        
        if not text:
            return "I'm listening, how can I help?"
            
        response = await self.get_openai_response(text)
        return response
        
    async def listen_and_respond(self):
        """Main listening and response loop"""
        with sr.Microphone() as source:
            print("\nListening for wake word...")
            
            try:
                self.recognizer.energy_threshold = 500
                self.recognizer.dynamic_energy_threshold = False
                self.recognizer.dynamic_energy_adjustment_ratio = 2.5
                self.recognizer.adjust_for_ambient_noise(source, duration=0.1)
                
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                if any(wake_word in text for wake_word in self.wake_word):
                    print("\nWake word detected! Listening for command...")
                    self.speak("Hey There!, How can I help?")
                    
                    audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=8)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"Command heard: {command}")
                    
                    self.speak("Please wait.")
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
    wake_word = ["shit", "deep", "hey", "hi", "sheet", "sit", "dip"]
    assistant = CustomAssistant(wake_word)
    
    assistant.speak("Hello! I'm your AI assistant. Say any of these words to activate me: " + ", ".join(wake_word))
    
    try:
        while True:
            await assistant.listen_and_respond()
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    asyncio.run(main())