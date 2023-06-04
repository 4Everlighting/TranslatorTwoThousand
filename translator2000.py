#Assignment: Python Project 1
#Joshua Pacheco (JP), 5/14/2023, The Translator Two Thousand, Python3 project
#I am estimating this will take 4 hours to code. It actually took 6 hours, as I had issues with getting the URL entry to work and debugging
#Spent an additional 2 hours adding the Speech to text and text to speech library mod

# sys for bailing out of script runtime with exit method
import sys
# requests for acquiring internet resources for translation 
import requests
# os library for validating local file existence
import os
import speech_recognition as sr
import pyttsx3

#initializes pyttsx3 globally
engine = pyttsx3.init()

#print(engine.getProperty("voice"))
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
#for voice in voices:
 #   print(voice, voice.id)
  #  engine.setProperty('voice', voice.id)
engine.say("Hello I AM the Translator Interface Two Thousand. Please select from the MENU")
engine.runAndWait()
    #engine.stop()
# textblob for translation capability
from textblob import TextBlob
# set minimum text size to consider as valid text to translated
MINIMUM_TEXT_LENGTH = 3
MAX_CHOICE = 6
TRANSLATED_LANGUAGE_FILE = 'selected_language.txt'
RECOGNIZED_LANGUAGE_FILE = 'recognized_language.txt'
LANGUAGE_IDS = {
     "ru":3,
     "es":2,
}
SUPPORTED_LANGUAGES = {
	'Spanish': 'es',
	'Afrikaans': 'af',
	'Japanese': 'ja',
	'Creole': 'ht',
	'Filipino': 'tl',
	'Russian': 'ru',
    'Swahili' : 'sw',
    'English' : 'en',
}
TEXTBLOB_LANGUAGES = {
     'en-us': 'en',
    'es-mx': 'es',


}
class InputValidator(object):
	def __init__(self, prompt_text):
		self.prompt_text = prompt_text
	def is_valid(self):
		return False
  
class FileInputValidator(InputValidator):	
     def is_valid(self):
      return(len(self.prompt_text)>0 and os.path.exists(self.prompt_text))
 
class TextInputValidator(InputValidator):
    def is_valid(self):
      return(len(self.prompt_text)>MINIMUM_TEXT_LENGTH)

class URLInputValidator(InputValidator):
    def is_valid(self):
      return(self.prompt_text.startswith("http://") or self.prompt_text.startswith("https://"))
    
class LanguageInputValidator(InputValidator):
    def is_valid(self):
      return(self.prompt_text in SUPPORTED_LANGUAGES.keys())

class MainMenuInputValidator(InputValidator):
    def is_valid(self):
        return(self.prompt_text.isdigit() and int(self.prompt_text) in range(MAX_CHOICE+1))

# necessary functions
def supported_languages_to_string():
    # convert dictionary to keys seperated by comma -> return string
	return(", ".join(SUPPORTED_LANGUAGES.keys()))
	# validate text size -> return true/false
def validate_text_length(TEXT):
    return(TextInputValidator(TEXT).is_valid())
	# list supported textblob languages -> return list of language names
def list_supported_languages():
	return(SUPPORTED_LANGUAGES.keys())
	# validate a language name -> return true/false
def is_valid_language(LANGUAGE):
    return(LanguageInputValidator(LANGUAGE).is_valid())  
def set_recognized_language(LANGUAGE):
    if LANGUAGE == 'english':
      	with open(RECOGNIZED_LANGUAGE_FILE, 'w') as f:
          f.write("en-us")
          return True
    elif LANGUAGE == 'spanish':
      	with open(RECOGNIZED_LANGUAGE_FILE, 'w') as f:
          f.write("es-mx")
          return True
    print("Error: Invalid recognized language- type english or spanish")
    return None

def set_translated_language(LANGUAGE):
	# record selected language to file -> return true/false
	if not is_valid_language(LANGUAGE):
		print("Error:NOT a possible or valid Language to translate to")
		return None   
	with open(TRANSLATED_LANGUAGE_FILE, 'w') as f:
		f.write(SUPPORTED_LANGUAGES[LANGUAGE])
	return True

def get_recognized_language():
    if not os.path.exists(RECOGNIZED_LANGUAGE_FILE):
        return 'en-us'
    l = ''
    with open(RECOGNIZED_LANGUAGE_FILE, 'r') as f:
     l = f.read()
     
    print(f'Returning lang {l}')
    return(l)
    
def get_translated_language():
	# return language we want to translate to -> return language key (eg, es, ru, etc)
	with open(TRANSLATED_LANGUAGE_FILE, 'r') as f:
		return(f.read())
def translate_text(TEXT):
	if not validate_text_length(TEXT):
		print("Invalid Text length")
		return None
	# translate arbitrary text string to selected language -> return string
	DESTINATION_LANGUAGE_KEY = get_translated_language()
	if DESTINATION_LANGUAGE_KEY in LANGUAGE_IDS.keys():
		voice_id = LANGUAGE_IDS[DESTINATION_LANGUAGE_KEY]
		print(f'requested language of "{DESTINATION_LANGUAGE_KEY}" is supported. configuring pyttsx3 to use voice #{voice_id}')
		engine.setProperty('voice', voices[voice_id].id)
		#engine.say(translated_text)
		#engine.runAndWait()

	else:
		print(f'requested language of "{DESTINATION_LANGUAGE_KEY}" is NOT supported. not overriding pytts language')

	print(f'Translating text "{TEXT}" to language "{DESTINATION_LANGUAGE_KEY}"!')

	b = TextBlob(TEXT)
	SRC_LANG = TEXTBLOB_LANGUAGES[get_recognized_language()]
	print(f'we are translating text "{TEXT}" from "{SRC_LANG}" to "{DESTINATION_LANGUAGE_KEY}"')

	translated_text = b.translate(from_lang=SRC_LANG, to=DESTINATION_LANGUAGE_KEY)
	print(f'Translation: "{translated_text}"')
	with open("result.txt", "w", encoding="utf-8") as f:
		f.write(str(translated_text))
	return(translated_text)
	
def translate_url(URL):
	# read text from uri -> return string
    response = requests.get(URL)       
    return translate_text(response.content.decode())
def translate_file(FILE_PATH):
	# read text from file -> return string
    found = False
    while not found:
      if FileInputValidator(FILE_PATH).is_valid():
        found = True
      else:
        FILE_PATH = input("Enter a valid file path: ")
    with open(FILE_PATH, 'r') as f:
	    return translate_text(f.read())
def get_choice(max_choice):
    while True:
        choice = input("Enter your choice: ")
        if MainMenuInputValidator(choice).is_valid():
            return int(choice)
        else:
            print("Invalid choice. Please enter a valid choice.")
def translate_STT():
             beginText = TextBlob("Okay, please tell me what you would like for me to translate and say")
             engine.say(beginText)
             engine.runAndWait()

             rec = sr.Recognizer()
             with sr.Microphone() as source:
                 print("Please speak...")
                 audio = rec.listen(source)
                 print("Processing...")
                 text = rec.recognize_google(audio, language=get_recognized_language())
                 engine.runAndWait()
                 print(f"What I heard you say:{text}")
                 translated_text = translate_text(text)
                                
                 engine.say(translated_text)
                 engine.runAndWait()
                 
def main():
    while True:
        engine.setProperty('voice', voices[0].id)
        print("\nTranslator Two Thousand MENU:")
        print("1. Choose translated language")
        print("2. Translate from your typed text")
        print("3. Translate text from a URL")
        print("4. Translate text from a Local File")
        print("5. Translate from Speech Recognition and Speak translation")
        print("6. Choose Recognized Language")

        print("0. To Exit the Program")

        choice = get_choice(MAX_CHOICE)

        # Perform the selected task
        if choice == 1:
            ok=False
            while ok==False:
                if set_translated_language(input(f"Enter language ({supported_languages_to_string()}):\n ")) != None:
                    ok=True
                    
        elif choice == 2:
            translate_text(input("Enter Text: "))
        elif choice == 3:
            translate_url(input("Enter URL: "))
        elif choice == 4:
            translate_file(input("Enter File: "))
        elif choice == 5:
             translate_STT()
        elif choice == 6:
            ok=False
            while ok==False:
              if set_recognized_language(input("Enter Recognized Language (english or spanish): ")) != None:
                ok=True
        elif choice == 0:
            sys.exit(0)
# option 1)
	# prompt user for selected language
	# ensure selected language is supported by textblob
	# record selected language to local file
# option 2)
	# prompt user for text
	# ensure text is greater then configurable quantity of bytes
	# translate text based on selected language
# option 3)
	# prompt user for url
	# fetch text from url
	# ensure text is greater then configurable quantity of bytes
	# translate text based on selected language
# option 4) prompt user for local file path
	# read text from local file
	# ensure text is greater then configurable quantity of bytes
	# translate text based on selected language
# option 5) exit program

if __name__ == "__main__":
	main()