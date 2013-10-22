'''

Vyscond's Walky (vyky)

A Genetic Algorithm for TSPLib Instances

'''

from __future__ import with_statement

__author__ = 'Ramon M.'
__version__ = '0.1.0'
__license__ = 'GPL-3.0'

from math      import sqrt , pow
from traceback import print_exc , format_exc
from random    import randint , shuffle , sample
from copy      import deepcopy
from time      import time 

import json

class TSPInstance :

    def __init__( self , tsp_file  ):
        
        tsp = ''.join( open( tsp_file , 'r' ) ).split('\n') 
        
        entries = {}
        
        for attr in tsp[:6] :
            name , value = attr.split(': ')
            entries[name] = value
            
        tmp = []
        for attr in tsp[7:-3]:
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
            self.mutation_rate = int( ( float(self.mutation_rate) * 100.0) % float(self.tsp_instance.DIMENSION) )
            
            # ---------------------------------------------------
            
            citys = list( self.tsp_instance.NODE_COORD_SECTION )
            
            for i in xrange( self.population_length ):
                
                shuffle( citys )
                
                self.population.append( Tour( list( citys ) , self.tsp_instance.DIMENSION , self.mutation_rate ) )
                
            # ---------------------------------------------------
            
            for i in xrange( self.generations ):
                
                # --- fitness
                
                self.population = sorted( self.population , key = lambda tour : tour.cost )
                
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
                
            return json.dumps( self.best_tour , default=lambda o: o.__dict__ , indent=4 ,separators=(',',':') )
            
        except :
            
            print_exc()
            
            return format_exc()
            
    def __str__( self ):
        
        return json.dumps( self , default=lambda o: o.__dict__ )

class Tour :
    
    def __init__( self , path , length , mutation_rate ):
        
        self.length        = length
        self.path          = path
        self.cost          = sum( [ self.path[ i - 1 ] + self.path[i]  for i in xrange( 1 , self.length )] )       
        self.mutation_rate = mutation_rate 
        
    def __add__( self , other_tour ): # crossover
        
        try : 
            
            tmp_path = list( self.path[ : self.length / 2 ] )
            
            # --- crossover
            for city in other_tour.path :
                
                if not city in tmp_path :
                    
                    tmp_path.append( deepcopy( city ) )
                    
            # --- mutation
            
            for index in sample( range( self.length ) , self.mutation_rate ) :
                
                other_tour_index = other_tour.path.index( tmp_path[index] )
                
                tmp_path[index] , tmp_path[other_tour_index] = tmp_path[other_tour_index] , tmp_path[index]
             
            return Tour( tmp_path , self.length , self.mutation_rate ) 
            
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
        
        #return str(self.name)
        return json.dumps( self , default=lambda o: o.__dict__ )
        
    def __eq__( self , other_city ):
        
        return self.name == other_city.name
       
    def __contains__( self , other_city ):
        
        return self.name == other_city.name
        
    def coordinates_as_tuple( self ):
        
        return ( self.x , self.y )
        
    def as_tuple( self ):
        
        return ( self.name , self.x , self.y )
        
