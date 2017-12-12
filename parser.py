import repository


resource = open('source/words.txt', 'r')

i = 1
word = resource.read(i).strip()
while word:
    print("%s" % word)

    repository.insert(word, len(word))

    i += 1
    word = resource.read(i).strip()
