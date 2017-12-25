""" This class contains objects used to maintain the structure of the python source code."""
class BaseNode(object):
    """ This object is the base for all of the other, more sepecific node types
    Attributes:
        children: A list of all children of this node
        name: A string containing the fully qualified name of the node
        docstring: A string containing the docstring associated with this node. Defaults to None
    """
    def __init__(self, name, docstring=None):
        """Create new BaseNode object"""
        self._name = name
        self._docstring = docstring
        self._children = list()

    def add_child(self, childnode):
        """Add a child node to this node
        Args:
            childnode(BaseNode): Node to be added under this node
        """
        self._children.append(childnode)

    def remove_child(self, targetnode):
        """Remove a child node from this node
        This is an O(n)=n function
        Args:
            targetnode(BaseNode): Node to be removed from this node
        """
        try:
            self._children.remove(targetnode)
        except ValueError:
            print("Failed to remove node" + targetnode)

    def get_children(self):
        """Return the list of children"""
        return self._children

    def is_childless(self):
        """Returns True if the node has no children"""
        return not self._children

    def __eq__(self, other):
        """Define custom Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        """Define custom NotEquals behavior"""
        if isinstance(other, self.__class__):
            return not self == other
        else:
            return NotImplemented

    def __repr__(self):
        """Define python representation of object"""
        return str(self.__class__) + str(self.__dict__)

    @DeprecationWarning
    def getlocalattr(self, attrname):
        """Return a function that returns the value of attrname in this class

        >>>self.x = 100
        >>>self.getlocalattr("x")()
        >>>100

        Args:
            attrname(str): String of the name of the variable
        """
        return lambda: getattr(self, attrname)

    @DeprecationWarning
    def setlocalattr(self, attrname):
        """Return a function that sets the value of attrname in this class

        >>>f = self.setlocalattr("x")
        >>>f(100)
        >>>self.x
        >>>100

        Args:
            attrname(str): String of the name of the variable
        """
        return lambda value: setattr(self, attrname, value)

    @DeprecationWarning
    def dellocalattr(self, attrname):
        """Return a function that deletes attrname from this class

        Args:
            attrname(str): String of the name of the variable
        """
        return lambda: delattr(self, attrname)

    @property
    def name(self):
        """The fully qualified name of the Node"""
        return self._name

    @property
    def docstring(self):
        """The DocString found documenting this Node"""
        return self._docstring

class PackageNode(BaseNode):
    """This Node represents a package, with modules and subpackages within

    Attributes:
        filepath: A string containing the relative filepath of the Package.
            These should be directories."""
    def __init__(self, name, docstring=None, filepath=None):
        self._filepath = filepath
        super().__init__(name=name, docstring=docstring)

    @property
    def filepath(self):
        """This is the filepath of the directory of the package, relative to startpoint"""
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

class ModuleNode(BaseNode):
    """This Node represents a Module, with classes, functions and imports within"""
    def __init__(self, name, docstring=None, filepath=None):
        super().__init__(name=name, docstring=docstring)
        self._filepath = filepath
    @property
    def filepath(self):
        """String containing the relative filepath of the module. Should point to .py file"""
        return self._filepath

    @filepath.setter
    def filepath(self, value):
        self._filepath = value

class ClassNode(BaseNode):
    """This node represents a class, with imports, functions, and attributes within"""
    def __init__(self, name, docstring=None):
        super().__init__(name=name, docstring=docstring)

class FunctionNode(BaseNode):
    """This node represents a function"""
    def __init__(self, name, docstring=None, arguments=None):
        super().__init__(name=name, docstring=docstring)
        self._arguments = arguments

    @property
    def arguments(self):
        """This is intended to represent a list of all arguments given to the function."""
        return NotImplemented

class ImportNode(BaseNode):
    """This node represents an import"""
    def __init__(self, name, docstring=None, alias=None):
        super().__init__(name=name, docstring=docstring)
        if alias is None:
            self._alias = name
        else:
            self._alias = alias

    @property
    def name(self):
        """The fully qualified name of the target imported package"""
        return self._name
    @property
    def alias(self):
        """This is the value that the imported package was imported as"""
        return self._alias

    @alias.setter
    def alias(self, value):
        self._alias = value

    @alias.deleter
    def alias(self):
        self._alias = self._name

def tree_builder(initial_directory):
    """
    This function returns a tree structure built from the directory specified.
    All packages, modules, classes, functions, and imports should be in this
    tree
    Args:
        initial_directory(string): path to start directory
    Returns:
        tree(BaseNode): Tree structure
    """
    # List components of the directory.
    # We want the root to have a setup.py, or an __init__.py
    import os
    currdircontents = os.listdir(initial_directory)
    tree = BaseNode(name=os.path.basename(initial_directory))
    if not "setup.py" in currdircontents and \
       not "__init__.py" in currdircontents:
        raise EnvironmentError("We don't have a package in the directory listed")
    tree = map_folder(initial_directory)
    return tree

def map_folder(file_path):
    """
    This function maps a directory, and all .py files in the directory.
    All directories within will be recursively mapped.
    Args:
        file_path(str): Path to map
    Returns:
        node(PackageNode): PackageNode with subnodes mapped
    """
    import os
    dircontents = os.listdir(file_path)
    # Only map the directory if it has at least one .py file in it.
    mappable = False
    basepath = file_path + "\\"
    dirs = list()
    pyfiles = list()
    for listing in dircontents:
        if os.path.splitext(listing)[-1] == ".py":
            mappable = True
            pyfiles.append(listing)
        elif os.path.isdir(basepath + listing):
            mappable = True
            dirs.append(listing)
    if not mappable:
        return None
    tree = PackageNode(os.path.basename(file_path), filepath=file_path)
    for listing in dirs:
        if listing is not None:
            tree.add_child(map_folder(basepath + listing))
    for listing in pyfiles:
        tree.add_child(map_module(basepath + listing))
    if tree.is_childless():
        return None
    else:
        return tree

def map_module(file_path):
    """
    This function parses a module to a single tree and returns it
    Args:
        file_path(str): File path to parse
    """
    import ast
    import os
    import logging
    logging.log(logging.DEBUG, str("Mapping module at location: " + file_path))
    try:
        syntree = ast.parse(open(file_path).read())
    except SyntaxError as syn:
        logging.log(logging.WARNING, str("Syntax error at: " + file_path))
        return None
    realtree = ModuleNode(os.path.basename(file_path), ast.get_docstring(syntree))
    # Proceed with naive implementation, assume that all classes, imports,
    # and functions are at one level here.
    # This allows the usage of the walk method.
    for node in ast.walk(syntree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                realtree.add_child(ImportNode(name=alias.name, alias=alias.asname))
        if isinstance(node, ast.ClassDef):
            realtree.add_child(ClassNode(node.name, ast.get_docstring(node)))
        if isinstance(node, ast.FunctionDef):
            arguments = list()
            for arg in node.args.args: # node.args is an argument node
                # node.args.args is a list of arguments
                arguments.append(arg.arg)
            arguments = "".join(str(arg) for arg in arguments)
            realtree.add_child(FunctionNode(node.name,
                                            ast.get_docstring(node),
                                            arguments=arguments))
    return realtree
