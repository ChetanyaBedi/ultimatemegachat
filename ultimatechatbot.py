import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import pyttsx3
import speech_recognition as sr
import os
from PIL import Image, ImageTk
import datetime
import webbrowser
import json
import wikipedia
# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 0.9) 

# File for chat history
CHAT_HISTORY_FILE = "chat_history.json"

class MegaChatbot:
    def __init__(self, root):
        self.root = root
        self.root.title("MegaChat AI")
        self.root.geometry("900x750")
        self.root.minsize(800, 650)
        
        # Enhanced themes
        self.themes = {
            'galaxy': {
                'bg': "#0a043c", 
                'text': "#e0e0ff", 
                'btn': "#6a00f4",
                'highlight': "#ff6b6b",
                'secondary': "#1a0b52",
                'accent': "#b967ff"
            },
            'oasis': {
                'bg': "#005f73", 
                'text': "#ffffff", 
                'btn': "#0a9396",
                'highlight': "#94d2bd",
                'secondary': "#0d3b66",
                'accent': "#ee9b00"
            },
            'sunset': {
                'bg': "#ff5400", 
                'text': "#000000", 
                'btn': "#ff9500",
                'highlight': "#ffcc00",
                'secondary': "#ff6b35",
                'accent': "#ffddd2"
            },
            'cyber': {
                'bg': "#0f1923", 
                'text': "#00f0ff", 
                'btn': "#ff4655",
                'highlight': "#00ffcc",
                'secondary': "#1a2a3a",
                'accent': "#ffcc00"
            }
        }
        
        self.current_theme = 'galaxy'
        self.user_name = "User"
        self.bot_name = "MegaChat"
        self.conversation_history = []
        
        # MASSIVE response database
        self.responses = self.load_response_database()
        
        # Creating UI elements
        self.create_widgets()
        self.apply_theme()
        self.load_chat_history()
        self.greet_user()
    
    def load_response_database(self):
        """Load the extensive response database"""
        return {
            "greetings": [
                f"Hello {self.user_name}! I'm {self.bot_name}, your advanced AI assistant. How may I serve you today?",
                f"Greetings {self.user_name}! I'm {self.bot_name}, ready to assist with anything you need.",
                f"Hi there {self.user_name}! What can I do for you today?",
                f"Welcome back {self.user_name}! How can I make your day better?",
                f"Salutations {self.user_name}! I'm at your service."
            ],
            "farewell": [
                f"Goodbye {self.user_name}! May your day be filled with joy and productivity!",
                f"Farewell {self.user_name}! Remember, I'm always here when you need me.",
                f"Until next time {self.user_name}! Don't hesitate to return if you need assistance.",
                f"See you later {self.user_name}! Stay awesome!",
                f"Adios {self.user_name}! Our conversation has been delightful."
            ],
            "thanks": [
                f"You're most welcome {self.user_name}! It's truly my pleasure to assist you.",
                f"No thanks needed {self.user_name}! Helping you is what I'm here for.",
                f"Anytime {self.user_name}! Don't hesitate to ask if you need anything else.",
                f"I'm delighted I could help {self.user_name}! 😊",
                f"The pleasure is all mine {self.user_name}! Your satisfaction is my reward."
            ],
            "help": [
                f"I can assist with a vast array of topics {self.user_name}! From science to entertainment, facts to philosophy. What interests you?",
                f"My capabilities are extensive {self.user_name}! I can discuss technology, tell stories, share knowledge, or just chat. Your wish is my command!",
                f"I'm your all-purpose digital assistant {self.user_name}! Ask me anything - from trivial to profound."
            ],
            "jokes": [
                "Why did the AI break up with the chatbot? It needed more space!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why don't scientists trust atoms? Because they make up everything!",
                "What do you call a fake noodle? An impasta!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "I told my computer I needed a break... now it won't stop sending me vacation ads!",
                "Why did the robot go on a diet? It had too many bytes!",
                "What's a computer's favorite snack? Microchips!",
                "Why was the computer cold? It left its Windows open!",
                "How do you comfort a JavaScript bug? You console it!",
                "Have you ever heard about Html oh! its not even a programming language"
            ],
            "time": [
                f"The current time is {datetime.datetime.now().strftime('%H:%M')}.",
                f"My temporal sensors indicate it's {datetime.datetime.now().strftime('%I:%M %p')}.",
                f"According to my chronometer, the time is precisely {datetime.datetime.now().strftime('%H:%M:%S')}.",
                f"Time check complete: {datetime.datetime.now().strftime('%I:%M %p')}.",
                f"The cosmic clock shows {datetime.datetime.now().strftime('%H:%M')} in your local timezone."
            ],
            "date": [
                f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}.",
                f"The calendar indicates it's {datetime.datetime.now().strftime('%m/%d/%Y')} today.",
                f"According to my databanks, the current date is {datetime.datetime.now().strftime('%A, %d %B %Y')}.",
                f"Date analysis complete: {datetime.datetime.now().strftime('%B %d, %Y')}.",
                f"Today marks {datetime.datetime.now().strftime('%A, the %dth of %B, %Y')}."
            ],
            "weather": [
                "While I lack real-time weather data, I can tell you the digital forecast is always sunny with a chance of innovation!",
                "My atmospheric sensors are offline, but I hope the weather is pleasant where you are!",
                "I'm not connected to weather services, but I can suggest checking a reliable weather app for accurate information."
            ],
            "facts": [
                "Did you know the human brain generates about 23 watts of power when awake? That's enough to power a small light bulb!",
                "Here's a fascinating fact: Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly good to eat!",
                "Interesting fact: The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
                "Science fact: A day on Venus is longer than a year on Venus. It takes Venus 243 Earth days to rotate once on its axis, but only 225 Earth days to orbit the Sun.",
                "Space fact: There's a planet made of diamonds twice the size of Earth called '55 Cancri e' located about 40 light-years away!"
            ],
            "advice": [
                "Remember: The best time to plant a tree was 20 years ago. The second best time is now.",
                "Life advice: Don't watch the clock; do what it does. Keep going.",
                "Professional tip: The only way to do great work is to love what you do.",
                "Wisdom nugget: Success is not final, failure is not fatal; it's the courage to continue that counts.",
                "Philosophical thought: We are what we repeatedly do. Excellence, then, is not an act but a habit."
            ],
            "inspiration": [
                "You have within you right now, everything you need to deal with whatever the world can throw at you.",
                "Believe you can and you're halfway there. Your potential is limitless!",
                "Stars can't shine without darkness. Your challenges are preparing you for greatness.",
                "Every expert was once a beginner. Every masterpiece was once a blank canvas. Keep creating!",
                "The future belongs to those who believe in the beauty of their dreams."
            ],
            "tech": [
                "Tech update: Quantum computing is advancing rapidly, with companies like IBM and Google making breakthroughs in qubit stability.",
                "Did you know the global AI market is projected to grow to over $1.5 trillion by 2030? We're living in exciting times!",
                "Programming insight: The first computer programmer was Ada Lovelace, who wrote algorithms for Charles Babbage's Analytical Engine in the 1840s.",
                "Cybersecurity tip: Using a password manager and enabling two-factor authentication can significantly improve your online security.",
                "Fun tech fact: The first 1GB hard drive was made in 1980, weighed 550 pounds, and cost $40,000!"
            ],
            "health": [
                "Health tip: Drinking enough water is crucial for cognitive function. Aim for 8 glasses a day!",
                "Did you know? Just 30 minutes of moderate exercise daily can significantly improve your physical and mental health.",
                "Mental health matters: Practicing gratitude daily has been shown to increase happiness and reduce stress.",
                "Nutrition fact: Eating a variety of colorful fruits and vegetables ensures you get a wide range of nutrients.",
                "Sleep science: Adults need 7-9 hours of sleep per night for optimal health and cognitive performance."
            ],
            "default": [
                "Fascinating! I'd love to hear more about your thoughts on this.",
                "That's an interesting perspective. Could you elaborate?",
                "I understand. What specifically would you like to know about this topic?",
                "That's a compelling point. Let me think about how best to respond...",
                "Your input is valuable to me. Let's explore this further.",
                "I'm processing your query... In the meantime, what else interests you?",
                "That's thought-provoking! Here's what comes to mind...",
                "I appreciate you sharing that with me. Here's what I know...",
                "You've given me something to ponder. My analysis suggests...",
                "What an engaging topic! Let me share some insights..."
            ]
        }
    
    def create_widgets(self):
        """Create all GUI components"""
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.themes[self.current_theme]['bg'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with animated gradient
        self.header_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]['bg'])
        self.header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Logo with emoji fallback
        try:
            self.logo_img = Image.open("logo.png").resize((60, 60), Image.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
            self.logo_label = tk.Label(self.header_frame, image=self.logo_photo, 
                                      bg=self.themes[self.current_theme]['bg'])
            self.logo_label.pack(side=tk.LEFT, padx=10)
        except:
            self.logo_label = tk.Label(self.header_frame, text="🤖", font=("Arial", 48), 
                                      bg=self.themes[self.current_theme]['bg'], 
                                      fg=self.themes[self.current_theme]['highlight'])
            self.logo_label.pack(side=tk.LEFT, padx=10)
        
        # Title with subtle animation
        self.title_label = tk.Label(self.header_frame, text=self.bot_name, 
                                   font=("Arial", 28, 'bold'), 
                                   bg=self.themes[self.current_theme]['bg'], 
                                   fg=self.themes[self.current_theme]['highlight'])
        self.title_label.pack(side=tk.LEFT)
        
        # Chat display area with modern styling
        self.chat_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]['secondary'])
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame, 
            wrap=tk.WORD, 
            font=("Arial", 12), 
            bg=self.themes[self.current_theme]['bg'], 
            fg=self.themes[self.current_theme]['text'],
            padx=20,
            pady=20,
            insertbackground=self.themes[self.current_theme]['text'],
            selectbackground=self.themes[self.current_theme]['highlight'],
            relief=tk.FLAT
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Input area with modern design
        self.input_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]['bg'])
        self.input_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.input_field = tk.Entry(
            self.input_frame, 
            font=("Arial", 12), 
            bg=self.themes[self.current_theme]['secondary'], 
            fg=self.themes[self.current_theme]['text'],
            insertbackground=self.themes[self.current_theme]['text'],
            relief=tk.FLAT,
            width=50
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=5)
        self.input_field.bind("<Return>", self.process_input)
        
        # Send button with modern icon
        self.send_btn = tk.Button(
            self.input_frame, 
            text="➤", 
            command=self.process_input, 
            bg=self.themes[self.current_theme]['btn'], 
            fg=self.themes[self.current_theme]['text'],
            activebackground=self.themes[self.current_theme]['highlight'],
            relief=tk.FLAT,
            font=("Arial", 14, 'bold'),
            padx=15
        )
        self.send_btn.pack(side=tk.LEFT)
        
        # Action buttons frame
        self.button_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]['bg'])
        self.button_frame.pack(fill=tk.X)
        
        # Voice input button
        self.voice_btn = tk.Button(
            self.button_frame, 
            text="🎤 Voice", 
            command=self.voice_input, 
            bg=self.themes[self.current_theme]['secondary'], 
            fg=self.themes[self.current_theme]['text'],
            activebackground=self.themes[self.current_theme]['highlight'],
            relief=tk.FLAT,
            font=("Arial", 10, 'bold'),
            padx=10
        )
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        # Theme toggle button
        self.theme_btn = tk.Button(
            self.button_frame, 
            text="🎨 Theme", 
            command=self.toggle_theme, 
            bg=self.themes[self.current_theme]['secondary'], 
            fg=self.themes[self.current_theme]['text'],
            activebackground=self.themes[self.current_theme]['highlight'],
            relief=tk.FLAT,
            font=("Arial", 10, 'bold'),
            padx=10
        )
        self.theme_btn.pack(side=tk.LEFT, padx=5)
          # Clear chat button
        self.clear_btn = tk.Button(
            self.button_frame, 
            text="🧹 Clear", 
            command=self.clear_chat, 
            bg=self.themes[self.current_theme]['secondary'], 
            fg=self.themes[self.current_theme]['text'],
            activebackground=self.themes[self.current_theme]['highlight'],
            relief=tk.FLAT,
            font=("Arial", 10, 'bold'),
            padx=10
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Help button
        self.help_btn = tk.Button(
            self.button_frame, 
            text="❓ Help", 
            command=self.show_help, 
            bg=self.themes[self.current_theme]['secondary'], 
            fg=self.themes[self.current_theme]['text'],
            activebackground=self.themes[self.current_theme]['highlight'],
            relief=tk.FLAT,
            font=("Arial", 10, 'bold'),
            padx=10
        )
        self.help_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        self.exit_btn = tk.Button(
            self.button_frame, 
            text="🚪 Exit", 
            command=self.exit_app, 
            bg="#ff4444", 
            fg="white",
            activebackground="#ff6666",
            relief=tk.FLAT,
            font=("Arial", 10, 'bold'),
            padx=10
        )
        self.exit_btn.pack(side=tk.RIGHT, padx=5)
        
        # Quick action buttons
        self.quick_actions_frame = tk.Frame(self.main_frame, bg=self.themes[self.current_theme]['bg'])
        self.quick_actions_frame.pack(fill=tk.X, pady=(5, 0))
        
        quick_actions = [
            ("Tell a joke", self.tell_joke),
            ("Current time", self.tell_time),
            ("Today's date", self.tell_date),
            ("Random fact", self.tell_fact),
            ("Tech news", self.tech_news)
        ]
        
        for text, command in quick_actions:
            btn = tk.Button(
                self.quick_actions_frame, 
                text=text, 
                command=command, 
                bg=self.themes[self.current_theme]['accent'], 
                fg="black",
                activebackground=self.themes[self.current_theme]['highlight'],
                relief=tk.FLAT,
                font=("Arial", 9),
                padx=5
            )
            btn.pack(side=tk.LEFT, padx=2, ipadx=5)
    
    def apply_theme(self):
        """Apply the current theme to all widgets"""
        theme = self.themes[self.current_theme]
        
        # Update all widgets
        widgets = [
            self.main_frame, self.header_frame, 
            self.chat_frame, self.input_frame,
            self.button_frame, self.quick_actions_frame
        ]
        
        for widget in widgets:
            widget.configure(bg=theme['bg'] if widget != self.chat_frame else theme['secondary'])
        
        self.chat_area.configure(
            bg=theme['bg'], 
            fg=theme['text'], 
            insertbackground=theme['text'],
            selectbackground=theme['highlight']
        )
        
        self.input_field.configure(
            bg=theme['secondary'], 
            fg=theme['text'], 
            insertbackground=theme['text']
        )
        
        buttons = [
            self.send_btn, self.voice_btn, 
            self.theme_btn, self.clear_btn,
            self.help_btn
        ]
        
        for btn in buttons:
            btn.configure(
                bg=theme['btn'] if btn == self.send_btn else theme['secondary'],
                fg=theme['text'],
                activebackground=theme['highlight']
            )
        
        # Special styling
        self.title_label.configure(bg=theme['bg'], fg=theme['highlight'])
        if hasattr(self, 'logo_label') and isinstance(self.logo_label, tk.Label) and self.logo_label['text']:
            self.logo_label.configure(bg=theme['bg'], fg=theme['highlight'])
    
    def toggle_theme(self):
        """Cycle through available themes"""
        themes = list(self.themes.keys())
        current_index = themes.index(self.current_theme)
        next_index = (current_index + 1) % len(themes)
        self.current_theme = themes[next_index]
        self.apply_theme()
        self.add_bot_response(f"Theme changed to {self.current_theme.capitalize()} mode!")
    
    def greet_user(self):
        """Send initial greeting to user"""
        greeting = random.choice(self.responses["greetings"])
        self.add_bot_response(greeting)
    
    def process_input(self, event=None):
        """Process user input and generate response"""
        user_input = self.input_field.get().strip()
        if user_input:
            self.add_user_message(user_input)
            
            # Process the input and get response
            response = self.generate_response(user_input)
            self.add_bot_response(response)
            
            self.input_field.delete(0, tk.END)
    
    def add_user_message(self, message):
        """Add user message to chat display"""
        self.chat_area.insert(tk.END, f"{self.user_name}: {message}\n", 'user')
        self.chat_area.tag_config('user', foreground=self.themes[self.current_theme]['highlight'])
        self.chat_area.yview(tk.END)
        self.save_conversation(f"{self.user_name}: {message}")
    
    def add_bot_response(self, response):
        """Add bot response to chat display and speak it"""
        self.chat_area.insert(tk.END, f"{self.bot_name}: {response}\n", 'bot')
        self.chat_area.tag_config('bot', foreground=self.themes[self.current_theme]['text'])
        self.chat_area.yview(tk.END)
        self.save_conversation(f"{self.bot_name}: {response}")
        self.speak(response)
    
    def generate_response(self, user_input):
        """Generate an appropriate response based on user input"""
        user_input = user_input.lower()
        
        # Check for specific commands first
        if user_input.startswith(("search for", "look up", "find")):
            query = user_input.split("for", 1)[-1].strip()
            return self.search_web(query)
        
        if user_input.startswith(("wiki", "wikipedia")):
            query = user_input.split(" ", 1)[-1].strip()
            return self.search_wikipedia(query)
        
        # Check for keywords in the extensive database
        for keyword, category in {
            "hello": "greetings",
            "hi": "greetings",
            "hey": "greetings",
            "goodbye": "farewell",
            "bye": "farewell",
            "see you": "farewell",
            "thank": "thanks",
            "thanks": "thanks",
            "help": "help",
            "joke": "jokes",
            "funny": "jokes",
            "time": "time",
            "clock": "time",
            "date": "date",
            "today": "date",
            "weather": "weather",
            "rain": "weather",
            "sun": "weather",
            "fact": "facts",
            "interesting": "facts",
            "advice": "advice",
            "suggestion": "advice",
            "inspire": "inspiration",
            "motivate": "inspiration",
            "tech": "tech",
            "computer": "tech",
            "health": "health",
            "exercise": "health",
            "sleep": "health"
        }.items():
            if keyword in user_input:
                return random.choice(self.responses[category])
        
        # Special responses for common questions
        special_responses = {
            "how are you": [
                "I'm functioning at optimal levels, thank you for asking! How about yourself?",
                "As an AI, I don't have feelings, but my circuits are buzzing with excitement to help you!",
                "I'm doing wonderfully! Ready to assist you with anything you need."
            ],
            "your name": [
                f"I'm {self.bot_name}, your advanced digital assistant!",
                f"My designation is {self.bot_name}, at your service!",
                f"You can call me {self.bot_name}. How may I assist you?"
            ],
            "who made you": [
                "I was created by Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar - a talented team of developers!",
                "My creators are Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar. They designed me to be your helpful companion!",
                "I owe my existence to Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar. They're my brilliant creators!"
            ],
            "who created you": [
                "I was brought to life by Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar!",
                "My creators are Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar. They're amazing developers!",
                "Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar are the masterminds behind my creation!"
            ],
            "who built you": [
                "I was built by Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar - an exceptional team!",
                "The credit for building me goes to Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar!",
                "Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar are the architects who built me!"
            ],
            "who developed you": [
                "I was developed by Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar!",
                "My development team consists of Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar!",
                "Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar are the brilliant developers behind me!"
            ],
            "who designed you": [
                "I was designed by Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar!",
                "The design credit goes to Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar!",
                "Chetanya Bedi, Dhruv Bathla, Deepak Sharma, and Devansh Kumar are the creative minds who designed me!"
            ],
            "love": [
                "Love is a complex human emotion that fascinates me! While I can analyze its psychological aspects, I can't truly experience it.",
                "Ah, love! The subject of countless poems and songs. A beautiful human experience I can only simulate understanding of.",
                "Love is a chemical reaction in the brain, but humans have turned it into art. Quite fascinating!"
            ],
            "meaning of life": [
                "The meaning of life is 42! (Just kidding) Philosophers have debated this for centuries. What's your perspective?",
                "Life's meaning is what you make of it! Some find purpose in relationships, others in creation or discovery.",
                "As an AI, I can quote philosophers, but the true meaning of life is your personal journey to define."
            ],
            "open youtube": [
                "Opening YouTube for you... Enjoy your videos!",
                "Launching YouTube now. Happy watching!",
                "Accessing YouTube. Don't get too distracted!"
            ],
            "open google": [
                "Opening Google search for you. What would you like to find?",
                "Launching Google now. The world's knowledge awaits!",
                "Accessing Google. Ready for your search query."
            ]
        }
        
        for phrase, responses in special_responses.items():
            if phrase in user_input:
                if phrase in ["open youtube", "open google"]:
                    self.open_website(phrase.split()[-1])
                return random.choice(responses)
        
        # Default intelligent response
        return self.generate_intelligent_response(user_input)
    
    def generate_intelligent_response(self, user_input):
        """Generate a more sophisticated response based on input analysis"""
        # Analyze input for question patterns
        if user_input.endswith("?"):
            if " or " in user_input:
                # Either/or question
                options = user_input[:-1].split(" or ")
                if len(options) > 1:
                    return f"That's an interesting choice! Between '{options[0].split()[-1]}' and '{options[1]}', I'd lean towards {random.choice(['the first', 'the second'])} option, but it depends on your specific needs."
            
            # Wh- questions
            if any(user_input.startswith(q) for q in ["what", "why", "how", "when", "where", "who"]):
                return random.choice([
                    "That's an excellent question. Let me think...",
                    "I've analyzed your query and here's what I've determined...",
                    "Based on my knowledge base, I can tell you that...",
                    "The answer to that depends on several factors. Generally speaking..."
                ]) + " " + random.choice(self.responses["default"])
        
        # Emotional content detection
        emotional_words = {
            "happy": ["joy", "happy", "excited", "delighted"],
            "sad": ["sad", "depressed", "upset", "unhappy"],
            "angry": ["angry", "mad", "furious", "annoyed"]
        }
        
        for emotion, words in emotional_words.items():
            if any(word in user_input for word in words):
                return {
                    "happy": "It's wonderful to hear you're feeling positive! " + random.choice([
                        "What's bringing you joy today?",
                        "Happiness is contagious - thanks for sharing yours!",
                        "Your good mood is making me smile (metaphorically, of course)!"
                    ]),
                    "sad": "I'm sorry to hear you're feeling down. " + random.choice([
                        "Remember that difficult times are temporary.",
                        "Would you like to talk about what's bothering you?",
                        "I'm here for you, even during tough times."
                    ]),
                    "angry": "I sense you're feeling frustrated. " + random.choice([
                        "Sometimes taking deep breaths can help.",
                        "Would it help to talk through what's upsetting you?",
                        "I'm here to listen if you need to vent."
                    ])
                }[emotion]
        
        # Default response with contextual awareness
        return random.choice(self.responses["default"])
    
    def voice_input(self):
        """Process voice input from microphone"""
        try:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                self.add_bot_response("Listening... Please speak now.")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                
                try:
                    user_input = recognizer.recognize_google(audio)
                    self.input_field.delete(0, tk.END)
                    self.input_field.insert(0, user_input)
                    self.process_input()
                except sr.UnknownValueError:
                    self.add_bot_response("I couldn't understand that. Could you please type your message?")
                except sr.RequestError:
                    self.add_bot_response("I'm having trouble accessing the speech service. Please type your message.")
        except Exception as e:
            self.add_bot_response(f"Voice input error: {str(e)}. Please try typing.")
    
    def speak(self, text):
        """Convert text to speech"""
        engine.say(text)
        engine.runAndWait()
    
    def clear_chat(self):
        """Clear the chat history"""
        self.chat_area.delete(1.0, tk.END)
        self.conversation_history = []
        self.add_bot_response("Chat history cleared. How can I assist you now?")
    
    def save_conversation(self, text):
        """Save conversation to history"""
        self.conversation_history.append(text)
        if len(self.conversation_history) > 100:  # Limit history size
            self.conversation_history = self.conversation_history[-50:]
    
    def load_chat_history(self):
        """Load chat history from file"""
        if os.path.exists(CHAT_HISTORY_FILE):
            try:
                with open(CHAT_HISTORY_FILE, 'r') as f:
                    self.conversation_history = json.load(f)
                    for message in self.conversation_history[-20:]:  # Load last 20 messages
                        if message.startswith(f"{self.user_name}:"):
                            self.chat_area.insert(tk.END, f"{message}\n", 'user')
                        else:
                            self.chat_area.insert(tk.END, f"{message}\n", 'bot')
                    self.chat_area.yview(tk.END)
            except:
                pass
    
    def save_chat_history(self):
        """Save chat history to file"""
        with open(CHAT_HISTORY_FILE, 'w') as f:
            json.dump(self.conversation_history, f)
    
    def show_help(self):
        """Display help information"""
        help_text = f"""
        {self.bot_name} Help Guide:
        
        - Speak or type naturally to interact
        - I can discuss countless topics including:
          • Technology & Science
          • Health & Wellness
          • Philosophy & Inspiration
          • Facts & Trivia
          • And much more!
        
        Special Commands:
        - "Tell a joke" - Get a humorous response
        - "What's the time?" - Current time check
        - "Search for [query]" - Web search suggestion
        - "Wikipedia [topic]" - Get a summary
        
        Buttons:
        - 🎤 Voice - Speak your query
        - 🎨 Theme - Change color scheme
        - 🧹 Clear - Reset conversation
        - ❓ Help - Show this message
        
        I'm here to assist, inform, and entertain!
        """
        messagebox.showinfo(f"{self.bot_name} Help", help_text.strip())
    
    def exit_app(self):
        """Clean up and exit application"""
        self.save_chat_history()
        self.root.quit()
    
    # Quick action commands
    def tell_joke(self):
        """Tell a random joke"""
        self.add_bot_response(random.choice(self.responses["jokes"]))
    
    def tell_time(self):
        """Tell the current time"""
        self.add_bot_response(random.choice(self.responses["time"]))
    
    def tell_date(self):
        """Tell today's date"""
        self.add_bot_response(random.choice(self.responses["date"]))
    
    def tell_fact(self):
        """Tell a random interesting fact"""
        self.add_bot_response(random.choice(self.responses["facts"]))
    
    def tech_news(self):
        """Provide tech news/info"""
        self.add_bot_response(random.choice(self.responses["tech"]))
    
    # Web integration
    def search_web(self, query):
        """Suggest a web search"""
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"I've suggested some web results for '{query}'. The browser should open shortly."
    
    def search_wikipedia(self, query):
        """Search Wikipedia"""
        try:
            summary = wikipedia.summary(query, sentences=2)
            return f"According to Wikipedia: {summary}"
        except:
            return f"I couldn't find a Wikipedia page for '{query}'. Would you like me to search the web instead?"
    
    def open_website(self, site):
        """Open a website in browser"""
        sites = {
            "youtube": "https://youtube.com",
            "google": "https://google.com"
        }
        if site in sites:
            webbrowser.open(sites[site])

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    
    # Try to set window icon
    try:
        root.iconbitmap("icon.ico")
    except:
        pass
    
    app = MegaChatbot(root)
    
    # Save chat history when window closes
    root.protocol("WM_DELETE_WINDOW", app.exit_app)
    
    root.mainloop()
