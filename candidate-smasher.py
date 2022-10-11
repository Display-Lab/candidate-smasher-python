

import json
import sys
import warnings
import time
import logging
import json
import candidate_smasher

#content = sys.argv[1]
md_source = sys.argv[2]
f=open(sys.argv[1])
content = json.load(f)
#print(type(content))
content =json.dumps(content)
#print(type(content))
#f1=open(sys.argv[2])
#md_source = json.load(f1)
#md_source =json.dumps(md_source)
#print(type(md_source))
#md_source =json.dumps(md_source)
#print(type(md_source))
cs = candidate_smasher.CandidateSmasher(content,md_source)
#cs.smash()
if cs.valid():
    print (cs.smash())

