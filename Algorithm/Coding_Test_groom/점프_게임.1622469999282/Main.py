# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean

def jump(arr, x, y):  
    if x >= n: return False  
    if y >= n: return False 
    if x == n-1 and y == n-1: return True
    result = record[x][y]  
    if result != -1: return result 
    move = arr[x][y]  
    result = max(result, jump(arr, x+move, y))  
    result = max(result, jump(arr, x, y+move)) 
    record[x][y] = result 
    return result

	
n = int(input())
arr = []
record = [[-1 for k in range(n)] for l in range(n)]  
for j in range(n):
	arr.append(list(map(int, input().split())))
if jump(arr, 0, 0):
    print("YES")
else:
    print("NO")
