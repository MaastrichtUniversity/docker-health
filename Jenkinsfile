pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command:
                    - cat
                    tty: true
                  - name: kustomize
                    image: k8s.gcr.io/kustomize/kustomize:v5.0.1
                    command:
                    - cat
                    tty: true
            '''
        }
    }

    environment {
        KUBECONFIG_CREDENTIALS = credentials('tst-kubeconfig')
        DOCKER_REGISTRY_CREDENTIALS = credentials('registry-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup kubectl') {
            steps {
                container('kubectl') {
                    // Write kubeconfig from Jenkins credentials
                    sh '''
                        mkdir -p ~/.kube
                        echo "$KUBECONFIG_CREDENTIALS" > ~/.kube/config
                        chmod 600 ~/.kube/config
                    '''
                }
            }
        }

        stage('Deploy to TST') {
            steps {
                container('kustomize') {
                    // Create regcred secret for private registry
                    sh '''
                        kubectl create secret docker-registry regcred \
                            --docker-server=registry.prod.dh.unimaas.nl \
                            --docker-username=$DOCKER_REGISTRY_CREDENTIALS_USR \
                            --docker-password=$DOCKER_REGISTRY_CREDENTIALS_PSW \
                            --namespace=dh-health \
                            --dry-run=client -o yaml | kubectl apply -f -
                    '''
                    
                    // Apply kustomize overlay
                    sh '''
                        cd deploy/overlays/tst
                        kustomize build . | kubectl apply -f -
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                container('kubectl') {
                    // Check deployment status
                    sh '''
                        kubectl wait --for=condition=available deployment --all -n dh-health --timeout=300s
                        kubectl wait --for=condition=complete job --all -n dh-health --timeout=300s
                    '''
                }
            }
        }
    }

    post {
        failure {
            // On failure, get logs and events
            container('kubectl') {
                sh '''
                    kubectl get pods -n dh-health
                    kubectl get events -n dh-health
                    kubectl describe deployment -n dh-health
                '''
            }
        }
    }
}