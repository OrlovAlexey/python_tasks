from abc import abstractmethod
import argparse
import random
import string


alphabet_rus = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
alphabet_eng = string.ascii_lowercase
eng_tag = "eng"
rus_tag = "rus"

class TextError(Exception):
    def __init__(self, text):
        self.txt = text


class AbstractCipher:
    name: str
    def __init__(self):
        pass

    @abstractmethod
    def encrypt(self, input_str: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, input_str: str) -> str:
        pass


class Caesar(AbstractCipher):
    alphabet : str
    name = "caesar"
    def __init__(self, language: str):
        super().__init__()
        if language == eng_tag:
            self.alphabet = alphabet_eng
        elif language == rus_tag:
            self.alphabet = alphabet_rus

    def encrypt(self, input_str: str) -> str:
        bias = int(input("Enter the bias, please: "))
        return self.caesar(input_str, bias)

    def decrypt(self, input_str: str) -> str:
        bias = int(input("Enter the bias, please: "))
        return self.caesar_decryption(input_str, bias)

    def caesar(self, input_str: str, bias: int) -> str:
        """ Caesar encryption algorithm
            input_str is the string to encrypt
            bias is the key (shifts the alphabet bias times to the right)
            language can be "eng" or "rus"
        """
        alphabet = self.alphabet
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
    
    def caesar_decryption(self, input_str: str, bias: int) -> str:
        return self.caesar(input_str, -bias)


class Viginere(AbstractCipher):
    alphabet : str
    name = "viginere"
    def __init__(self, language: str):
        super().__init__()
        if language == eng_tag:
            self.alphabet = alphabet_eng
        elif language == rus_tag:
            self.alphabet = alphabet_rus

    def encrypt(self, input_str: str) -> str:
        keyword = str(input("Enter the keyword, please: "))
        return self.vigenere(input_str, keyword)

    def decrypt(self, input_str: str) -> str:
        keyword = str(input("Enter the keyword, please: "))
        return self.vigenere_decryption(input_str, keyword)

    def vigenere(self, input_str: str, key_word: str) -> str:
        """ Vigenere encryption
            input str : string
            key_word : string
            language : "eng", "rus"
        """
        alphabet = self.alphabet

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

    def vigenere_decryption(self, input_str: str, key_word: str) -> str:
        alphabet = self.alphabet
        
        reversed_key_word = []
        key_word = key_word.lower()
        for letter in key_word:
            reversed_key_word.append(alphabet[len(alphabet) - alphabet.index(letter)])
        reversed_key_word = ''.join(reversed_key_word)
        return self.vigenere(input_str, reversed_key_word)



class Vernam(AbstractCipher):
    name = "vernam"
    def __init__(self):
        super().__init__()

    def encrypt(self, input_str: str) -> str:
        keyword = ''.join([chr(random.randint(ord('A'), ord('z'))) for i in range(len(input_str))])
        print("Your generated keyword:", keyword)
        return self.vernam(input_str, keyword)

    def decrypt(self, input_str: str) -> str:
        key_str = str(input("Enter your keystring, please: "))
        return self.vernam_decryption(input_str, key_str)

    def vernam(self, input_str: str, key_str: str) -> str:
        """ Vernam encryption algo
            input_str is string to encrypt
            key_str is randomly generated key THE SAME SIZE AS input_str
        """
        if len(key_str) < len(input_str):
            raise Exception("Keystring is too small")
        result = []
        for i in range(len(input_str)):
            result.append(chr(ord(input_str[i]) ^ ord(key_str[i])))
        result = ''.join(result)
        return result

    def vernam_decryption(self, input_str: str, key_str: str) -> str:
        return self.vernam(input_str, key_str)


class Frequency_analysis:
    name = "frequency_analysis"
    def __init__(self, language: str):
        if language == eng_tag:
            self.alphabet = alphabet_eng
            self.most_commoly_used_letter_index = self.alphabet.index('e')
        elif language == rus_tag:
            self.alphabet = alphabet_rus
            self.most_commoly_used_letter_index = self.alphabet.index('о')

    def decrypt(self, input_str: str) -> str:
        return self.frequency_analysis(input_str)

    def frequency_analysis(self, input_str: str) -> str:
        """ Frequency Caesar decryption algorithm based on most commoly used letter
            input_str = string to decrypt
            language = {"eng", "rus"}
        """
        alphabet = self.alphabet
        most_commoly_used_letter_index = self.most_commoly_used_letter_index

        frequency_rate = [0] * len(alphabet)
        for letter in input_str.lower():
            if letter.isalpha():
                frequency_rate[alphabet.index(letter)] += 1
                
        most_common_letter_index = frequency_rate.index(max(frequency_rate))
        bias = -(most_common_letter_index - most_commoly_used_letter_index)
        
        """caesar(input_str, bias)"""
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


def main():
    mode1 = "encryption"
    mode2 = "decryption"
    parser = argparse.ArgumentParser(description="A normal console arguments parser")
    parser.add_argument("--language", choices=[eng_tag, rus_tag], default=eng_tag, type=str, help="This is supported language(english or russian)")
    parser.add_argument("--mode", choices=[mode1, mode2], default=mode1, type=str, help="This is mode of cryptography(encryption or decryption)")
    parser.add_argument("--type", choices=[Caesar.name, Viginere.name, Vernam.name, Frequency_analysis.name], default=Caesar.name, type=str, help="This is type of encryption(caesar, vigenere, vernam) or decryption(caesar, vigenere, vernam, frequency_analysis)")
    parser.add_argument("--input_file", required=True, type=str, help="This a path to text-file to encrypt/decrypt")
    args = parser.parse_args()

    with open(args.input_file, 'r') as input_file:
        input_str = input_file.read()
    
    cipher: AbstractCipher
    if args.type == Caesar.name:
        cipher = Caesar(args.language)
    elif args.type == Viginere.name:
        cipher = Viginere(args.language)
    elif args.type == Vernam.name:
        cipher = Vernam()
    elif args.type == Frequency_analysis.name:
        cipher = Frequency_analysis(args.language)

    output_str: str
    if args.mode == mode1:
        output_str = cipher.encrypt(input_str)
    elif args.mode == mode2:
        output_str = cipher.decrypt(input_str)

    with open(args.mode + ".py", 'w') as output_file:
        output_file.write(output_str)

    print("All has been written to ", args.mode + ".py")

if __name__ == "__main__":
    main()
