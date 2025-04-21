import json
import os
from collections import deque
from datetime import datetime
import uuid


class ConversationHistory:
    """Manages chatbot conversation history with a capped size and persistence."""
    
    def __init__(self, file_path, max_size=10, history_file="conversation_history.json"):
        self.max_size = max_size
        self.history = deque(maxlen=max_size)
        self.history_file = os.path.join(file_path, history_file)
        self.load_history()

    def load_history(self):
        """Load conversation history from file if it exists."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    loaded_history = json.load(f)
                    self.history = deque(loaded_history, maxlen=self.max_size)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading conversation history: {e}")
                self.history = deque(maxlen=self.max_size)

    def save_history(self):
        """Save conversation history to file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.history), f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving conversation history: {e}")

    def add_user_message(self, text, image_paths=None):
        """Add a user message to the history."""
        message = {
            "role": "user",
            "text": text or "",
            "image_paths": image_paths or [],  # Base64 strings or file paths
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())
        }
        self.history.append(message)
        self.save_history()

    def add_bot_message(self, description, image_paths, image_ids):
        """Add a bot message to the history."""
        message = {
            "role": "bot",
            "text": description,
            "image_paths": image_paths,
            "image_ids": image_ids,
            "timestamp": datetime.now().isoformat(),
            "id": str(uuid.uuid4())
        }
        self.history.append(message)
        self.save_history()

    def get_history(self):
        """Return the current conversation history as a list."""
        return list(self.history)

    def get_last_n(self, n=5):
        """Return the last n entries from history."""
        return list(self.history)[-n:]

    def clear(self):
        """Clear the conversation history."""
        self.history.clear()
        self.save_history()

