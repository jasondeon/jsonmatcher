#spell_test.py
from autocorrect import spell as auto_test
from yuxinzhu import test as yux_test
from spell import correction as norvig_test

correct = ""
total_tests = 0
autocorrect_score = 0
yux_score = 0
norvig_score = 0

#main
with open("wikipedia.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line[0] == "$":
            correct = line[1:]
        else:
            total_tests += 1
            #Test 1: autocorrect.py
            if auto_test(line) == correct:
                autocorrect_score += 1
            #Test 2: yuxinzhu checker
            if yux_test(line) == correct:
                yux_score += 1
            #Test 3: Norvig checker
            if norvig_test(line) == correct:
                norvig_score += 1
            if total_tests % 100 == 0: print total_tests
print "Autocorrect: " + str(autocorrect_score / float(total_tests))
print "Yuxinzhu: " + str(yux_score / float(total_tests))
print "Norvig: " + str(norvig_score / float(total_tests))
"""
Results (% correct):
Autocorrect: 0.648472505092
Yuxinzhu: 0.193482688391
Norvig: 0.566191446029
"""
