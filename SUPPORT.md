# Troubleshooting

## Images Not Found

If you see `ImagePullBackOff` errors, ensure you've built the images with Minikube's Docker daemon:

```bash
eval $(minikube docker-env)
docker-compose build
kubectl rollout restart deployment -n dh-health
```

## Storage Issues

For persistent storage issues:

```bash
# Ensure storage provisioner is enabled
minikube addons enable storage-provisioner

# Check PVC status
kubectl get pvc -n dh-health
```

## Ingress Not Working

Check if the ingress controller is properly installed:

```bash
kubectl get pods -n ingress-nginx
```

## Troubleshooting MacOS specifically

Kubernetes on MacOS is less straight forward unfortunately. While trying to run Kubernetes, you may run into the
following issues:

1. Errors while trying to run `minikube start`. This seems to be due to Minikube defaulting to the `None` driver on
   MacOS, which is not supported on Darwin(OS)/arm64. This can be fixed by specifying the driver for Minikube to use:

```bash
# minikube needs to be running to check its profiles
minikube start
# check which driver you should use, e.g. docker
minikube profile list
minikube delete; minikube start --driver=docker
```

2. The `sed` command, used in checking for- and deleting duplicates related to specific virtual hosts in `/etc/hosts`,
   may not initially be recognised on MacOS. Install it manually through Homebrew
   via [gnu-sed](https://formulae.brew.sh/formula/gnu-sed). Be sure to add a "gnubin" directory to your PATH from your
   bashrc/zshrc (on newer macs) to allow for use of the 'sed' command instead of their default 'gsed':

```
# allows for use of 'sed' instead of 'gsed'; HOMEBREW_PREFIX is the location of your homebrew (`which brew`)
PATH="$HOMEBREW_PREFIX/opt/gnu-sed/libexec/gnubin:$PATH"
```

Restart the terminal for the change to take effect:

```bash
source ~/.zshrc
```

3. Minikube seemingly being starved of resources. This problem in particular could present itself when trying to start
   the `ehrdb` and `ehrbase` pods, where the pods continuously timeout and restart. Using the following does not work on
   MacOS:

```bash
minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
```

Instead, specify the allocated resources through the minikube config file with the number of cpus and amount of memory
you require. Good practise is to leave some breathing room for your OS, so do not max the amount of cpus and memory
based on your specific system specs:

```bash
minikube config set cpus 4 # specify number of cpus you require
minikube config set memory 8192 # specify amount of memory you require
```

These changes take effect after restarting minikube and should persist across sessions.

4. By default, the Minikube ip (through `minikube ip`) will be used and added to the virtual hosts in `/etc/hosts`.
   However, using the Minikube ip does not work for this purpose on MacOS. Instead, use `127.0.0.1` and add these to
   `/etc/hosts` manually:

```
# these can replace the minikube ips
127.0.0.1 ehrbase.envida.local.dh.unimaas.nl
127.0.0.1 ehrbase.mumc.local.dh.unimaas.nl
127.0.0.1 ehrbase.test.local.dh.unimaas.nl
127.0.0.1 ehrbase.zio.local.dh.unimaas.nl
127.0.0.1 ehrbase.vitala.local.dh.unimaas.nl
127.0.0.1 elk.local.dh.unimaas.nl
127.0.0.1 etl.envida.local.dh.unimaas.nl
127.0.0.1 etl.mumc.local.dh.unimaas.nl
127.0.0.1 etl.zio.local.dh.unimaas.nl
127.0.0.1 etl.vitala.local.dh.unimaas.nl
127.0.0.1 federation.mumc.local.dh.unimaas.nl
127.0.0.1 federation.zio.local.dh.unimaas.nl
127.0.0.1 federation.envida.local.dh.unimaas.nl
127.0.0.1 federation.vitala.local.dh.unimaas.nl
127.0.0.1 jupyter.local.dh.unimaas.nl
127.0.0.1 openehrtool.envida.local.dh.unimaas.nl
127.0.0.1 openehrtool.mumc.local.dh.unimaas.nl
127.0.0.1 openehrtool.test.local.dh.unimaas.nl
127.0.0.1 openehrtool.zio.local.dh.unimaas.nl
127.0.0.1 openehrtool.vitala.local.dh.unimaas.nl
127.0.0.1 portal.envida.local.dh.unimaas.nl
127.0.0.1 portal.mumc.local.dh.unimaas.nl
127.0.0.1 portal.zio.local.dh.unimaas.nl
127.0.0.1 portal.vitala.local.dh.unimaas.nl
127.0.0.1 terminology.local.dh.unimaas.nl
127.0.0.1 transform.envida.local.dh.unimaas.nl
127.0.0.1 transform.mumc.local.dh.unimaas.nl
127.0.0.1 transform.test.local.dh.unimaas.nl
127.0.0.1 transform.vitala.local.dh.unimaas.nl
127.0.0.1 transform.zio.local.dh.unimaas.nl
127.0.0.1 traefik.dashboard.local.dh.unimaas.nl
```


5. There is an issue regarding the ingress and ingress-dns addons on MacOS. In order to work around this, use
   `minikube tunnel`. This tunnel creates a route to services deployed with the LoadBalancer type and sets their Ingress
   to their ClusterIPs. Use a different terminal for this because it has to stay open:

```bash
# in a different terminal; sudo is required
sudo minikube tunnel
```

After all that, the following seems to work:

```bash
minikube start --driver=docker
minikube addons enable ingress
./dh.sh setup
./dh.sh pull
./dh.sh build
# in a different terminal; sudo is required
sudo minikube tunnel
./dh.sh apply
```

### Troubleshooting SEBP/ELK on MacOS
MacOS requires the `sebp/elk:9.1.5` image to be built in `ARM64` architecture to function. The image we are currently
using in the repository uses `AMD64` architecture and will not work on MacOS. The solution is to build the image in `ARM64`
instead, but it requires a few additional steps. The initial process remains the same:
```bash
minikube start --driver=docker
minikube addons enable ingress
./dh.sh setup # remember to change the etc/host/ ip values here, see above
./dh.sh pull
```
Then, **before** using `./dh.sh build`, first do the following to build the `sebp/elk:9.1.5`image in `ARM64` inside the
Minikube container:
```bash
minikube ssh # go inside the minikube container
git clone https://github.com/spujadas/elk-docker.git
cd elk-docker
git checkout 9.1.5 # the specific version you want to use
docker build --platform=linux/arm64 --build-arg ARCH=aarch64 -t sebp/elk:9.1.5 . # build & tag the image with 'sebp/elk:9.1.5'
exit
```
Then, outside the Minikube container, resume the usual process:
```bash
./dh.sh build
./dh.sh apply local/ops
```
ELK should now be up and running and its UI can be access through http://elk.local.dh.unimaas.nl/.
