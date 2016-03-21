import weka.core.jvm as jvm
from weka.classifiers import Classifier
from weka.core.converters import Loader
from weka.core.dataset import Instance

jvm.start()
loader = Loader(classname="weka.core.converters.ArffLoader")
data_train = loader.load_file("file_train.arff")
data_train.class_is_last()

data_test = loader.load_file("file_test.arff")
data_test.class_is_last()


cls = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.3"])

cls.build_classifier(data_train)

for index, inst in enumerate(data_test):
    pred = cls.classify_instance(inst)
    dist = cls.distribution_for_instance(inst)
    #formatar aqui a saída...
    print(str(index+1) + ":=" + str(pred))

jvm.stop()
