#Assignment: Python Project 1
#Joshua Pacheco (JP), 5/14/2023, The Translator Two Thousand
#I am estimating this will take 6 hours to code
# sys for bailing out of script runtime with exit method
import sys
# requests for acquiring internet resources for translatio 
import requests
# os library for validating local file existence
import os
# textblob for translation capability
from textblob import TextBlob
# set minimum text size to consider as valid text to translated
MINIMUM_TEXT_LENGTH = 3
TRANSLATED_LANGUAGE_FILE = 'selected_language.txt'
SUPPORTED_LANGUAGES = {
	'Spanish': 'es',
	'Afrikaans': 'af',
	'Japanese': 'ja',
	'Haitian': 'ht',
	'Filipino': 'tl',
	'Russian': 'ru',
    'Swahili' : 'sw',
}
# necessary functions
def supported_languages_to_string():
    # convert dictionary to keys seperated by comma -> return string
	return(", ".join(SUPPORTED_LANGUAGES.keys()))
	# validate text size -> return true/false
def validate_text_length(TEXT):
	return(len(TEXT)>=MINIMUM_TEXT_LENGTH)
	# list supported textblob languages -> return list of language names
def list_supported_languages():
	return(SUPPORTED_LANGUAGES.keys())
	# validate a language name -> return true/false
def is_valid_language(LANGUAGE):
	return(LANGUAGE in list_supported_languages())
def set_translated_language(LANGUAGE):
	# record selected language to file -> return true/false
	if not is_valid_language(LANGUAGE):
		print("Error:NOT a possible or valid Language to translate to")
		return None   
	with open(TRANSLATED_LANGUAGE_FILE, 'w') as f:
		f.write(SUPPORTED_LANGUAGES[LANGUAGE])
	return True
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
	#print(f'Translating text "{TEXT}" to language "{DESTINATION_LANGUAGE_KEY}"!')
	b = TextBlob(TEXT)
	translated_text = b.translate(from_lang='en', to=DESTINATION_LANGUAGE_KEY)
	print(f'Translation: "{translated_text}"')
	return(translated_text)
def translate_url(URL):
	# read text from uri -> return string
    response = requests.get(URL)
    return translate_text(response.content.decode())
def translate_file(FILE_PATH):
	# read text from file -> return string
    found = False
    while not found:
      if  os.path.exists(FILE_PATH):
        found = True
      else:
        FILE_PATH = input("Enter a valid file path: ")
		
    with open(FILE_PATH, 'r') as f:
	    return translate_text(f.read())
def get_choice(max_choice):
    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and int(choice) in range(max_choice+1):
            return int(choice)
        else:
            print("Invalid choice. Please enter a valid choice.")
def main():
    while True:
        print("\nTranslator Two Thousand MENU:")
        print("1. Select translated language")
        print("2. Translate text")
        print("3. Translate text from URL")
        print("4. Translate text from local file")
        print("0. Exit")

        choice = get_choice(5)

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