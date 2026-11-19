"""Native Word math building blocks; requires python-docx.

Append equation(...) to paragraph._p. All arguments are OMML element lists;
math_text creates one-element lists and constructors compose them.
Example: paragraph._p.append(equation(math_text('k = ') +
    fraction(math_text('1'), subscript(math_text('C'), math_text('t')))))
This is an OMML constructor, not a LaTeX parser. Define the scientific equation
separately, then render the resulting document and verify its notation.
"""

from copy import deepcopy
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def math_text(value):
    run = OxmlElement("m:r")
    text = OxmlElement("m:t")
    text.set(qn("xml:space"), "preserve")
    text.text = str(value)
    run.append(text)
    return [run]


def _container(tag, children):
    node = OxmlElement(tag)
    for child in children:
        node.append(deepcopy(child))
    return node


def fraction(numerator, denominator):
    return [_container("m:f", [
        _container("m:num", numerator), _container("m:den", denominator)])]


def subscript(base, script):
    return [_container("m:sSub", [
        _container("m:e", base), _container("m:sub", script)])]


def superscript(base, script):
    return [_container("m:sSup", [
        _container("m:e", base), _container("m:sup", script)])]


def square_root(expression):
    node = OxmlElement("m:rad")
    props = OxmlElement("m:radPr")
    hide = OxmlElement("m:degHide")
    hide.set(qn("m:val"), "1")
    props.append(hide)
    node.extend([props, OxmlElement("m:deg"), _container("m:e", expression)])
    return [node]


def equation(expression, display=True):
    math = _container("m:oMath", expression)
    return _container("m:oMathPara", [math]) if display else math
