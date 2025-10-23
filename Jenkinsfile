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
                sh "/usr/bin/python3 -m pip install --upgrade pip --break-system-packages"
                sh "/usr/bin/python3 -m pip install -r requirements.txt --break-system-packages"
            }
        }

        stage('Set Environment') {
            steps {
                sh """
                echo MONGO_URL=\"${MONGO_URL}\" > .env
                """
            }
        }

        stage('Restart App') {
            steps {
                sh """
                export PATH=/var/lib/jenkins/.local/bin:\$PATH
                export PYTHONPATH=/var/lib/jenkins/.local/lib/python3.12/site-packages
                export MONGO_URL=\"${MONGO_URL}\"
                pkill -f 'app.py' || true
                nohup /usr/bin/python3 app.py > flask.log 2>&1 &
                sleep 5
                tail -n 20 flask.log
            """
            }
        }
    }
}
