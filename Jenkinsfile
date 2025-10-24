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
                sh """
                if [ \$(docker ps -q -f name=$CONTAINER_NAME) ]; then
                    echo "Stopping old container..."
                    docker stop $CONTAINER_NAME && docker rm $CONTAINER_NAME
                fi
                """
            }
        }

        stage('Run New Container') {
            steps {
                sh """
                echo "Starting new container..."
                docker run -d --name $CONTAINER_NAME \
                -e MONGO_URL=$MONGO_URL \
                -p 5000:5000 \
                $IMAGE_NAME:latest
                """
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