import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# টেলিগ্রাম বট টোকেন পরিবেশ ভেরিয়েবল থেকে ইনক্লুড করা হয়েছে
TOKEN = os.getenv('TELEGRAM_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Ask me anything.')

def ask_question(update: Update, context: CallbackContext) -> None:
    user_question = update.message.text
    # ইউজারের প্রশ্ন URL এ যুক্ত করা
    api_url = f"https://gemini-pro-green.vercel.app/ask?q={user_question}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        # সঠিক কী ব্যবহার করে রেসপন্স পাওয়া
        answer = data.get('response', 'I did not understand the question.')
        
        # এখানে টেক্সট ফরম্যাট করা হয়েছে
        formatted_answer = format_text(answer)
        
    else:
        formatted_answer = f'Failed to get a response from the API. Status code: {response.status_code}'

    update.message.reply_text(formatted_answer)

def format_text(text: str) -> str:
    import re
    
    # প্রথমে ** এর ভিতরের অংশগুলোকে `•` দিয়ে রিপ্লেস করা
    pattern_double_star = r'\* \*\*(.*?)\*\*'
    formatted_text = re.sub(pattern_double_star, r'• \1', text)
    
    # নতুন ** এর আগের এবং পরের অংশগুলোকে রিমুভ করা
    pattern_remove_double_star = r'\*\*(.*?)\*\*'
    formatted_text = re.sub(pattern_remove_double_star, r'\1', formatted_text)
    
    # তারপর শুধুমাত্র * এর আগের অংশগুলোকে রিমুভ করা
    pattern_single_star = r'\* ([^\*]+)'
    formatted_text = re.sub(pattern_single_star, r'\1', formatted_text)
    
    return formatted_text

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, ask_question))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
