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
        GIT_TOKEN = credentials('datahub-git-token')
    }

    parameters {
        string(name: 'TARGET_BRANCH', defaultValue: 'develop', description: 'Target branch to deploy')
        string(name: 'FALLBACK_BRANCH', defaultValue: 'main', description: 'Fallback branch if target fails')
    }

    stages {
        stage('Setup Git') {
            steps {
                script {
                    // Clean workspace
                    cleanWs()
                    
                    // Configure Git credentials
                    sh '''
                        git config --global credential.helper store
                        echo "https://datahub-deployment:${GIT_TOKEN}@github.com" > ~/.git-credentials
                        chmod 600 ~/.git-credentials
                    '''
                    
                    // Checkout with fallback logic
                    try {
                        checkout([$class: 'GitSCM',
                            branches: [[name: "*/${params.TARGET_BRANCH}"]],
                            userRemoteConfigs: [[
                                url: 'https://github.com/MaastrichtUniversity/docker-health.git',
                                credentialsId: 'datahub-git-token'
                            ]]
                        ])
                    } catch (Exception e) {
                        echo "Checking out target branch failed, using fallback instead"
                        checkout([$class: 'GitSCM',
                            branches: [[name: "*/${params.FALLBACK_BRANCH}"]],
                            userRemoteConfigs: [[
                                url: 'https://github.com/MaastrichtUniversity/docker-health.git',
                                credentialsId: 'datahub-git-token'
                            ]]
                        ])
                    }
                }
            }
        }

        stage('Deploy to Test') {
            steps {
                container('kubectl') {
                    sh '''
                        mkdir -p ~/.kube
                        echo "$KUBECONFIG_CREDENTIALS" > ~/.kube/config
                        chmod 600 ~/.kube/config
                    '''
                }
                
                container('kustomize') {
                    script {
                        // Create registry secret
                        sh '''
                            kubectl create secret docker-registry regcred \
                                --docker-server=registry.prod.dh.unimaas.nl \
                                --docker-username=$DOCKER_REGISTRY_CREDENTIALS_USR \
                                --docker-password=$DOCKER_REGISTRY_CREDENTIALS_PSW \
                                --namespace=dh-health \
                                --dry-run=client -o yaml | kubectl apply -f -
                        '''
                        
                        // Deploy using test overlay
                        sh '''
                            cd deploy/overlays/tst
                            kustomize build . | kubectl apply -f -
                        '''
                    }
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
        always {
            sh 'rm -f ~/.git-credentials'
        }
    }
}