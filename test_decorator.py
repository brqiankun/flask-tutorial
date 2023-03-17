def hi(name = "bairui"):
    print("now you are inside the hi() functon")
    return "hi" + name

print(hi())

greet = hi
print(greet())

del hi
# print(hi())

print(greet())