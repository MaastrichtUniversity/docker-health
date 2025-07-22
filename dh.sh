#!/bin/bash

set -e

# Colors for better readability
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

# Define logging constants and functions first
# These should be defined at the top as they're used by other functions
DBG=0
INF=1
WRN=2
ERR=3
LOGTRESHOLD=${LOGTRESHOLD:-$INF}

# Logging function
log() {
    local level=$1
    shift
    if [[ $level -ge $LOGTRESHOLD ]]; then
        if [[ $level -eq $DBG ]]; then
            echo -e "\e[90m[DEBUG] $@\033[0m"
        elif [[ $level -eq $INF ]]; then
            echo -e "[INFO ] $@"
        elif [[ $level -eq $WRN ]]; then
            echo -e "\e[33m[WARN ] $@\033[0m"
        elif [[ $level -eq $ERR ]]; then
            echo -e "\e[31m[ERROR] $@\033[0m"
        fi
    fi
}

# Abort function
abort() {
    log $ERR "$@"
    exit 1
}

# Process command line arguments
ARGS="$@ "
if [[ ${ARGS} = *"-vv "* ]]; then
   export LOGTRESHOLD=$DBG
   ARGS="${ARGS/-vv /}"
elif [[ ${ARGS} = *"--verbose "* ]] || [[ ${ARGS} = *"-v "* ]]; then
   export LOGTRESHOLD=$INF
   ARGS="${ARGS/--verbose /}"
   ARGS="${ARGS/-v /}"
fi

# Define function for handling external repositories
function run_repo_action {
    log $DBG "${FUNCNAME[0]} $@"

    # validate number of params
    if [[ $# -lt 2 ]]; then
        abort "${FUNCNAME[0]}: illegal number of params"
    fi

    # split 'action' in (git)action and options
    rra_action=${1/ */}               # remove all after first space
    rra_options=${1/$rra_action/}     # remaining part is first part of options
    shift
    while [[ ${1:0:6} != "extern" ]] && [[ ${1:0:6} != "docker" ]]; do
        rra_options="$rra_options $1"
        shift
    done
    rra_options="$(echo -e "${rra_options}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"    #trim surrounding spaces
    rra_externals=$1

    # validate params
    if [[ -z $rra_action ]]; then
        abort "${FUNCNAME[0]}: missing parameter [action]"
    fi
    if [[ "$rra_externals" == "" ]]; then
        log $INF "No externals provided, so action '$1' needs nothing to do"
        return
    fi

    # determin current folder name
    baserepo=$(basename $(pwd))

    # processing
    while read -r rra_external; do
        rra_external=($rra_external)
        echo -e "\e[32m=============== $baserepo/${rra_external[0]} ======================\033[0m"
        # compose git command (depending on action this might differ)
        if [[ $rra_action == "clone" ]]; then
            cmd="git clone ${rra_external[1]} ${rra_external[0]}"
        elif [[ $rra_action == "pull" ]]; then
            cmd="git -C ${rra_external[0]} pull --rebase"
        else
            cmd="git -C ${rra_external[0]} $rra_action $rra_options"
        fi
        # execute the composed git command (and set errorcode in case it failed)
        log $DBG "executing: $cmd"
        retval=0
        $cmd || retval=$?
        log $DBG "command returned: $retval"
        # show warning in case of error!
        if [[ "$retval" -gt 0 ]]; then
            log $WRN "Issue occurred while executing command '$cmd'"
        fi
    done <<< "$rra_externals"
}

# Set script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Default values
K8S_NAMESPACE="dh-health"
ENV_TAG="latest"

# specify externals for this project
externals="externals/dh-hdp-zib-templates https://github.com/um-datahub/dh-hdp-zib-templates.git
externals/dh-hdp-transform-rest https://github.com/MaastrichtUniversity/dh-hdp-transform-rest.git
externals/dh-hdp-etl https://github.com/MaastrichtUniversity/dh-hdp-etl.git
externals/dh-hdp-federation-api https://github.com/MaastrichtUniversity/dh-hdp-federation-api.git
externals/dh-hdp-notebooks https://github.com/MaastrichtUniversity/dh-hdp-notebooks.git
externals/dh-hdp-portal https://github.com/MaastrichtUniversity/dh-hdp-portal.git
externals/dh-hdp-etl-utils https://github.com/MaastrichtUniversity/dh-hdp-etl-utils.git"

# Check if minikube is running
check_minikube() {
    if ! minikube status &>/dev/null; then
        echo -e "${YELLOW}Minikube is not running. Starting Minikube...${NC}"
        minikube start --cpus 4 --memory 8192 --disk-size=30g --driver=docker
        minikube addons enable ingress
        minikube addons enable ingress-dns
    fi

    # Set docker environment to minikube's docker
    echo -e "${YELLOW}Setting docker environment to Minikube's docker daemon${NC}"
    eval $(minikube docker-env)
}

# Build an image or all images
build_images() {
    local service_name=$1
    local image_tag=${2:-latest}
    
    if [[ -z "$service_name" ]]; then
        echo -e "${YELLOW}Building all services using docker-bake...${NC}"
        docker buildx bake
    else
        echo -e "${YELLOW}Building service: $service_name using docker-bake...${NC}"
        docker buildx bake $service_name --set=\*.tags=registry.prod.dh.unimaas.nl/docker-health/$service_name:$image_tag
    fi
    
    if [[ $? -eq 0 ]]; then
        if [[ -z "$service_name" ]]; then
            echo -e "${GREEN}Successfully built all services with tag: $image_tag${NC}"
        else
            echo -e "${GREEN}Successfully built service: $service_name:$image_tag${NC}"
        fi
    else
        echo -e "${RED}Error building service(s)${NC}"
        return 1
    fi
}

# Apply kubernetes manifests
apply_manifests() {
    local overlay=${1:-local}
    
    echo -e "${YELLOW}Applying Kubernetes manifests using kustomize overlay: $overlay${NC}"
    kubectl apply -k deploy/overlays/$overlay | awk '/created|configured/ {print "\033[1;34m" $0 "\033[0m"; next} {print}'

    echo -e "${GREEN}Successfully applied manifests${NC}"
}

# Check a job execution status
check_job_execution(){
  job=$1
  echo "Waiting for job $job to complete..."
  while true; do
    succeeded=$(kubectl get job "$job" -n dh-health -o jsonpath='{.status.succeeded}')
    if [ "$succeeded" = "1" ]; then
      echo -e "${GREEN}$job is complete.${NC}"
      kubectl delete -f deploy/overlays/$overlay/job.yaml
      exit 0
    fi

    failed=$(kubectl get job "$job" -n dh-health -o jsonpath='{.status.failed}')
    if [ "$failed" != "" ] && [ "$failed" -ge 1 ]; then
      echo -e "${RED}❌ $job has failed. Exiting.${NC}"
      exit 1
    fi
    echo "$job not completed yet, sleeping 5s..."
    sleep 5
  done
}


# Setup ingress host entries using existing localhost.sh script
setup_hosts() {
    # Get the current Minikube IP
    local minikube_ip=$(minikube ip)
    if [ -z "$minikube_ip" ]; then
        echo -e "${RED}Error: Could not get Minikube IP. Make sure Minikube is running correctly.${NC}"
        return 1
    fi

    # First check if localhost.sh exists and is executable
    if [ ! -f "./localhost.sh" ]; then
        echo -e "${RED}localhost.sh not found. Creating a basic version...${NC}"
        cat > ./localhost.sh << 'EOF'
#!/bin/bash
MINIKUBE_IP=$(minikube ip)

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
EOF
        chmod +x ./localhost.sh
    fi

    # Extract hosts from localhost.sh
    echo -e "${YELLOW}Updating host entries in /etc/hosts...${NC}"
    hosts=$(grep -o '[a-z0-9.-]\+\.local\.dh\.unimaas\.nl' ./localhost.sh | sort | uniq)
    
    # Create a temporary file
    temp_file=$(mktemp)
    
    # For each host in our list, remove its existing entry from /etc/hosts if present
    cat /etc/hosts > "$temp_file"
    for host in $hosts; do
        # Remove any line containing this specific hostname
        sed -i "/[[:space:]]$host\$/d" "$temp_file"
    done
    
    # Apply the modified hosts file without our entries
    sudo cp "$temp_file" /etc/hosts
    rm "$temp_file"
    
    # Now add the hosts with current Minikube IP
    echo -e "${YELLOW}Adding host entries with current Minikube IP (${minikube_ip})...${NC}"
    for host in $hosts; do
        echo "$minikube_ip $host" | sudo tee -a /etc/hosts > /dev/null
    done
    
    echo -e "${GREEN}Host entries updated using current Minikube IP${NC}"
}

# Mount local directories to minikube
pull_docker_images() {
    echo -e "${YELLOW}Pull external docker images${NC}"
    ./pull-external-images.sh
}

# Mount local directories to minikube
setup_mounts() {
    echo -e "${YELLOW}Setting up directory mounts in Minikube${NC}"
    if ! ls externals &>/dev/null; then
        echo -e "${RED}Error: External repos are not pulled"
        return 1
    fi
    ./mount.sh
}

# Helper functions for external repos
clone_externals() {
    # Check if externals directory exists and is not empty
    if [ -d "externals" ] && [ "$(ls -A externals 2>/dev/null)" ]; then
        echo $INF "External repositories already exist. Skipping clone."
        return 0
    fi
    
    # Create externals directory if it doesn't exist
    mkdir -p externals
    
    # Proceed with cloning if directory is empty
    run_repo_action "clone" "${externals}"
}

checkout_externals() {
    local branch=${1:-2024.1}
    # Check if any externals exist first
    if [ ! -d "externals" ] || [ -z "$(ls -A externals 2>/dev/null)" ]; then
        log $INF "External repositories don't exist yet. Cloning first..."
        clone_externals
    fi

    # dh-hdp-etl-utils is on main branch instead of 2024.1
    etl_utils_repo="externals/dh-hdp-etl-utils https://github.com/MaastrichtUniversity/dh-hdp-etl-utils.git"

    while IFS= read -r repo_path; do
    repo_path=$(echo "$repo_path" | xargs)  # Trim leading/trailing whitespace
    if [[ "$repo_path" == "$etl_utils_repo" ]]; then
        run_repo_action "checkout main" "$repo_path"
    else
        run_repo_action "checkout $branch" "$repo_path"
    fi
done <<< "$externals"
}

# Print usage
print_usage() {
    echo "Usage: $0 <command> [options]"
    echo
    echo "Commands:"
    echo "  setup                        Initialize Minikube Kubernetes environment with docker engine"
    echo "  start                        Start an already initialized Minikube Kubernetes environment with docker engine"
    echo "  pull                         Pull external images"
    echo "  build       <subcommand>     Build service images"
    echo "  externals   <subcommand>     Manage external repositories"
    echo "  apply       <subcommand>     Apply Kubernetes manifests (default overlay: local)"
    echo "  delete      <subcommand>     Delete Kubernetes manifests (default overlay: local)"
    echo "  status      <subcommand>     Show status of all pods"
    echo "  rollout     <subcommand>     Manage the rollout to restart one or many resources (default all)"
    echo "  up          <subcommand>     Apply a subset of deployments"
    echo "  down        <subcommand>     Delete a subset of deployments"
    echo "  run         <subcommand>     Apply Kubernetes manifests and wait & check the job (with the same name) execution"
    echo "  headlamp                     Enable the addons headlamp, start the service and create a temporary token"
    echo
    echo "Examples:"
    echo "  $0 setup                  Setup Kubernetes environment"
    echo "  $0 start                  Start Kubernetes environment"
    echo "  $0 build                  Build all Docker images"
    echo "  $0 apply                  Apply Kubernetes manifests with local overlay"
    echo "  $0 apply tst              Apply Kubernetes manifests with tst overlay"
    echo "  $0 delete                 Delete Kubernetes manifests with local overlay"
    echo "  $0 delete tst             Delete Kubernetes manifests with tst overlay"
    echo "  $0 status                 Print the pods status"
    echo "  $0 status -w              Print and follow the pods status"
    echo "  $0 rollout                Rollout a restart of all the deployments"
    echo "  $0 rollout jupyter-zib    Rollout a restart of the jupyter-zib deployment"
    echo "  $0 up test-node           Apply Kubernetes manifests with local overlay & the label test-node"
    echo "  $0 up others              Apply Kubernetes manifests with local overlay & without the labels test-node"
    echo "  $0 down test-node         Delete Kubernetes manifests with local overlay & the label test-node"
    echo "  $0 down others            Delete Kubernetes manifests with local overlay & without the labels test-node"
    echo "  $0 run test-single-node   Apply Kubernetes manifests with 'test-single-node' overlay & wait and check of the job execution status"
    echo "  $0 run test-federation    Apply Kubernetes manifests with 'test-federation' overlay & wait and check of the job execution status"
}

# Main command handler
main() {
    local command=$1
    shift || true

    TEST_NODE_LABELS="ehrnode in (test-node, all)"
    OTHERS_LABELS="ehrnode notin (test-node)"
    
    case $command in
        setup)
            check_minikube
            clone_externals
            setup_hosts
            setup_mounts
            ;;

        pull)
            check_minikube
            pull_docker_images
            ;;
            
        build)
            check_minikube
            build_images "$@"
            ;;

        start)
            check_minikube
            ;;

        rollout)
            kubectl rollout restart deployment "$@" -n dh-health
            ;;

        apply)
            local overlay=${1:-local}
            apply_manifests $overlay
            ;;

        delete)
            local overlay=${1:-local}
            kubectl delete -k "deploy/overlays/${overlay}"
            ;;

        headlamp)
            minikube addons enable headlamp
            minikube service headlamp -n headlamp
            kubectl create token headlamp --duration 24h -n headlamp
            ;;

        status)
            kubectl get pods -n $K8S_NAMESPACE "$@"
            ;;

        run)
            local overlay=$1
            apply_manifests "$overlay"
            check_job_execution "$overlay"
            ;;

        up)
            case $1 in
              test-node)
                kubectl apply -k deploy/overlays/local -l "${TEST_NODE_LABELS}"
                ;;
              others)
                kubectl apply -k deploy/overlays/local -l "${OTHERS_LABELS}"
                ;;
            esac
            ;;

        down)
            case $1 in
              test-node)
                kubectl delete -k deploy/overlays/local -l "${TEST_NODE_LABELS}"
                ;;
              others)
                kubectl delete -k deploy/overlays/local -l "${OTHERS_LABELS}"
                ;;
            esac
            ;;
            
        *)
            echo -e "${RED}Unknown command: $command${NC}"
            print_usage
            exit 1
            ;;
    esac
}

# Special case for externals command (keep original behavior)
if [[ $1 == "externals" ]]; then
    action=${ARGS/$1/}
    run_repo_action ${action} "${externals}"
    exit 0
fi

# Run the script
if [ $# -eq 0 ]; then
    print_usage
    exit 0
fi

main "$@"
