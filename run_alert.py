import sys

import json

alert_name = sys.argv[1]

print(alert_name)

alert_type = sys.argv[2]

print(alert_type)

params = json.loads(sys.argv[3])

print(params)

params['alert_name']= alert_name

def loadmodel(module,classname):

    try:

        module = __import__(module, fromlist=[classname])

    except ImportError as e:

        raise ValueError("Importing Classes Issues {}".format(classname))

    try:

        class_info= getattr(module, classname)

    except AttributeError:

        raise ValueError("Module {} has no class {}".format(module, classname))

    return class_info

# run the actual alerts in the scripts folder in this repo

class_info = loadmodel('scripts.{}'.format(alert_type), alert_type)

class_info(params).run()