from collections import namedtuple
from operator import itemgetter
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
from __future__ import division
import numpy as np
from time import time
import pandas as pd
import csv

RADIUS_OF_EARTH_IN_KM = 6372.8

fig =plt.figure(figsize=(10, 8), dpi=80)
ax = plt.gca()


def haversine(p1  , p2):
   distance = 0.0
   for i in range(3):
     distance += (p1[i] - p2[i]) ** 2
   return sqrt(distance)
      
def parse_tree(node,prev_node=None,label='Root'):
  
    if node is None:
        return
    ax.plot(node.cell[0],node.cell[1],'ro')
    ax.text(node.cell[0],node.cell[1],label + ' ' + str(node.cell[2]))
    if prev_node:
        ax.plot([node.cell[0],prev_node.cell[0]],[node.cell[1],prev_node.cell[1]])
    parse_tree(node.left_branch,node,label='L')
    parse_tree(node.right_branch,node,label='R')
    
def find_nearest_neighbour(node,point,distance_fn,current_axis):

    if node is None:
        return None,None
    current_closest_node = node
    closest_known_distance = distance_fn(node.cell , point)
    
    x = (node.cell[0],node.cell[1],node.cell[2])
    y = point
    
    new_node = None
    new_closest_distance = None
    if x[current_axis] > y[current_axis]:
        new_node,new_closest_distance= find_nearest_neighbour(node.left_branch,point,distance_fn,
                                                          (current_axis+1) %3)
    else:
        new_node,new_closest_distance = find_nearest_neighbour(node.right_branch,point,distance_fn,
                                                           (current_axis+1) %3) 
    
    if  new_closest_distance and new_closest_distance < closest_known_distance:
        closest_known_distance = new_closest_distance
        current_closest_node = new_node
        
    return current_closest_node,closest_known_distance
    
    
class Node(namedtuple('Node','cell, left_branch, right_branch')):
    # Esta clase está tomada del fragmento de código de la wikipedia para el árbol KD
    pass
    
def create_kdtree(cell_list,current_axis,no_of_axis):
    # Crea un árbol KD recursivamente siguiendo el fragmento de wikipedia para el árbol KD
    # pero haciéndolo genérico para cualquier número de ejes y cambios en la estructura de datos
    if not cell_list:
        return
    # sget the cell as a tuple list
    k= [(cell[0],cell[1],cell[2])  for cell  in cell_list]
    k.sort(key=itemgetter(current_axis)) # ordenar las actuales axis
    median = len(k) // 2 # media de la lista
    axis = (current_axis + 1) % no_of_axis # cycle the axis
    return Node(k[median], # recursion 
                create_kdtree(k[:median],axis,no_of_axis),
                create_kdtree(k[median+1:],axis,no_of_axis))

i = 0
df = pd.read_csv('20000.csv')
cell_list = list(df.itertuples(index=False, name=None))

start_time = time()
tree = create_kdtree(cell_list,0,3)
elapsed_time = time() - start_time
elapsed_time = elapsed_time * 1000
print("Elapsed time of insert: %0.10f ms." % elapsed_time)
#parse_tree(tree)
#plt.show()

queries_20000 = [(2863, 12030, 8217) , (3268, 12927, 2714), (5037, 19169, 4791), (6117, 7670, 3173), (7495, 2897, 4857), (7507, 765, 19003), (11538, 6689, 2942), (13916, 16922, 13400), (16900, 11807, 7612), (19221, 1893, 8179)]
for q in queries_20000 :
  start_time = time()
  node,distance = find_nearest_neighbour(tree, q, haversine,0)
  elapsed_time = time() - start_time
  elapsed_time = elapsed_time * 1000
  print("Elapsed time of neighbour: %0.10f ms." % elapsed_time)
  print ("Nearest Neighbour= ",node.cell,distance , "\n")