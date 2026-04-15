#!/bin/bash

MINIKUBE_IP=$(minikube ip)

echo "#Minikube hosts from script" | sudo tee -a /etc/hosts

echo "$MINIKUBE_IP elk.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP transform.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP transform.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP transform.test.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP transform.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP transform.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP terminology.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP terminology.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP terminology.test.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP terminology.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP terminology.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP jupyter.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.test.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.test.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.vitala.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP traefik.dashboard.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP grafana.local.dh.unimaas.nl" | sudo tee -a /etc/hosts

