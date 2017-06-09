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
        modnam = modname(module.name)

        with self.dotfile.subgraph(name='cluster_'+modnam) as module:
            self.objname[modnam] = 'cluster_'+modnam
            for cla in classes:
                module.node(modnam + "." + cla, label=cla)
                self.objname[modnam + "." + cla] = modnam + "." + cla

        self.donelist.append(modnam)
        return imports

    def main(self):
        """Main loop"""
        for files in self.filelist:
            if os.path.isfile(files) and ispython(files):
                imports = self.modulegrapher(open(files))
                for imp in imports:
                    self.dotfile.edge(self.objname[modname(files)], imp)
                    if imp not in self.donelist:
                        self.filelist.append(imp+".py")
            elif os.path.isdir(files.split('.')[0]):
                #It's a package!
                targfile = open(files.replace('.', '/', 1))
                targfilename = targfile.name
                imports = self.modulegrapher(targfile)
                for imp in imports:
                    self.dotfile.edge(self.objname[modname(targfilename)], imp)
                    if imp not in self.donelist:
                        self.filelist.append(imp+".py")
            else:
                self.dotfile.node(files)

def ispython(filename):
    """Returns True if file extension is py
    Returns False otherwise.
    """
    return filename.split('.')[1] == 'py'

def modname(filename):
    """Returns module name from py file"""
    return filename.split('.')[0]
