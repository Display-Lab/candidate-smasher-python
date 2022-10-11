
a = [1,2,3]
b = [3,4,5,6]
b2 = 7

p(a.is_a?(Array))
res = Array(a) + Array(b2)
p(res)
p(res.uniq)

f = [[[1,2], 3, [4, 5]], 6]
f2 = f.flatten(1)
p(f)
p(f2)
