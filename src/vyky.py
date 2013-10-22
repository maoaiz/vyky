#
# Owner
#   Ramon M. "Vyscond"
#
# email
#   vyscond@gmail.com
#
# github
#   vyscond
#
# twitter
#   @vyscond
#
#
# License 
#   This software is licensed under GNU General Public License, version 3 (GPL-3.0)


from math      import sqrt , pow
from traceback import print_exc , format_exc
from random    import randint , shuffle , sample
from copy      import deepcopy

import json

class TSPInstance :

    def __init__( self , tsp_file  ):
        
        tsp = ''.join( open( tsp_file , 'r' ) ).split('\n') 
        
        entries = {}
        
        for attr in tsp[:6] :
            name , value = attr.split(': ')
            entries[name] = value
            
        tmp = []
        for attr in tsp[8:-3]:
            name , x , y = attr.strip().split(' ')
            tmp.append( City( name , x , y ) )
            
        entries[tsp[6]] = list( tmp )
        entries['DIMENSION'] = int( entries['DIMENSION'] )
        self.__dict__.update( entries )
        
    def __str__( self ):
        
        return json.dumps( self , default=lambda o: o.__dict__ )

class GeneticAlgorithm :
    
    def __init__( self , generations , population_length , mutation_rate , tsp_instance ):
        
        self.generations = generations
        
        self.population_length = population_length
        
        self.population = []
        
        self.tsp_instance = tsp_instance
        
        self.best_tour = []
        
        self.mutation_rate = mutation_rate
        
        self.tour_per_generations = []
        
    def run( self ):
        
        try :
            
            self.tsp_instance = TSPInstance( self.tsp_instance )
            print self.tsp_instance
            
            # ---------------------------------------------------
            
            citys = list( self.tsp_instance.NODE_COORD_SECTION )
            
            for i in xrange( self.population_length ):
                
                shuffle( citys )
                
                self.population.append( Tour( list( citys ) , self.tsp_instance.DIMENSION , self.mutation_rate ) )
                
            # ---------------------------------------------------
            
            for i in xrange( self.generations ):
                
                # --- fitness
                
                self.population = sorted( self.population , key = lambda tour : tour.calc_cost() )
                
                self.best_tour.append( deepcopy( self.population[0]  ))
                
                # --- crossover
                tmp_new_population = []
                for i in xrange( self.population_length ) :
                    
                    try :
                        
                        tmp_new_population.append( self.population[ i ] + self.population[ i + 1 ] )
                        
                    except :
                        
                        tmp_new_population.append( self.population[ 0 ] + self.population[ i ]  )
                     
                self.tour_per_generations.append( list( self.population ) )
                self.population = tmp_new_population
                
            for tour in self.best_tour :
                
                print str(tour) , tour.cost
                
            return json.dumps( self.best_tour , default=lambda o: o.__dict__ )
            
        except :
            
            print_exc()
            
            return format_exc()
            
    def __str__( self ):
        
        return json.dumps( self , default=lambda o: o.__dict__ )

class Tour :
    
    def __init__( self , path , length , mutation_rate ):
        self.length        = length
        self.path          = path
        self.cost          = self.calc_cost()       
        self.mutation_rate = ( ( mutation_rate * 100) % self.length )
        
    def calc_cost( self ): # fitness
        
        tmp_sum = 0
        
        for i in xrange( self.length ):
            
            try :
                
                tmp_sum += self.path[ i ] + self.path[i+1]
                
            except IndexError :
                
                pass
                
        return tmp_sum
        
    def __add__( self , other_tour ): # crossover
        
        try : 
            
            # --- crossover
            new_tour = Tour( self.path[ : self.length / 2 ] , self.length , self.mutation_rate )
            
            for city in other_tour.path :
                
                if not city in new_tour.path :
                    
                    new_tour.path.append( city )
                    
            # --- mutation
            
            for index in sample( range( self.length ) , self.mutation_rate ) :
                
                other_tour_index = other_tour.path.index( new_tour.path[index] )
                new_tour.path[index] , new_tour.path[other_tour_index] = new_tour.path[other_tour_index] , new_tour.path[index]
             
            return new_tour 
            
        except :
            
            print_exc()
            
        return None
        
    def __str__( self ):
        
        return json.dumps( self , default=lambda o: o.__dict__ )
        

class City :

    def __init__( self , name , x , y ):
        
        self.name = int(name)
        self.x    = float(x)
        self.y    = float(y)
        
    def __add__( self , other_city ):
        
        return  sqrt( pow( self.x - other_city.x , 2 ) + pow(self.y - other_city.y , 2 )) 
        
    def __str__( self ):
        
        return self.name
        
    def __eq__( self , other_city ):
        
        return self.name == other_city.name
       
    def __contains__( self , other_city ):
        
        return other_city.name == self.name
        
    def coordinates_as_tuple( self ):
        
        return ( self.x , self.y )
        
    def as_tuple( self ):
        
        return ( self.name , self.x , self.y )
        
