from imports import *

def load(dir_path: str) -> list:
  files = os.walk(dir_path)
  
  k8s_objects = []

  i = 0

  for parent in files:
    for children in parent[2]:
      f = os.path.join(parent[0], children)
      with open(f, "r") as stream:
        try: 
          l = yaml.safe_load_all(stream)
          for y in l:
            i +=  1
            if all(key in y.keys() for key in ['apiVersion', 'kind', 'metadata']):
              y["mappingId"] = i
              k8s_objects.append(y)
            else: 
              print(f'Bad manifest at {f}, skipping...')                
        except yaml.YAMLError as e:
          print(e)            
    

  return k8s_objects