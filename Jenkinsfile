pipeline {
    agent any

    stages {
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
