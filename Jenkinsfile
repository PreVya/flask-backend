pipeline {
    agent any

    environment {
        CONTAINER_NAME = 'flask-backend'
        IMAGE_NAME = 'flask-backend'
        MONGO_URL = credentials('MONGO_URL')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/PreVya/flask-backend.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:latest .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh '''
                if [ $(docker ps -q -f name=flask-backend) ]; then
                    echo "Stopping old container..."
                    docker stop flask-backend && docker rm flask-backend
                fi
                '''
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                echo "Starting new container..."
                docker run -d --name flask-backend \
                -e MONGO_URL="$MONGO_URL" \
                -p 5000:5000 \
                flask-backend:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Flask backend successfully built and deployed locally.'
        }
        failure {
            echo 'Deployment failed. Check Jenkins logs.'
        }
    }
}