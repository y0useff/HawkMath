import re

def word_to_number(text):
    units = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
    }
    teens = {
        "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
        "fourteen": 14, "fifteen": 15, "sixteen": 16,
        "seventeen": 17, "eighteen": 18, "nineteen": 19
    }
    tens = {
        "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90
    }

    text = text.lower().replace("-", " ")
    words = text.split()

    num = current = 0
    for word in words:
        if word in units:
            current += units[word]
        elif word in teens:
            current += teens[word]
        elif word in tens:
            current += tens[word]
        elif word == "hundred":
            current *= 100
        elif word == "thousand":
            current *= 1000
            num += current
            current = 0
        else:
            return None
    return num + current

def transmute(text):
    operations = {
        "add": "+", "plus": "+", "minus": "-", "subtract": "-",
        "multiply": "\\times", "times": "\\times",
        "divide": "\\div", "open parenthesis": "(", "close parenthesis": ")", "power of" : "^{"
    }

    text = text.lower().replace("-", " ")
    text = re.sub(r'(\d+)/(\d+)', r'\\frac{\1}{\2}', text)

    words = text.split()
    result = []
    i = 0

    while i < len(words):
        word = words[i]
        next_word = words[i + 1] if i + 1 < len(words) else ""
        combined = f"{word} {next_word}"

        # Special case: "divide by" for fractions
        if word == "divide" and next_word == "by" and i + 2 < len(words):
            numerator = result.pop() if result else None
            if numerator is not None and isinstance(numerator, str):
                num_value = word_to_number(numerator)
                if num_value is not None:
                    numerator = str(num_value)

            i += 2  # Skip "divide by"
            denominator_words = []
            while i < len(words) and (words[i].isdigit() or word_to_number(words[i]) is not None):
                denominator_words.append(words[i])
                i += 1
            denominator = word_to_number(' '.join(denominator_words)) if denominator_words else None

            if numerator and denominator is not None:
                result.append(f"\\frac{{{numerator}}}{{{denominator}}}")
            continue

        # Handle combined operations like "open parenthesis"
        if combined in operations:
            result.append(operations[combined])
            i += 2
            continue

        # Handle simple one-word operations
        if word in operations:
            result.append(operations[word])
            i += 1
            continue

        # Handle digits
        if word.isdigit():
            result.append(word)
            i += 1
            continue

        # Handle variables or combined numbers and variables like "3x"
        if re.match(r'^[a-zA-Z]+$', word) or re.match(r'^\d+[a-zA-Z]+$', word):
            result.append(word)
            i += 1
            continue

        # Try grouping number words (e.g., "twenty five")
        j = i
        num_words = []
        while j < len(words) and word_to_number(words[j]) is not None:
            num_words.append(words[j])
            j += 1
        if num_words:
            number = word_to_number(' '.join(num_words))
            result.append(str(number))
            i = j
            continue

        # Skip unknown words
        i += 1

    return "\\begin{align}\n" + ' '.join(result) + "\n\\end{align}"

# Example usage
x="five divide by eight minus three divide by eight open parenthesis two times four close parenthesis plus 3x minus k divide by 3"
result = transmute(x)
print(result)
