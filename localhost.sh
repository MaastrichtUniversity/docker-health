#!/bin/bash

MINIKUBE_IP=$(minikube ip)

echo "" | sudo tee -a /etc/hosts > /dev/null
echo "# Minikube hosts script" | sudo tee -a /etc/hosts > /dev/null
echo "$MINIKUBE_IP transform.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP jupyter.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.test.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.mumc.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.zio.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.envida.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.test.local.dh.unimaas.nl" | sudo tee -a /etc/hosts