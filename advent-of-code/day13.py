#!/usr/bin/env python3

# Advent of Code 2022 [https://adventofcode.com/2022/]
# Day 13: Distress Signal
# hans elliott
import copy

def int_vs_int(int1, int2):
    if int1 < int2:
        return True
    elif int1 > int2:
        return False
    else:
        return "Same"

def list_vs_int(item1, item2):
    if isinstance(item1, int):
        item1 = [item1]
        assert type(item2) == list 
    else:
        item2 = [item2]
        assert type(item1) == list
    
    return list_vs_list(item1, item2)


def list_vs_list(list1:list, list2:list):
    if len(list1) < len(list2):
        list1 += ['*'] * (len(list2) - len(list1))
    if len(list1) > len(list2):
        list2 += ['*'] * (len(list1) - len(list2))

    for i, (l1, l2) in enumerate(zip(list1, list2)):
        if l1=='*':
            # list1 = [e for e in list1 if e != '*']
            # list2 = [e for e in list2 if e != '*']
            return True
        if l2=='*':
            # list1 = [e for e in list1 if e != '*']
            # list2 = [e for e in list2 if e != '*']
            return False

        if isinstance(l1, int) and isinstance(l2, int):
            c = int_vs_int(l1, l2)
            if c == "Same":
                continue
            else:
                return c
        
        if isinstance(l1, list) and isinstance(l2, list):
            c = list_vs_list(l1, l2)
            if c == "Same":
                continue
            else:
                return c
        
        if (isinstance(l1, list) & isinstance(l2, int)) | (isinstance(l1, int) & isinstance(l2, list)):
            c = list_vs_int(l1, l2)
            if c == "Same":
                continue
            else:
                return c
    return "Same"

    



if __name__=="__main__":

    input_pairs = []
    with open("advent-of-code/inputs/day13.txt") as f:
        pair = []
        for line in f:
            if line.strip() == '':
                input_pairs.append(pair)
                pair = []
            else:
                pair.append( eval(line.strip()) )
        else:
            input_pairs.append(pair)


    # Part 1: Find indices of pairs which are in the correct order and get their sum
    correct = []
    for i,pair in enumerate(input_pairs):
        c = list_vs_list(pair[0], pair[1])
        if c:
            correct.append(i+1)
    print("Part 1:", sum(correct))



    # Part 2: Sort all items in the input and get the product of the final
    #         indices of the divider packets

    flat_input = [ [[2]], [[6]] ] ##add additional divider packets
    flat_input += [pair[0] for pair in input_pairs] + [pair[1] for pair in input_pairs]
    
    # bubble sort
    n = len(flat_input)
    for i in range(n):
        for j in range(n - i - 1):
            p0 = copy.deepcopy(flat_input[j])
            p1 = copy.deepcopy(flat_input[j+1])

            c = list_vs_list(p0, p1)
            if c == "Same": print("uh oh")
            if c: 
                continue
            else:
                flat_input[j], flat_input[j+1] = flat_input[j+1], flat_input[j]


    div1 = flat_input.index([[2]]) +1
    div2 = flat_input.index([[6]]) +1
    print("Part 2:", div1*div2)
