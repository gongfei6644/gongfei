list01 = ["a", "b", "c"]
list02 = ["A", "B", "C"]

result = []
for r in list01:
    for c in list02:
        result.append(r + c)

print(result)

result = [r + c for r in list01 for c in list02]
print(result)



