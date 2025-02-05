
def letter_to_number(letter: str) -> int:
    return ord(letter.upper()) - ord("A")

def number_to_letter(number: int) -> str:
    return chr(number + 65).upper()