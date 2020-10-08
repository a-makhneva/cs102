def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    shift = shift % 26  # 26 = number of letters in the english alphabet

    for i in range(0, len(plaintext)):
        letter = plaintext[i: i + 1]
        x = ord(letter)

        if (x in range(65, 90 - shift + 1)) or (x in range(97, 122 - shift + 1)):  # main body
            x = x + shift
        elif (x in range(90 - shift + 1, 91)) or (x in range(122 - shift + 1, 123)):  # tail (xyz)
            x = x - 26 + shift
        else:  # other cases
            x = x

        ciphertext = ciphertext + chr(x)
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    shift = shift % 26  # 26 = number of letters in the eng alphabet

    for i in range(0, len(ciphertext)):
        letter = ciphertext[i: i + 1]
        x = ord(letter)

        if (x in range(65 + shift, 91)) or (x in range(97 + shift, 123)):  # main body
            x = x - shift
        elif (x in range(65, 65 + shift)) or (x in range(97, 97 + shift)):  # head (abc)
            x = x + 26 - shift
        else:  # other cases
            x = x

        plaintext = plaintext + chr(x)
    return plaintext


def caesar_breaker(ciphertext: str, dictionary: set()) -> int:
    """
    >>> d = {"python", "java", "ruby"}
    >>> caesar_breaker("python", d)
    0
    >>> caesar_breaker("sbwkrq", d)
    3
    """
    best_shift = 0

    for i in range(27):
        if decrypt_caesar(ciphertext, i) in dictionary:
            best_shift = i
            break
        else:
            best_shift = 404  # not found

    return best_shift
