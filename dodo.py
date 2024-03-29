import os
import sys
from surround import Config

CONFIG = Config(os.path.dirname(__file__))
DOIT_CONFIG = {'verbosity':2}
IMAGE = "%s/%s:%s" % (CONFIG["company"], CONFIG["image"], CONFIG["version"])

def task_build():
    """Build the Docker image for the current project"""
    return {
        'actions': ['docker build --tag=%s .' % IMAGE]
    }

def task_remove():
    """Remove the Docker image for the current project"""
    return {
        'actions': ['docker rmi %s -f' % IMAGE]
    }

def task_dev():
    """Run the main task for the project"""
    return {
        'actions': ["docker run --volume \"%s/\":/app %s" % (CONFIG["volume_path"], IMAGE)]
    }

def task_prod():
    """Run the main task inside a Docker container for use in production """
    return {
        'actions': ["docker run %s" % IMAGE],
        'task_dep': ["build"]
    }

def task_train():
    """Run training mode inside the container"""
    output_path = CONFIG["volume_path"] + "/output"
    data_path = CONFIG["volume_path"] + "/data"

    return {
        'actions': ["docker run --volume \"%s\":/app/output --volume \"%s\":/app/data %s python3 -m surround_tensorboard_example --mode train" % (output_path, data_path, IMAGE)]
    }

def task_batch():
    """Run batch mode inside the container"""
    output_path = CONFIG["volume_path"] + "/output"
    data_path = CONFIG["volume_path"] + "/data"

    return {
        'actions': ["docker run --volume \"%s\":/app/output --volume \"%s\":/app/data %s python3 -m surround_tensorboard_example --mode batch" % (output_path, data_path, IMAGE)]
    }

def task_train_local():
    """Run training mode locally"""
    return {
        'basename': 'trainLocal',
        'actions': ["%s -m surround_tensorboard_example --mode train" % sys.executable]
    }

def task_batch_local():
    """Run batch mode locally"""
    return {
        'basename': 'batchLocal',
        'actions': ["%s -m surround_tensorboard_example --mode batch" % sys.executable]
    }
