import vyky
import time

if __name__ == '__main__' :

    start_time = time.time()
    my_ga = vyky.GeneticAlgorithm( generations=100 , population_length=2 , mutation_rate=0.9 , tsp_instance='pr2392.tsp', print_info=True)
    
    result = my_ga.run()
    end_time = time.time()

    #save result in a file
    output = "pr2392-solution.json"
    f = open(output, "w")
    f.write(result)
    f.close()
    
    print("Se guardo la ruta en el archivo {}\n".format(f.name))
    print("Tiempo de ejecucion: {0:.4f} seconds.\n".format(end_time - start_time))
