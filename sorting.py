st = 'azzMMaossmub*%@19@*'

print('Before Sorting')
print(st)

st = list(st)
smallLetters = []
smallLetterIndex = []
id = 0

for x in st:
    if x.islower():
        smallLetters.append(x)
        smallLetterIndex.append(id)
    id+=1

smallLetters = sorted(smallLetters)
print(smallLetters)
print(smallLetterIndex)
for i in range(len(smallLetters)):
    st[smallLetterIndex[i]] = smallLetters[i]

st = ''.join([str(elem) for elem in st])

print()
print('After Sorting')
print(st)