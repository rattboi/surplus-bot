#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import sys
import os
import imp

import warnings
warnings.filterwarnings("ignore")


def cli():
    argvs = sys.argv[1:]
    action = argvs[0]

    plugins = [x
               for x in glob.glob('surplus/plugins/*.py')
               if '__init__' not in x]
    for plugin in plugins:
        plugin_ext = os.path.splitext(plugin)[1]
        plugin_filename = os.path.basename(plugin).split(plugin_ext)[0]
        plug = imp.load_source('plugins.{}'.format(plugin_filename), plugin)
        if hasattr(plug, action):
            method = getattr(plug, action)
            if callable(method):
                method()

if __name__ == '__main__':
    cli()
