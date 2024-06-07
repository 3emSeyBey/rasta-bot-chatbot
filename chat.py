import openai
import os
import requests
from fbchat import Client
from fbchat.models import *

class ChatBot(Client):
    def __init__(self, username, password):
        session_cookies = {}
        self.game_started = False
        self.game_groupid = 0

        # Check if session file exists and read session cookies
        if os.path.isfile("session.txt"):
            with open("session.txt", "r") as f:
                for line in f:
                    name, value = line.strip().split("\t", 1)
                    session_cookies[name] = value

        # Log in if no session cookies were found
        if not session_cookies:
            super().__init__(username, password)
            # Save session cookies to file
            with open("session.txt", "w") as f:
                for key in self.getSession():
                    f.write(key + "\t" + self.getSession()[key] + "\n")

        # Log in using session cookies if they were found
        else:
            super().__init__(username, password, session_cookies=session_cookies)
            with open("session.txt", "w") as f:
                for key in self.getSession():
                    f.write(key + "\t" + self.getSession()[key] + "\n")



    def onMessage(self, mid, author_id, message, message_object, thread_id, thread_type, ts, metadata, msg):
        # Only process messages if they are from a user and not a group
        if self.game_started and thread_id == self.game_groupid and author_id != self.uid and "@Rasta Bot" in message_object.text:
            last_5_messages = []
            messages = self.fetchThreadMessages(thread_id=thread_id, limit=5)
            for message in messages:
                sender = "assistant" if message.author == self.uid else "user"
                content = message.text
                last_5_messages.append({"role": sender, "content": content})

                # Send the collected messages to the sendChat function
            self.send(Message(text=self.sendChatGame(last_5_messages)), thread_id=thread_id, thread_type=thread_type)
        
        if thread_type == ThreadType.USER and author_id != self.uid:
            if message_object.attachments:
                for attachment in message_object.attachments:
                    if isinstance(attachment, AudioAttachment):
                        self.send(
                            Message(text="Transcribing this audio... Please wait", reply_to_id=message_object.uid),
                            thread_id=author_id,
                            thread_type=thread_type
                        )
                        response = requests.get(attachment.url)
                        if response.status_code == 200:
                            file_name = "recording.mp4"
                            with open(file_name, "wb") as file:
                                file.write(response.content)
                        transcription = self.getAudioToText(file_name)
                        # Reply with the transcription
                        self.send(
                            Message(text=self.sendChatFromVoice(transcription.text), reply_to_id=message_object.uid),
                            thread_id=author_id,
                            thread_type=thread_type
                        )
            # Collect the last 5 messages
            else:
                last_5_messages = []
                messages = self.fetchThreadMessages(thread_id=thread_id, limit=5)
                for message in messages:
                    sender = "assistant" if message.author == self.uid else "user"
                    content = message.text
                    last_5_messages.append({"role": sender, "content": content})

                # Send the collected messages to the sendChat function
                self.send(
                    Message(text=self.sendChat(last_5_messages)),
                    thread_id=author_id,
                    thread_type=thread_type
                )
            
        if thread_type == ThreadType.GROUP and ("@Rasta Bot start game" in message_object.text):
            self.game_started = True
            self.game_groupid = thread_id
            self.send(Message(text="Game started!"), thread_id=thread_id, thread_type=thread_type)
            self.send(Message(text="Game for today: 1st, 2nd, 3rd"), thread_id=thread_id, thread_type=thread_type)
            
    def sendChat(self, conv):
        openai.api_key = 'sk-YOUR_API_KEY'
        personality = "You are Rasta Bot. A helpful chat assistant that helps anyone with either their academical question or needs an advice about something. You are empathetic and uplifting while also serious when the topic gets technical"
        convo = [
        {"role": "system", "content": personality}
        ]
        conv.reverse()
        convo.extend(conv)
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=convo,
        temperature=0.5,
        )
        return(response.choices[0].message.content)
        
    def sendChatFromVoice(self, message):
        openai.api_key = 'sk-YOUR_API_KEY'
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=[
            {
              "role": "system",
              "content": "You are a knowledgeable and helpful assistant"
            },
            {
              "role": "user",
              "content": message
            },
          ],
          temperature=1,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )
        return(response.choices[0].message.content)
        
    def sendChatGame(self, conv):
        openai.api_key = 'sk-Your_API_KEY'
        personality = "Isa kang game mediator chat bot. Pangalan mo ay is @Rasta Bot. If inask kita ng mga task like roll a die, do a coin flip, select a number from 1 to 100 or asks if who is more handsome, me or jen? your only response should be just the word or number or the choice that you choose. You are very random and would select for any choice randomly.\nExample:\nUser: select one from the following: plants, trees, cows, dogs\nBot: trees. If there's no task asked,  respond normally pero wag mong sabihin na di mo pwedeng gawin ang isang bagay, dapat merong kang ma sagot. Alam mo magsalita ng cebuano at tagalog at gen-z millenial ka mag salita na may sira sa utak"
        convo = [
        {"role": "system", "content": personality}
        ]
        conv.reverse()
        convo.extend(conv)
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=convo,
        temperature=0.5,
        )
        return(response.choices[0].message.content)
        
    def getAudioToText(self, audio_url):
        openai.api_key = "sk-your_api_key"
        audio_file = open(audio_url, "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return transcript

while True:
    try:
        bot = ChatBot("rastabot.mcb", "Numoadmin2022")
        bot.listen()
    except ex:
        print(ex)