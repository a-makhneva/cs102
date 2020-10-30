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
            keyword += keyword  # no need to shorten key afterwards

    for i in range(0, len(plaintext)):
        plainletter = plaintext[i: i + 1]
        x = ord(plainletter)
        keyletter = keyword[i:i + 1]
        shift = ord(keyletter) - ord('A')

        if ((x in range(ord('A'), ord('Z')+1)) and (shift + x > ord('Z'))) or ((x in range(ord('a'), ord('z')+1)) and (shift + x > ord('z'))):
            shift -= 26
        # if (uppercase) or (lowercase)

        if x < ord('A') or ((x > ord('Z')+1) and (x < ord('a'))) or x > ord('z')+1:  # non-alphabetic
            shift = 0

        ciphertext += chr(x + shift)

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
            keyword += keyword  # no need to shorten key afterwards

    for i in range(0, len(ciphertext)):
        cipherletter = ciphertext[i: i + 1]
        x = ord(cipherletter)
        keyletter = keyword[i:i + 1]
        shift = ord(keyletter) - ord('A')

        if ((x in range(ord('A'), ord('Z')+1)) and (x - shift < ord('A'))) or ((x in range(ord('a'), ord('z')+1)) and (x - shift < ord('a'))):
            shift -= 26
        # if (uppercase) or (lowercase)

        if x < ord('A') or ((x > ord('Z')+1) and (x < ord('a'))) or x > ord('z')+1:  # non-alphabetic
            shift = 0

        plaintext += chr(x - shift)

    return plaintext
