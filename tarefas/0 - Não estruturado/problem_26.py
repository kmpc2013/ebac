A = [4,5,2,7,8]
limit = 2
B = []
for i in range(len(A)):
    if i == 0:
        continue
    if A[i-1] > limit:
        B.append(i)

print(B)