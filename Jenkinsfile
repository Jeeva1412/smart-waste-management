pipeline {
    agent any

    environment {
        IMAGE_NAME = 'smartwasteapp'
        APP_PORT = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Jeeva1412/smart-waste-management.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                script {
                    // Stop and remove old container if exists
                    sh '''
                    if [ $(docker ps -aq -f name=smartwaste_container) ]; then
                        docker stop smartwaste_container
                        docker rm smartwaste_container
                    fi
                    '''
                    // Run container
                    sh "docker run -d -p ${APP_PORT}:8000 --name smartwaste_container $IMAGE_NAME"
                }
            }
        }

        stage('Health Check') {
            steps {
                sh 'curl --fail http://localhost:8000 || exit 1'
            }
        }
    }
    
    post {
        failure {
            echo 'Build or deployment failed!'
        }
        success {
            echo 'Build and deployment successful!'
        }
    }
}
