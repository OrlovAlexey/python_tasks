import argparse
import random
import string


alphabet_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
alphabet_eng = [letter for letter in string.ascii_lowercase]

class TextError(Exception):
    def __init__(self, text):
        self.txt = text

def caesar(input_str, bias = 3, language = "eng"):
    """ Caesar encryption algorithm
        input_str is the string to encrypt
        bias is the key (shifts the alphabet bias times to the right)
        language can be "eng" or "rus"
    """
    
    if language == "eng":
        alphabet = alphabet_eng
    elif language == "rus":
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

def caesar_decryption(input_str, bias = 3, language = "eng"):
    return caesar(input_str, -bias, language)


def vigenere(input_str, key_word, language = "eng"):
    """ Vigenere encryption
        input str : string
        key_word : string
        language : "eng", "rus"
    """
    
    if language == "eng":
        alphabet = alphabet_eng
    elif language == "rus":
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


def vigenere_decryption(input_str, key_word, language = "eng"):
    
    if language == "eng":
        alphabet = alphabet_eng
    elif language == "rus":
        alphabet = alphabet_rus
    
    reversed_key_word = []
    key_word = key_word.lower()
    for letter in key_word:
        reversed_key_word.append(alphabet1[len(alphabet) - alphabet.index(letter)])
    reversed_key_word = ''.join(reversed_key_word)
    return vigenere(input_str, reversed_key_word, language)


def vernam(input_str, key_str):
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

def vernam_decryption(input_str, key_str):
    return vernam(input_str, key_str)


def frequency_analysis(input_str, language = "eng"):
    """ Frequency Caesar decryption algorithm based on most commoly used letter
        input_str = string to decrypt
        language = {"eng", "rus"}
    """
    
    if language == "eng":
        alphabet = alphabet_eng
        most_commoly_used_letter_index = alphabet.index('e')
    elif language == "rus":
        alphabet = alphabet_rus
        most_commoly_used_letter_index = alphabet.index('о')
    
    frequency_rate = [0] * len(alphabet)
    for letter in input_str.lower():
        if letter.isalpha():
            frequency_rate[alphabet.index(letter)] += 1
            
    most_common_letter_index = frequency_rate.index(max(frequency_rate))
    bias = most_common_letter_index - most_commoly_used_letter_index
    return caesar_decryption(input_str, bias, language)

def main():
    parser = argparse.ArgumentParser(description="A normal console arguments parser")
    parser.add_argument("--language", choices=["eng", "rus"], default="eng", type=str, help="This is supported language(english or russian)")
    parser.add_argument("--mode", choices=["encryption", "decryption"], default="encryption", type=str, help="This is mode of cryptography(encryption or decryption)")
    parser.add_argument("--type", choices=["caesar", "viginere", "vernam", "frequency_analysis"], default="caesar", type=str, help="This is type of encryption(caesar, vigenere, vernam) or decryption(caesar, vigenere, vernam, frequency_analysis)")
    parser.add_argument("--input_file", required=True, type=str, help="This a path to text-file to encrypt/decrypt")
    args = parser.parse_args()

    with open(args.input_file, 'r') as input_file:
        input_str = input_file.read()
    with open(args.mode + ".py", 'w') as output_file:
        if args.mode == "encryption":
            if args.type == "caesar":
                bias = int(input("Enter the bias, please: "))
                output_file.write(caesar(input_str, bias, args.language))
            elif args.type == "viginere":
                keyword = str(input("Enter the keyword, please: "))
                output_file.write(viginere(input_str, keyword, args.language))
            elif args.type == "vernam":
                keyword = ''.join([chr(random.randint(ord('A'), ord('z'))) for i in range(len(input_str))])
                print("Your generated keyword:", keyword)
                output_file.write(vernam(input_str, keyword))
        elif args.mode == "decryption":
            if args.type == "caesar":
                bias = int(input("Enter the bias, please: "))
                output_file.write(caesar_decryption(input_str, bias, args.language))
            elif args.type == "viginere":
                keyword = str(input("Enter the keyword, please: "))
                output_file.write(viginere_decryption(input_str, keyword, args.language))
            elif args.type == "vernam":
                key_str = str(input("Enter your keystring, please: "))
                output_file.write(vernam_decryption(input_str, key_str))
            elif args.type == "frequency_analysis":
                output_file.write(frequency_analysis(input_str, args.language))
        print("All has been written to", args.mode + ".py")

if __name__ == "__main__":
    main()
