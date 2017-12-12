import repository


resource = open('words.txt', 'r')

i = 1
word = resource.read(i).strip()
while word:
    print("%s" % word)
    i += 1
    word = resource.read(i).strip()

    repository.insert(word, len(word))
