def count_words(sentence):
    count = 0
    in_word = False

    for char in sentence:
        if char.isalnum():
            if not in_word:
                count += 1
                in_word = True
        else:
            in_word = False  # End of the word

    return count


sentence = "Hello and good morning"
word_count = count_words(sentence)
print("Number of words:", word_count)
