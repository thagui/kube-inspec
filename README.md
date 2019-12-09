# Kube-inspec
Inspec as a Cronjob in Kubernetes

## What are we trying to solve with that

- Having hosts being managed by a FreeIPA server (https://www.freeipa.org/)
- Wanting to audit them with Inspec (https://www.inspec.io/)
- Sending the results to an ElasticSearch (https://www.elastic.co/)
- Having a periodic job doing all of this !

## How do we do this

- Using the Chef Inspec container
- Using a Python script that connect to the FreeIPA server and fetch all the hosts.
- For each host, scanning them with Inspec using the Git repo passed as an environment variable
- For each host, posting the result to an ElasticSearch 
- Defining a cronjob in k8s to do this !

## How can I use this

Upcoming !

## ToDo
- Kibana Dashboard
- Variable Inspec usage
  - OS
  - Database
  - What else
