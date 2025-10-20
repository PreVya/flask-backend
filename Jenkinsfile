pipeline {
    agent any

    environment {
        PYTHON = "/usr/bin/python3"
        MONGO_URL = credentials('MONGO_URL')  // Jenkins secret ID
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/PreVya/flask-backend.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh "${env.PYTHON} -m pip install --upgrade pip"
                sh "${env.PYTHON} -m pip install -r requirements.txt"
            }
        }

        stage('Set Environment') {
            steps {
                // Write MONGO_URL to .env so Flask app can read it
                sh """
                echo MONGO_URL=\"${MONGO_URL}\" > .env
                """
            }
        }

        stage('Restart App') {
            steps {
                // Restart Flask app using PM2
                sh "pm2 restart flask-app || pm2 start app.py --name flask-app"
            }
        }
    }
}
