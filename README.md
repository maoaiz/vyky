
### Permutation Encoding

#### Crossover

Single point crossover - one crossover point is selected, till this point the permutation is copied from the first parent, then the second parent is scanned and if the number is not yet in the offspring it is added
Note: there are more ways how to produce the rest after crossover point
    
    (1 2 3 4 5 6 7 8 9) + (4 5 3 6 8 9 7 2 1) = (1 2 3 4 5 6 8 9 7)

#### Mutation

Order changing - two numbers are selected and exchanged
    
    (1 2 3 4 5 6 8 9 7) => (1 8 3 4 5 6 2 9 7)

