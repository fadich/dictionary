import repository


resource = open('source/one-thousand-words.txt', 'r')

i = 1
word = resource.readline().strip()
while word:
    print("%s" % word)

    repository.insert(word)

    i += 1
    word = resource.readline().strip()

resource.close()
