# Rasta Bot

Rasta Bot is a Facebook Messenger chatbot that leverages the fbchat module and OpenAI's GPT-3.5 to provide an engaging and interactive user experience. This bot can participate in text and audio conversations, manage group games, and provide helpful responses to a variety of queries.

## Features

- **Text Conversation:** Responds to user messages with context-aware answers.
- **Audio Transcription:** Transcribes audio messages and responds based on the transcription.
- **Group Games:** Starts and manages group games with simple commands.
- **Session Management:** Uses session cookies to maintain login state.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/rasta-bot.git
    cd rasta-bot
    ```

2. **Install required libraries:**
    ```sh
    pip install fbchat openai requests
    ```

3. **Set up OpenAI API Key:**
    Replace `'sk-YOUR_API_KEY'` with your actual OpenAI API key in the `sendChat`, `sendChatFromVoice`, `sendChatGame`, and `getAudioToText` methods.

## Usage

1. **Run the bot:**
    ```sh
    python chat.py
    ```

2. **Interacting with the bot:**
    - **One-on-One Chat:**
        - Send a message to the bot, and it will respond contextually.
    - **Audio Transcription:**
        - Send an audio message, and the bot will transcribe and respond to the content.
    - **Group Game:**
        - In a group chat, type `@Rasta Bot start game` to start a game.

## Code Overview

### Initialization

```python
class ChatBot(Client):
    def __init__(self, username, password):
        session_cookies = {}
        self.game_started = False
        self.game_groupid = 0
        # Session management code
        # Login code
```

### Message Handling

```python
def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg):
    # Processing user messages and group messages
```

### Sending Chat Messages

```python
def sendChat(self, conv):
    # Generate responses using OpenAI GPT-3.5
```

### Audio Transcription

```python
def getAudioToText(self, audio_url):
    # Transcribe audio using OpenAI's Whisper model
```

### Group Games

```python
def sendChatGame(self, conv):
    # Manage group game interactions
```

## Example

Here is an example of how Rasta Bot interacts in a conversation:

- **User:** "Hello, Rasta Bot!"
- **Rasta Bot:** "Hello! How can I assist you today?"

For audio messages, the bot transcribes the audio and provides a relevant response. In group settings, users can initiate games and receive automated responses from the bot.

## Contributing

We welcome contributions to enhance Rasta Bot. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
