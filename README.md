# Kube-inspec
Inspec as a Cronjob in Kubernetes

## What are we trying to solve with that

- Having hosts being managed by a FreeIPA server (https://www.freeipa.org/)
- Wanting so audit them with Inspec (https://www.inspec.io/)
- Seding the result to an ElasticSearch (https://www.elastic.co/)

## How do we do this

- Using the Chef Inspec container
- Using a Python script that connect to the FreeIPA server and fetch all the hosts.
- For each host, scanning them with Inspec using the Git repo passed as an environment variable
- For each host, posting the result to an ElasticSearch 

## How can I use this

Upcoming !

## ToDo
- Kibana Dashboard
- Variable Inspec usage
  - OS
  - Database
  - What else
