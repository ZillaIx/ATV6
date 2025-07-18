from pyrogram import Client, filters
from pyrogram.errors import RPCError

target_channel_id = -1002238854475
allowed_user_ids = [7484467266, 5046008695, 7808944025, 6368532633, 7102950493, 7503766983, 2143000075] # REPLACE with the actual numeric IDs of the users
                   #    SILO        ED         SKUNKY    JOSH_RIP     NOTXENOS   AUTO_T_V6      ZILLA
destination_chat_username = "@v8journal" # Your forwarding destination

sent_strings = set()

app = Client("v_eight")


@app.on_message(filters.chat(target_channel_id))
async def my_handler(client, message):
    print(f"Received message: {message.id}")
    
    # Ensure the message is from the target channel
    if message.chat and message.chat.id == target_channel_id:
        # Check if the message is from one of the allowed users
        if message.from_user and message.from_user.id in allowed_user_ids:
            # Ensure the message has text content
            if message.text:
                keywords = ['bonk', 'pump', 'moon', 'jups']
                message_text_lower = message.text.lower()
                
                found_string = None
                # Iterate through words/segments to find the specific string
                for word in message.text.split():
                    # Check if the word meets the length requirement and contains any of the keywords
                    if len(word) >= 43 and any(keyword in word.lower() for keyword in keywords):
                        found_string = word
                        break # Found the string, no need to check further words
                
                if found_string:
                    # --- NEW DEDUPLICATION CHECK: Check if this exact string has already been sent ---
                    if found_string in sent_strings:
                        print(f"DEBUG: Extracted string '{found_string}' from message {message.id} has already been sent, skipping duplicate.")
                        return # Exit the handler for this message
                    
                    try:
                        # Use send_message to send only the extracted string
                        await client.send_message(
                            chat_id=destination_chat_username,
                            text=found_string
                        )
                        # --- UPDATED: Add the extracted string to the set upon successful sending ---
                        sent_strings.add(found_string)
                        print(f"DEBUG: Successfully extracted and sent string '{found_string}' from message {message.id} to {destination_chat_username}.")
                    except RPCError as e:
                        print(f"DEBUG: RPCError during sending extracted string from message {message.id}: {e}")
                    except Exception as e:
                        print(f"DEBUG: Unexpected error during sending extracted string from message {message.id}: {e}")
                else:
                    print(f"DEBUG: Message {message.id} from allowed user did not contain a string meeting length (>=43) and keyword criteria.")
            else:
                print(f"DEBUG: Message {message.id} from allowed user has no text content, skipping processing.")
       # else:
        #    print(f"DEBUG: Message {message.id} not from an allowed user, skipping processing.")
   # else:
    #    print("DEBUG: Message not from target channel, skipping processing.")


app.run()
