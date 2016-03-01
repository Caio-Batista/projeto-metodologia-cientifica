# coding: utf-8
import sys, os, random

result = []

for arg in sys.argv[1:]:
    result.append(arg)

if len(result) > 4 or len(result) < 3:
    print "Os argumentos não estão sendo passados corretamente:  \n%s" % (str(result))
else:
    if len(result) == 4 and result[0] == "-v":
        verbose = True
        technique, training, test = result[1:]
    elif len(result) == 3:
        verbose = False
        technique, training, test = result[0:]

    spams = os.listdir(test+"/spam/")
    hams = os.listdir(test+"/ham/")

    all_emails = []
    
    fn = 0
    fp = 0
    tn = 0
    tp = 0
    
    for i in range(len(spams)):
        email_spam = spams[i]
        classifier = random.randint(0,1)
        if classifier == 1:
            tp += 1
            if verbose:
                print "%s: spam" %(spams[i])
        else:
            fn += 1
            if verbose:
                print "%s: ham" %(spams[i])

    for i in range(len(hams)):
        email_ham = hams[i]
        classifier = random.randint(0,1)
        if classifier == 0:
            fp += 1
            if verbose:
                print "%s: ham" %(hams[i])
        else:
            tn += 1
            if verbose:
                print "%s: spam" %(hams[i])

    precision = tp / float(tp + fp)
    recall = tp / float(tp + fn)
    f_measure = 2 * precision * recall / float(precision + recall)
    
    print ""
    print "precision: %02d" %(int(precision * 100))
    print "recall: %02d" %(int(recall * 100))
    print "f-measure: %02d" %(int(f_measure * 100))
    
