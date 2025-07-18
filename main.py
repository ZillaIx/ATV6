import os
from dotenv import load_dotenv
import asyncio
from pyrogram import Client

load_dotenv() # This line loads the variables from your .env file locally

# Get the API ID and Hash from environment variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# Important: Convert API_ID to an integer, as Pyrogram expects it
if API_ID:
    try:
        API_ID = int(API_ID)
    except ValueError:
        print("Error: API_ID environment variable must be an integer.")
        exit(1) # Or handle this error appropriately

if not API_HASH:
    print("Error: API_HASH environment variable not set.")
    exit(1) # Or handle this error appropriately

# Configuration variables
CHANNEL_USERNAME = "solearlytrending" # Set this to your target channel
TARGET_USER = [-1002751333878, -1002238854475]
PREFIX_TO_REMOVE = "https://t.me/soul_sniper_bot?start=15_" # The specific prefix to remove from URLs

async def get_last_messages():
    """
    Connects to Telegram, retrieves the last 3 messages from the specified channel,
    extracts and processes specific URLs, and sends unique processed URLs to a target user.
    This process is repeated x times with seconds delay between repetitions.
    """
    # Initialize a set to store URLs that have already been successfully sent
    # This prevents sending duplicate URLs across multiple iterations.
    sent_urls = set()

    # Initialize the Pyrogram Client.
    # "my_account" is the session name. If it doesn't exist, Pyrogram will ask
    # you to log in the first time you run the script.
    # MODIFIED: Passing api_id and api_hash from environment variables
    async with Client("my_account", api_id=API_ID, api_hash=API_HASH) as app:
        # Outer loop to repeat the process x times
        for iteration in range(999999):
            print(f"\n--- Starting message processing iteration {iteration + 1} ---")
            try:
                # Retrieve the last 3 messages from the channel
                # The limit is now set to 3 as requested.
                async for message in app.get_chat_history(CHANNEL_USERNAME, limit=3):
                    message_content = None
                    message_type_display = "[UNKNOWN CONTENT TYPE]" # Default in case nothing matches
                    processed_url = None # Variable to store the *processed* URL (only one, if found and modified)
                    entities_to_check = None # Default for message entities

                    # --- Content Extraction and URL Collection ---
                    # Prioritize caption, then text, then other media types
                    if message.caption:
                        message_content = message.caption
                        message_type_display = "message.caption"
                        entities_to_check = message.caption_entities
                    elif message.text:
                        message_content = message.text
                        message_type_display = "message.text"
                        entities_to_check = message.entities
                    elif message.photo:
                        message_type_display = "message.photo"
                        message_content = f"[Photo] File ID: {message.photo.file_id}"
                        entities_to_check = message.caption_entities
                    elif message.video:
                        message_type_display = "message.video"
                        message_content = f"[Video] File ID: {message.video.file_id}"
                        entities_to_check = message.caption_entities
                    elif message.document:
                        message_type_display = "message.document"
                        message_content = f"[Document] File Name: {message.document.file_name or 'N/A'}"
                        entities_to_check = message.caption_entities
                    elif message.poll:
                        message_type_display = "message.poll"
                        message_content = f"[Poll] Question: {message.poll.question} (ID: {message.poll.id})"
                        entities_to_check = None # Polls typically don't have entities for URLs
                    elif message.web_page:
                        message_type_display = "message.web_page"
                        message_content = f"[Web Page Preview] Title: {message.web_page.title or 'N/A'} URL: {message.web_page.url or 'N/A'}"
                        # Check web_page URL directly and process it if it contains the prefix
                        if message.web_page.url and PREFIX_TO_REMOVE in message.web_page.url:
                            processed_url = message.web_page.url.replace(PREFIX_TO_REMOVE, "")
                        entities_to_check = None # Web page URLs are handled directly, no need to check entities
                    else:
                        message_content = f"[{message_type_display} - No extractable text/caption]"
                        entities_to_check = None

                    # --- Iterate through entities to find ONLY THE FIRST URL that matches the criteria ---
                    # Only check entities if no URL was processed from web_page type yet
                    if not processed_url and entities_to_check:
                        for entity in entities_to_check:
                            # Check if entity has a URL AND if that URL contains the specific prefix
                            if entity.url and PREFIX_TO_REMOVE in entity.url:
                                processed_url = entity.url.replace(PREFIX_TO_REMOVE, "")
                                break # Stop after finding and processing the first matching URL!

                    # --- Print extracted details to console ---
                    print(f"\n--- Message Details (Iteration {iteration + 1}) ---")
                    print(f"Message Type Used: {message_type_display}")
                    print(f"Message Content:\n{message_content}")

                    if processed_url:
                        print(f"--- Processed URL Part: {processed_url} ---")
                        # --- Send Processed URL Part to Target User (only if new) ---
                        if processed_url not in sent_urls:
                            message_to_send = f"In This: \n- {processed_url}\n"
                            for user_id in TARGET_USER: # Iterate through each user ID
                                try:
                                    await app.send_message(
                                        chat_id=user_id, # Use the current user_id from the loop
                                        text=message_to_send
                                    )
                                    print(f"Successfully sent NEW processed URL part to {user_id}")

                                except Exception as e:
                                    print(f"Failed to send processed URL part to {user_id}: {e}")
                            sent_urls.add(processed_url)
                        else:
                            print(f"--- Skipping duplicate URL: {processed_url} (already sent in a previous check) ---")
                    else:
                        print("--- No matching URLs Extracted or Processed for this message ---")
                    print("----------------------------")

            except Exception as e:
                # Catch and print any errors that occur during message retrieval or processing
                print(f"An error occurred during iteration {iteration + 1}: {e}")

            # Wait for x seconds before the next iteration, unless it's the last one
            if iteration < 999999: # Only wait after x number of iterations
                print(f"\n--- Iteration {iteration + 1} complete. Waiting 10 seconds before next check... ---")
                await asyncio.sleep(60)
            else:
                print("\n--- From July 15th 2025 when you completed AutoTrencherV6 till now\n Congrats bro, you now have more than \n $1M ($1,000,000 +) \n Cash Out and Flex \n Thank Jehovah ---")

asyncio.run(get_last_messages())
