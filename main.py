from imports import *
from parse import load
from map import K8sMap

def main(): 
  manifests = load('manifest')

  map = K8sMap(manifests)

  map.draw()

main()