from imports import *
from composer import BuildModel, LinkModel

class K8sMap:
  def __init__(self, k8s_objects):
    self.name = "Test"
    self.k8s_objects = k8s_objects
    self.apps = self.parse_apps()
    self.map = self.map()
    self.manifest = self.generate_manifest()

  def lookup_object(self, id) -> dict:
    for o in self.k8s_objects: 
      if o['mappingId'] == id:
        return o

  def map(self) -> list:
    return self.map_services()

  def draw(self):
    flatlist = {}
    with Diagram(self.name, show=False) as diagram:
      BuildModel(self.manifest["components"], flatlist)
      LinkModel(self.manifest["connections"], flatlist)
      

  def parse_apps(self) -> list:
    # Get apps returns the namespace/name and two lists, one containing mapped cms, vols, secrets and one containing the selectors
    app_list = []

    for obj in self.k8s_objects:
      if obj["apiVersion"] == "apps/v1":
        if 'namespace' in obj["metadata"].keys():
          namepsace = obj["metadata"]["namespace"]
        else:
          namespace = 'default'
          
        selector_labels = obj["spec"]["template"]["metadata"]["labels"]

        if 'volumeMounts' in obj["spec"]["template"]["spec"]:      
          volumes = obj["spec"]["template"]["spec"]["volumeMounts"]
        else:
          volumes = {}
        
        app = {
          'namespace': namespace,
          'name': obj["metadata"]["name"],
          'kind': obj["kind"],
          'selectors': selector_labels,
          'volumes': volumes,
          'mappingId': obj["mappingId"]
        }

        app_list.append(app)

    return app_list

  def generate_manifest(self) -> dict:
    boilerplate = {
      "project_name": self.name,
      "diagram_name": self.name,
      "components": [

      ],
      "connections": [

      ]

    }

    for o in self.k8s_objects:
      component = {
        "name": f'{o["kind"]}/{o["metadata"]["name"]}',
        "type": o["kind"]
      }

      boilerplate["components"].append(component)
    
    for s in self.map:
      f = self.lookup_object(s[0])
      t = self.lookup_object(s[2])
      connection = {
        "from": f'{f["kind"]}/{f["metadata"]["name"]}',
        "to": f'{t["kind"]}/{t["metadata"]["name"]}'
      }
      boilerplate["connections"].append(connection)

    return boilerplate

  def map_services(self) -> list:
    # map services creates and returns a map 
    # of service to apps

    mapping_list = []

    for obj in self.k8s_objects:
      if obj["apiVersion"] == "v1" and obj["kind"] == "Service":
        service_selectors = obj["spec"]["selector"]

        for app in self.apps:
          app_selectors = app["selectors"]

          shared_kvs = {k :service_selectors[k] for k in service_selectors if k in app_selectors and app_selectors[k] == service_selectors[k]}        

          if service_selectors.items() <= shared_kvs.items():
                
            mapping_list.append((obj["mappingId"], '>>', app["mappingId"]))

    return mapping_list