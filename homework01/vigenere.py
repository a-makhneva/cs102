def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    if keyword == '':
        keyword = "a"
    keyword = keyword.upper()  # the key is case-insensitive

    if len(plaintext) > len(keyword):
        while len(plaintext) > len(keyword):
            keyword = keyword + keyword  # no need to shorten key afterwards

    for i in range(0, len(plaintext)):
        plainletter = plaintext[i: i + 1]
        x = ord(plainletter)
        keyletter = keyword[i:i + 1]
        shift = ord(keyletter) - 65  # 65 is the code for capital A

        if ((x in range(65, 91)) and (shift + x > 90)) or ((x in range(97, 123)) and (shift + x > 122)):
            shift = shift - 26
        # if (uppercase) or (lowercase)

        if x<65 or ((x>91) and (x<97)) or x>123:  # non-alphabetic
            shift=0

        ciphertext = ciphertext + chr(x + shift)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    if keyword == '':
        keyword = "a"
    keyword = keyword.upper()  # the key is case-insensitive

    if len(ciphertext) > len(keyword):
        while len(ciphertext) > len(keyword):
            keyword = keyword + keyword  # no need to shorten key afterwards

    for i in range(0, len(ciphertext)):
        cipherletter = ciphertext[i: i + 1]
        x = ord(cipherletter)
        keyletter = keyword[i:i + 1]
        shift = ord(keyletter) - 65  # 65 is the code for capital A

        if ((x in range(65, 91)) and (x - shift < 65)) or ((x in range(97, 123)) and (x - shift < 97)):
            shift = shift - 26
        # if (uppercase) or (lowercase)

        if x < 65 or ((x > 91) and (x < 97)) or x > 123:  # non-alphabetic
            shift = 0

        plaintext = plaintext + chr(x - shift)

    return plaintext