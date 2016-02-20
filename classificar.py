# coding: utf-8
import sys

result = []

for arg in sys.argv:
    result.append(arg)

print "Os argumentos estão sendo passados corretamente:  \n%s" % (str(result))