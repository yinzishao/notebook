#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
判断b是不是a的子结构
def has_sub_tree(a, b):
    if (a或b空)
        return False
    if b.val == a.val:
        result = does_tree1_have_tree2(a, b)
    if !result:
        result = has_sub_tree(a.left_node, b)
    if !result:
        result = has_sub_tree(a.left_node, b)
    return result

def does_tree1_have_tree2(a, b):
    if not b:
        return True
    if not a:
        return False
    if (a.val != b.val):
        return False
    else:
        return does_tree1_have_tree2(a.left, b.left) and does_tree1_have_tree2(a.right, b.right)

"""


