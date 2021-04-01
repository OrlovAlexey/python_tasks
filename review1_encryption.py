import string
import argparse
import random


alphabet_rus = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о","п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я"]
alphabet_eng = [letter for letter in string.ascii_lowercase]

class TextError(Exception):
    def __init__(self, text):
        self.txt = text

def Caesar(input_str, bias = 3, language = "eng"):
    """ Caesar encryption algorithm
        input_str is the string to encrypt
        bias is the key (shifts the alphabet bias times to the right)
        language can be "eng" or "rus"
    """
    
    if (language == "eng"):
        alphabet = alphabet_eng
    elif (language == "rus"):
        alphabet = alphabet_rus

    alphabet_length = len(alphabet)
    new_str = []
    for letter in input_str:
        if letter in alphabet:
            new_str.append(alphabet[(alphabet.index(letter) + bias) % alphabet_length])
        elif letter in [i.upper() for i in alphabet]:
            new_str.append(alphabet[(alphabet.index(letter.lower()) + bias) % alphabet_length].upper())
        elif letter.isalpha():
            raise TextError("Wrong alphabet")
        else:
            new_str.append(letter)
    output_str = ''.join(new_str)
    return output_str

def Caesar_decryption(input_str, bias = 3, language = "eng"):
    return Caesar(input_str, -bias, language)


def Vigenere(input_str, key_word, language = "eng"):
    """ Vigenere encryption
        input str : string
        key_word : string
        language : "eng", "rus"
    """
    
    if (language == "eng"):
        alphabet = alphabet_eng
    elif (language == "rus"):
        alphabet = alphabet_rus

    key_word = key_word.lower()
    alphabet_length = len(alphabet)
    new_str = []
    key_length = len(key_word)
    for j in range(len(input_str)):
        letter = input_str[j]
        if letter.isalpha():
            if letter in alphabet:
                new_str.append(alphabet[(alphabet.index(letter) + alphabet.index(key_word[j % key_length])) % alphabet_length])
            elif letter in [i.upper() for i in alphabet]:
                new_str.append(alphabet[(alphabet.index(letter.lower()) + alphabet.index(key_word[j % key_length])) % alphabet_length].upper())
            else:
                raise TextError("Wrong alphabet")
        else:
            new_str.append(letter)
    output_str = ''.join(new_str)
    return output_str


def Vigenere_decryption(input_str, key_word, language = "eng"):
    
    if (language == "eng"):
        alphabet = alphabet_eng
    elif (language == "rus"):
        alphabet = alphabet_rus
    
    reversed_key_word = []
    key_word = key_word.lower()
    for letter in key_word:
        reversed_key_word.append(alphabet1[len(alphabet) - alphabet.index(letter)])
    reversed_key_word = ''.join(reversed_key_word)
    return Vigenere(input_str, reversed_key_word, language)


def Vernam(input_str, key_str):
    """ Vernam encryption algo
        input_str is string to encrypt
        key_str is randomly generated key THE SAME SIZE AS input_str
    """
    print(len(input_str))
    print(len(key_str))
    result = []
    for i in range(len(input_str)):
        result.append(chr(ord(input_str[i]) ^ ord(key_str[i])))
    result = ''.join(result)
    return result

def Vernam_decryption(input_str, key_str):
    return Vernam(input_str, key_str)


def frequency_analysis(input_str, language = "eng"):
    """ Frequency Caesar decryption algorithm based on most commoly used letter
        input_str = string to decrypt
        language = {"eng", "rus"}
    """
    
    if (language == "eng"):
        alphabet = alphabet_eng
        most_commoly_used_letter_index = alphabet.index('e')
    elif (language == "rus"):
        alphabet = alphabet_rus
        most_commoly_used_letter_index = alphabet.index('о')
    
    frequency_rate = [0] * len(alphabet)
    for letter in input_str.lower():
        if letter.isalpha():
            frequency_rate[alphabet.index(letter)] += 1
            
    most_common_letter_index = frequency_rate.index(max(frequency_rate))
    bias = most_common_letter_index - most_commoly_used_letter_index
    return Caesar_decryption(input_str, bias, language)


parser = argparse.ArgumentParser(description="A normal console arguments parser")
parser.add_argument("--language", choices=["eng", "rus"], default="eng", type=str, help="This is supported language(english or russian)")
parser.add_argument("--mode", choices=["encryption", "decryption"], default="encryption", type=str, help="This is mode of cryptography(encryption or decryption)")
parser.add_argument("--type", choices=["caesar", "viginere", "vernam", "frequency_analysis"], default="caesar", type=str, help="This is type of encryption(caesar, vigenere, vernam) or decryption(caesar, vigenere, vernam, frequency_analysis)")
parser.add_argument("--input_file", required=True, type=str, help="This a path to text-file to encrypt/decrypt")
args = parser.parse_args()

with open(args.input_file, 'r') as input_file:
    input_str = input_file.read()
    with open(args.mode + ".py", 'w') as output_file:
        if (args.mode == "encryption"):
            if (args.type == "caesar"):
                bias = int(input("Enter the bias, please: "))
                output_file.write(Caesar(input_str, bias, args.language))
            elif (args.type == "viginere"):
                keyword = str(input("Enter the keyword, please: "))
                output_file.write(Viginere(input_str, keyword, args.language))
            elif (args.type == "vernam"):
                keyword = ''.join([chr(random.randint(65, 122)) for i in range(len(input_str))])
                print("Your generated keyword:", keyword)
                output_file.write(Vernam(input_str, keyword))
        elif (args.mode == "decryption"):
            if (args.type == "caesar"):
                bias = int(input("Enter the bias, please: "))
                output_file.write(Caesar_decryption(input_str, bias, args.language))
            elif (args.type == "viginere"):
                keyword = str(input("Enter the keyword, please: "))
                output_file.write(Viginere_decryption(input_str, keyword, args.language))
            elif (args.type == "vernam"):
                key_str = str(input("Enter your keystring, please: "))
                output_file.write(Vernam_decryption(input_str, key_str))
            elif (args.type == "frequency_analysis"):
                output_file.write(frequency_analysis(input_str, args.language))
        print("All has been written to", args.mode + ".py")

