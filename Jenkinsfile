pipeline {
    agent any

    stages {
        stage('Install Tooling') {
            steps {
                sh '''
                    set -e

                    install_with_sudo() {
                      if command -v sudo >/dev/null 2>&1; then
                        sudo "$@"
                      else
                        "$@"
                      fi
                    }

                    if ! command -v docker >/dev/null 2>&1; then
                      install_with_sudo apt-get update
                      install_with_sudo apt-get install -y docker.io
                    fi

                    if ! command -v kubectl >/dev/null 2>&1; then
                      curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                      install_with_sudo install -m 0755 kubectl /usr/local/bin/kubectl
                      rm -f kubectl
                    fi

                    if ! command -v minikube >/dev/null 2>&1; then
                      curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
                      install_with_sudo install minikube-linux-amd64 /usr/local/bin/minikube
                      rm -f minikube-linux-amd64
                    fi

                    docker --version
                    kubectl version --client
                    minikube version
                '''
            }
        }

        stage('Build Image') {
            steps {
                sh 'docker build -t notes-api:latest .'
            }
        }

        stage('Load Image To Minikube') {
            steps {
                sh 'minikube image load notes-api:latest'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f k8s-deployment.yaml'
                sh 'kubectl rollout restart deployment/notes-api'
                sh 'kubectl rollout status deployment/notes-api'
            }
        }
    }
}
