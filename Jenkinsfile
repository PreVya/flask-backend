pipeline {
    agent any

    environment {
        CONTAINER_NAME = 'flask-backend'
        IMAGE_NAME = 'docker.io/prevya/flask-backend'
        MONGO_URL = credentials('MONGO_URL')
        BACKEND_URL = credentials('BACKEND_URL')
        DOCKER_NAME = credentials('DOCKER_NAME')  // Docker Hub username (Secret Text)
        DOCKER_PASS = credentials('DOCKER_PASS')  // Docker Hub password or token (Secret Text)
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

        stage('Login to Docker Hub') {
            steps {
                sh 'echo $DOCKER_PASS | docker login -u $DOCKER_NAME --password-stdin'
            }
        }

        stage('Push Docker Image') {
            steps {
                sh 'docker push $IMAGE_NAME:latest'
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
            echo 'Flask backend successfully built, pushed, and deployed.'
        }
        failure {
            echo 'Deployment failed. Check Jenkins logs.'
        }
    }
}