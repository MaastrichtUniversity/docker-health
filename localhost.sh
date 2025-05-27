#!/bin/bash

MINIKUBE_IP=$(minikube ip)

echo "#Minikube hosts from script" | sudo tee -a /etc/hosts

echo "$MINIKUBE_IP transform.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.local.dh.unimaas.nl" | sudo tee -a /etc/hosts
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

# TODO: Remove lines below?
echo "$MINIKUBE_IP transform.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP federation.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP jupyter.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.mumc.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.zio.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.envida.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP portal.vitala.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.mumc.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.zio.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.envida.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.vitala.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP openehrtool.test.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.mumc.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.zio.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.envida.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.test.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ehrbase.vitala.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.mumc.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.zio.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.envida.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP etl.vitala.tst.dh.unimaas.nl" | sudo tee -a /etc/hosts
