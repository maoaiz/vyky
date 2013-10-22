import vyky

if __name__ == '__main__' :
    import pprint   
    pp = pprint.PrettyPrinter(indent=4)

    my_ga = vyky.GeneticAlgorithm( generations=2 , population_length=4 , mutation_rate=1 , tsp_instance='ulysses16.tsp' )
    
    result = my_ga.run()

    pp.pprint( result )
