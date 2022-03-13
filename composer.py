from imports import *

def BuildModel(components, flatlist):
    for component in components:
        if component["type"] == "Service":
            flatlist[component["name"]] = Service(component["name"].split('/')[1])
        elif component["type"] == "StatefulSet":
            flatlist[component["name"]] = StatefulSet(component["name"].split('/')[1])
        elif component["type"] == "Deployment":
            flatlist[component["name"]] = Deployment(component["name"].split('/')[1])

def LinkModel(connections, flatlist):
    for item in connections:
        flatlist[item["from"]] >> flatlist[item["to"]]