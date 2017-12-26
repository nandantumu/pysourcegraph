"""
This module contains the parsing functions used to create node trees from
source code
"""
from .nodes import BaseNode, PackageNode, ModuleNode, ClassNode, FunctionNode,\
                   ImportNode

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
    except SyntaxError:
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
