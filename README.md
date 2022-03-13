# k8s-diagrams

Prototype for a K8s diagram generator. 

The aim is to generate human-consumable diagrams from templated manifests or from `kubectl get all > ns.yaml`.

Then to be used in architectual documentation as references.

Currently does Services, Deployments and Statefulsets, additional objects should just require expanding the composer definitions. 