"""
This package is a way for people who contribute to software to develop an
understanding of the codebase they wish to contribute to in a visual, intuitive
manner.
"""
from .nodes import BaseNode, PackageNode, ModuleNode, ClassNode, FunctionNode,\
                   ImportNode, tree_builder
