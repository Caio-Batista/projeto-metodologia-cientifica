#coding:utf-8
import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader
from weka.core.dataset import Instance
import sys

jvm.start()
loader = Loader(classname="weka.core.converters.ArffLoader")
data_train = loader.load_file("file_train.arff")
data_train.class_is_last()

data_test = loader.load_file("file_test.arff")
data_test.class_is_last()

SPAM = 1.0
HAM = 0.0
l1 = [0,0]
l2 = [0,0]
count_spams = 0
counts_hams = 0

l = sys.argv
tec = l[1]
if(tec == "1"):
	cls = Classifier(classname="weka.classifiers.bayes.NaiveBayes")
elif(tec == "2"):
	cls = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.25"])
else:
	cls = Classifier(classname="weka.classifiers.trees.RandomForest", options=["-I", "10"])

cls.build_classifier(data_train)

for index, inst in enumerate(data_test):
	pred = cls.classify_instance(inst)
    
	if(index <= 29):
		if(pred == SPAM):
			l1[0] = l1[0]+1
		else:
			l1[1] = l1[1]+1

	else:
		if(pred == SPAM):
			l2[0] = l2[0]+1
		else:
			l2[1] = l2[1]+1

precision_spam = (l1[0]/float(l1[0] + l2[0]))
recall_spam = (l1[0]/float(l1[0] + l1[1]))
f_measure_spam = 0
if(precision_spam != 0 or recall_spam != 0):
	f_measure_spam = 2 * precision_spam * recall_spam / float(precision_spam + recall_spam)

precision_ham = (l2[1]/float(l2[1] + l1[1]))
recall_ham = (l2[1]/float(l2[1] + l2[0]))
f_measure_ham = 0
if(precision_ham != 0 or recall_ham != 0):	
	f_measure_ham = 2 * precision_ham * recall_ham / float(precision_ham + recall_ham)

precision_m = (precision_spam + precision_ham)/2.
recall_m = (recall_spam + recall_ham)/2.
f_measure_m = (f_measure_ham + f_measure_spam)/2.

print "matriz de comfusão" 
print "     spam ham"
print "spam  %d   %d" % (l1[0], l1[1])
print "ham   %d   %d" % (l2[0], l2[1])

print "precision = %.2f" % (precision_m*100)
print "recall = %.2f" % (recall_m*100)
print "f-measure = %.2f" % (f_measure_m*100)


jvm.stop()
