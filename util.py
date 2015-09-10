##### Filename: util.py
##### Author: Charles Liu
##### Date: 9/8/2015
##### Email: cliu02@g.harvard.edu

import copy
from collections import deque

## Problem 1

def matrix_multiply(x, y):
    #return matrix dimensions are len(x) x len(y[0])
    ret = [[]]*len(x)
    #loop through rows of x/columns of y
    for row in range(0, len(x)):
        #loop through cols of y
        for col in range(0, len(y[0])):
            sum = 0
            #sumproduct of row and col
            for index in range(0, len(x[row])):
                sum += x[row][index]*y[index][col]
            ret[row] = ret[row] + [sum]
    return ret
        

## Problem 2, 3

class MyQueue:
    def __init__(self):
        self._deq = deque()
    def push(self, val):
        self._deq.append(val)
    def pop(self):
        if self._deq.count == 0:
            return None
        return self._deq.popleft()
    def __eq__(self, other):
        return self._deq == other._deq if isinstance(other, MyQueue) else False
    def __ne__(self, other):
        return ((self == other) == False)
    def __str__(self):
        return str(self._deq).replace('deque', 'myqueue', 1)

class MyStack:
    def __init__(self):
        self._deq = deque()
    def push(self, val):
        self._deq.append(val)
    def pop(self):
        if self._deq.count == 0:
            return None
        return self._deq.pop()
    def __eq__(self, other):
        return self._deq == other._deq if isinstance(other, MyStack) else False
    def __ne__(self, other):
        return ((self == other) == False)
    def __str__(self):
        return str(self._deq).replace('deque', 'mystack', 1)

## Problem 4

def add_position_iter(lst, number_from=0):
    ret = copy.copy(lst)
    count = 0
    for i in range(0, len(ret)):
        ret[i] += number_from + count
        count += 1
    return ret
        

def add_position_recur(lst, number_from=0):
    if len(lst) == 0:
        return []
    removed_el = copy.copy(lst)
    del removed_el[0]
    return [lst[0] + number_from] + add_position_recur(removed_el, number_from + 1) 

def add_position_map(lst, number_from=0):
    return map(lambda (i,x): i + x + number_from, enumerate(lst))

## Problem 5

def remove_course(roster, student, course):
    roster[student] = roster[student] - set([course])
    return roster

## Problem 6

def copy_remove_course(roster, student, course):
    roster_new = copy.copy(roster)
    return remove_course(roster_new, student, course)

