#spell_test.py
from autocorrect import spell as auto_test
from yuxinzhu import test as yux_test
from norvig import correction as norvig_test
from hybrid_check import spell as hybrid_test
import random

correct = ""
total_tests = 0
autocorrect_score = 0
yux_score = 0
norvig_score = 0
hybrid_score = 0

#main
print "Reading test data ... "
dict = {}
with open("wikipedia.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line[0] == "$":
            correct = line[1:]
            dict[correct] = []
        else:
            dict[correct].append(line)
        
print "Testing ... "
for correct in random.sample(list(dict), 1500):
    for w in dict[correct]:
        total_tests += 1
        #Test 1: autocorrect.py
        if auto_test(w) == correct:
            autocorrect_score += 1
        #Test 2: yuxinzhu checker
        if yux_test(w) == correct:
            yux_score += 1
        #Test 3: Norvig checker
        if norvig_test(w) == correct:
            norvig_score += 1
        #Test 4: Hybrid checker
        if hybrid_test(w) == correct:
            hybrid_score += 1
        if total_tests % 100 == 0: print total_tests
print "Autocorrect: " + str(autocorrect_score) + "/" + str(total_tests) + " " + str(autocorrect_score*100 / float(total_tests)) + "%"
print "Yuxinzhu: " + str(yux_score) + "/" + str(total_tests) + " " + str(yux_score*100 / float(total_tests)) + "%"
print "Norvig: " + str(norvig_score) + "/" + str(total_tests) + " " + str(norvig_score*100 / float(total_tests)) + "%"
print "Hybrid: " + str(hybrid_score) + "/" + str(total_tests) + " " + str(hybrid_score*100 / float(total_tests)) + "%"