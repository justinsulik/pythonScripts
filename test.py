from krippendorffsAlpha import krippAlpha

test1 = 'testData1.csv'
test2 = 'testData2.csv'
test3 = 'testData3.csv'
test4 = 'testData4.csv'

# for test in range(1,5):


#Should be 0.811
print(krippAlpha(test1))

#Should be 1
print(krippAlpha(test2))

#Should be 0.692
print(krippAlpha(test3,var_type='nominal'))

#Should be 0.849
print(krippAlpha(test4))

#Should be 0.743
print(krippAlpha(test4, var_type='nominal'))
