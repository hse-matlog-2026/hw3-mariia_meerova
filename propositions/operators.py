# This file is part of the materials accompanying the book
# "Mathematical Logic through Python" by Gonczarowski and Nisan,
# Cambridge University Press. Book site: www.LogicThruPython.org
# (c) Yannai A. Gonczarowski and Noam Nisan, 2017-2022
# File name: propositions/operators.py

"""Syntactic conversion of propositional formulas to use only specific sets of
operators."""

from propositions.syntax import *
from propositions.semantics import *

def to_not_and_or(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'``, ``'&'``, and ``'|'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'``, ``'&'``, and
        ``'|'``.
    """
    # Task 3.5
    if is_variable(formula.root):
        return formula
    if is_constant(formula.root):
        p = Formula('p')
        if formula.root == 'T':
            return Formula('|', p, Formula('~', p))
        else:
            return Formula('&', p, Formula('~', p))
    if is_unary(formula.root):
        return Formula('~', to_not_and_or(formula.first))
    left = to_not_and_or(formula.first)
    right = to_not_and_or(formula.second)
    if formula.root == '&':
        return Formula('&', left, right)
    if formula.root == '|':
        return Formula('|', left, right)
    if formula.root == '->':
        return Formula('|', Formula('~', left), right)
    if formula.root == '+':
        part1 = Formula('&', left, Formula('~', right))
        part2 = Formula('&', Formula('~', left), right)
        return Formula('|', part1, part2)
    if formula.root == '<->':
        part1 = Formula('&', left, right)
        part2 = Formula('&', Formula('~', left), Formula('~', right))
        return Formula('|', part1, part2)
    if formula.root == '-&':
        return Formula('~', Formula('&', left, right))
    if formula.root == '-|':
        return Formula('~', Formula('|', left, right))

def to_not_and(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'~'`` and ``'&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'~'`` and ``'&'``.
    """
    # Task 3.6a
    f = to_not_and_or(formula)

    if is_variable(f.root):
        return f
    if is_unary(f.root):
        return Formula('~', to_not_and(f.first))
    if f.root == '&':
        return Formula('&', to_not_and(f.first), to_not_and(f.second))
    if f.root == '|':
        left = to_not_and(f.first)
        right = to_not_and(f.second)
        return Formula('~', Formula('&', Formula('~', left), Formula('~', right)))
    return f

def to_nand(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'-&'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'-&'``.
    """
    # Task 3.6b
    f = to_not_and(formula)
    
    if is_variable(f.root):
        return f
    if is_unary(f.root):
        inner = to_nand(f.first)
        return Formula('-&', inner, inner)
    if f.root == '&':
        left = to_nand(f.first)
        right = to_nand(f.second)
        nand_ab = Formula('-&', left, right)
        return Formula('-&', nand_ab, nand_ab)
    return f

def to_implies_not(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'~'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'~'``.
    """
    # Task 3.6c
    f = to_not_and_or(formula)

    if is_variable(f.root):
        return f
    if is_unary(f.root):
        return Formula('~', to_implies_not(f.first))
    if f.root == '&':
        left = to_implies_not(f.first)
        right = to_implies_not(f.second)
        return Formula('~', Formula('->', left, Formula('~', right)))
    if f.root == '|':
        left = to_implies_not(f.first)
        right = to_implies_not(f.second)
        return Formula('->', Formula('~', left), right)
    return f

def to_implies_false(formula: Formula) -> Formula:
    """Syntactically converts the given formula to an equivalent formula that
    contains no constants or operators beyond ``'->'`` and ``'F'``.

    Parameters:
        formula: formula to convert.

    Returns:
        A formula that has the same truth table as the given formula, but
        contains no constants or operators beyond ``'->'`` and ``'F'``.
    """
    # Task 3.6d
    f = to_implies_not(formula)

    if is_variable(f.root):
        return f
    if f.root == 'F':
        return f
    if f.root == '->':
        left = to_implies_false(f.first)
        right = to_implies_false(f.second)
        return Formula('->', left, right)
    if f.root == '~':
        inner = to_implies_false(f.first)
        return Formula('->', inner, Formula('F')) 
    return f
