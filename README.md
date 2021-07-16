Installation

    Python 3.4+ if using a Python wrapper of VnCoreNLP. To install this wrapper, users have to run the following command:

    $ pip3 install vncorenlp

    A special thanks goes to Khoa Duong (@dnanhkhoa) for creating this wrapper!

    Java 1.8+

    File VnCoreNLP-1.1.1.jar (27MB) and folder models (115MB) are placed in the same working folder.

Usage for Python users

Assume that the Python wrapper of VnCoreNLP is already installed via: $ pip3 install vncorenlp
Use as a service

    Run the following command:

    # To perform word segmentation, POS tagging, NER and then dependency parsing
    $ vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p 9000 -a "wseg,pos,ner,parse"
    
    # To perform word segmentation, POS tagging and then NER
    # $ vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p 9000 -a "wseg,pos,ner"
    # To perform word segmentation and then POS tagging
    # $ vncorenlp -Xmx2g <FULL-PATH-to-VnCoreNLP-jar-file> -p 9000 -a "wseg,pos"
    # To perform word segmentation only
    # $ vncorenlp -Xmx500m <FULL-PATH-to-VnCoreNLP-jar-file> -p 9000 -a "wseg"

The service is now available at http://127.0.0.1:9000.

    Use the service in your python code:

Use without the service

from vncorenlp import VnCoreNLP

# To perform word segmentation, POS tagging, NER and then dependency parsing
annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g') 

# To perform word segmentation, POS tagging and then NER
# annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg,pos,ner", max_heap_size='-Xmx2g') 
# To perform word segmentation and then POS tagging
# annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg,pos", max_heap_size='-Xmx2g') 
# To perform word segmentation only
# annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg", max_heap_size='-Xmx500m') 
    
