""" This module contains methods related to graphing the structure of python programs. """
import os
import graphviz
from pysourcegraph import import_lister, class_lister

class Grapher:
    """This class maintains the structure of the graph that will be returned"""
    def __init__(self, title=None):
        """ Creates a Grapher object

        Args:
            title (str): The title of the project to be graphed.
        """
        self.title = title
        self.filelist = os.listdir()
        self.donelist = []
        self.dotfile = graphviz.Digraph(name=title)
        self.objname = dict()

    def modulegrapher(self, module):
        """ Graphs a module and all classes inside it returns a list of all modules linked

        Args:
            module (file): File pointing to the module to be graphed
        """
        imports = import_lister(module)
        classes = class_lister(module)
        modname = module.name.split('.')[0]

        with self.dotfile.subgraph(name='cluster_'+modname) as module:
            self.objname[modname] = 'cluster_'+modname
            for c in classes:
                module.node(modname + "." + c, label='c')
                self.objname[modname + "." + c] = modname + "." + c
        
        return imports
    
    def main(self):
        