import pandas as pd
import numpy as np
import itertools
from collections import Counter

def number_pairable_values(number_observations):
    """How many values in the column could be paired?
    If only 1 value, there isn't anything to pair it with
    """
    return(number_observations if number_observations>1 else 0)

def permutation_pairs(column):
    #Pair-wise permutations from unit values
    column = column.dropna()
    permutations = [x for x in itertools.permutations(column, 2)]
    return(permutations)

def value_matrix(dataframe):
    #Set up a blank dataframe all unit values as both column and row names
    values = dataframe.stack().unique()
    value_matrix = pd.DataFrame(index=values,columns=values)
    return(value_matrix)

def coincidence_matrix(dataframe):
    """
    See https://en.wikipedia.org/wiki/Krippendorff%27s_alpha for a description of what a coincidence matrix is
    """

    #Set up dataframe with all values in data
    coincidence_matrix = value_matrix(dataframe)

    #Fill with zeros
    coincidence_matrix[:] = 0

    #All pair permutations
    pairs = [permutation_pairs(dataframe[x]) for x in dataframe]

    #Number of pairable values
    n_pairable = list(dataframe.count(axis=0).map(number_pairable_values))

    #Fill matrix
    for i, x in enumerate(pairs):
        pair_counts = Counter(x)
        for pair in pair_counts:
            coincidence_matrix[pair[0]][pair[1]] += pair_counts[pair]/(n_pairable[i]-1)
    return(coincidence_matrix)

def difference_matrix(dataframe,var_type):
    difference_matrix = value_matrix(dataframe)
    pairs = list(itertools.product(difference_matrix.columns, repeat=2))
    for pair in pairs:
        difference_matrix[pair[0]][pair[1]] = difference_metric(pair,var_type)
    return(np.matrix(difference_matrix))

def difference_metric(pair,var_type):
    if var_type == 'interval':
        diff = (pair[0]-pair[1])**2
    elif var_type == 'nominal':
        diff = 0 if pair[0]==pair[1] else 1
    else:
        raise ValueError("var_type must be in ['interval', 'nominal']. Feel free to implement other difference metrics as descripted in the links below.")
    return(diff)



def krippAlpha(data_file, var_type='interval'):
    """
    Calculates krippendorff's alpha coefficient, a statistical measure of rater agreement
    See https://en.wikipedia.org/wiki/Krippendorff%27s_alpha for an introduction and
    http://repository.upenn.edu/cgi/viewcontent.cgi?article=1043&context=asc_papers for more details

    args: datafile - a csv file with raters/coders as rows and items/units as columns. See test.py for examples
    """
    df = pd.read_csv(data_file, header=0, index_col=0)

    #Coincidence matrix
    cm = coincidence_matrix(df)
    N = sum(cm.sum())

    #Observed difference
    diffs1 = np.triu(cm, k=1)
    diffs2 = np.triu(difference_matrix(df, var_type), k=1)
    difference_observed = sum([x*diffs2.flatten()[i]for i,x in enumerate(diffs1.flatten())])

    #Expected difference
    variables = itertools.combinations(cm.columns,2)
    sums = itertools.combinations(cm.sum(), 2)
    difference_expected = 1/(N-1)*sum([difference_metric(x,var_type)*y[0]*y[1] for x,y in zip(variables,sums)])
    #print(difference_expected)

    alpha = 1-difference_observed/difference_expected
    return(alpha)
