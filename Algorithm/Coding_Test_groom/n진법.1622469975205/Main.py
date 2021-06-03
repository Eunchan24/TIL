# -*- coding: utf-8 -*-
# UTF-8 encoding when using korean
# 입력
import string
n, m = map(int, input().split())

# 대문자 
tmp = string.digits+string.ascii_uppercase

def convert(n, m):
	q, r = divmod(n, m)
	if q==0:
		return tmp[r]
	else:
		return convert(q, m) + tmp[r]

print(convert(n, m))