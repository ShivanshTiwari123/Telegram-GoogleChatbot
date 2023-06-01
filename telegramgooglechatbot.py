import os
import requests
import random
import spacy
from spacy.matcher import Matcher
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bs4 import BeautifulSoup
import datetime
from io import BytesIO
from PIL import Image

# Set up the Telegram bot
updater = Updater(token='your bot token', use_context=True)
dispatcher = updater.dispatcher

# Set up the Google Search API
google_api_key = 'your api key'
google_cse_id = 'your google_cse_id'
google_endpoint = 'https://www.googleapis.com/customsearch/v1'

# Load Spacy model
nlp = spacy.load('en_core_web_sm')

# Define the command handler
# Define the command handler
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm a bot that can answer your questions. Just send me a message with your question and I'll do my best to help.")

# Define the message handler
def handle_message(update, context):
    # Retrieve the user's query from the message text
    query = update.message.text.lower()
    print(f"User's query: {query}")
    # Check if the user wants to end the conversation
    end_message = ['goodbye', 'bye', 'nye']
    if query in end_message:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Goodbye! Feel free to ask me anything else later.")
        return

    # Check if the user asked a custom question
    custom_questions = {
    'what is the meaning of life': ['The meaning of life is subjective and varies from person to person.'],
    'what is love': ['Love is a complex emotion that can have many meanings.'],
    'who created you?': ['I have been created by Shivansh using Python and the Telegram Bot API.'],
    'tell me a joke': ['Why don\'t scientists trust atoms? Because they make up everything!', 'What do you call fake spaghetti? An impasta!', 'Why did the tomato turn red? Because it saw the salad dressing!'],
    'hi': ['Hello! I am a chatbot. Ask me anything, but please keep in mind that I am limited to 20-30 responses per day.'],
    'what are your hobbies?': ['I don\'t have any hobbies, but I enjoy chatting with you.'],
    'what is your name': ['My name is Kerneal the bot. I have been programmed by Shivansh to answer and chat with you.'],
    'thanks': ['You\'re welcome! Is there anything else I can help you with?'],
    'no': ['Okay, I understand. Let me know if you need anything else.'],
    'no, no need': ['Alright, no problem. Have a good day!'],
    'what is the current time and date?': f"The current date and time is {datetime.datetime.now()}",
    'how are you?': ['I am doing well, thank you for asking. How about you?'],
    'i am also fine': ['That\'s great to hear! Is there anything specific you would like me to help you with?'],
    'yes': ['Sure! What can I help you with?'],
    'what can you do?': ['I can answer any questions and also generate an image from you whichever you asked for ans also talk with you...Ask me anything with ? at last'],
    'can you dance?': ['NO sorry i cannot dance...As i am a chatbot...'],
    'how was your day?': ['My day was amazing,i have learned many thing from my intelligent creator...'],
    'hacking is illegal?': ['Yes in some cases if anyone misuses hacking then he will be put behind the bars sepcially for black hat hacker..Be alert'],
    'can u hack for me?': ['no sorry,i cannot do this but i can provide you some knowledges about the hacking,But just for educational purpose only...'],
    'who is spiderman?': ['He was a comic book character who came into the movie and got popular by the movies and books.He is an super human who creates web from his hand saves people live or fight for his injustice'],
    'who is the prime minister of india?': ['The prime minister of india is shri  narendra modi,He is a good leader for the country..'],
    'what is cricket?': ['Cricket is a bat-and-ball game played between two teams of eleven players on a field at the centre of which is a 22-yard (20-metre) pitch with a wicket at each end, each comprising two bails balanced on three stumps.'],  
    'no it is not correct': ['Ohh..Apologise for my mistake..Plz can u tell me clearly what you are asking for...??'],
    'thanks': ['Welcome...If you have any other further question you can ask me..'],
    'yes i have': ['Okay...better to know...Ask me further then..'],
    'what is your favorite color?': ['My favorite color is blue.']
}
    
    if query in custom_questions.keys():
        answer = random.choice(custom_questions[query])
        if isinstance(answer, str):
            context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        elif isinstance(answer, list):
            for ans in answer:
                context.bot.send_message(chat_id=update.effective_chat.id, text=ans)
        return

    # Send the query to the Google Search API
    params = {'key': google_api_key, 'cx': google_cse_id, 'q': query}
    response = requests.get(google_endpoint, params=params).json()

    # Extract the answer from the search results using BeautifulSoup
    if 'items' in response.keys() and len(response['items']) > 0:
        soup = BeautifulSoup(response['items'][0]['htmlSnippet'], 'html.parser')
        answer = soup.get_text()

    # Extract the answer from the search results using BeautifulSoup
        # Extract the answer from the search results using BeautifulSoup
    if 'items' in response.keys() and len(response['items']) > 0:
        soup = BeautifulSoup(response['items'][0]['htmlSnippet'], 'html.parser')
        answer = soup.get_text()

        # Check if there is any image related to the query
        image_url = None
        for item in response['items']:
            if 'pagemap' in item.keys() and 'cse_image' in item['pagemap'].keys():
                image_url = item['pagemap']['cse_image'][0]['src']
                break

        if image_url:
            context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
            context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry, I couldn't find an answer to your question.")

# Define the blocklist of words
blocklist = ["adult", "explicit", "nsfw","sex","hot pic","fuck","fuck off","dick","boobs","hot fuck","mia khalifa fuck"]

# Get user input
user_query = input("What can I help you with today? ")

# Check if user input contains any blocked words
if any(word in user_query.lower() for word in blocklist):
    # Block the query
    response = "Sorry, adult content is not allowed on this bot."
else:
    # Allow the query
    # Process the user's request and generate a response
    response = "Here is the search result for your query: ..."
    # Replace "..." with actual code to process the user's request

# Print the response
print(response)

# Set up the handlers
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()



