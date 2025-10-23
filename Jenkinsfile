pipeline {
    agent any

    environment {
        PYTHON = "/usr/bin/python3"
        MONGO_URL = credentials('MONGO_URL')  
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

        // stage('Restart App') {
        //     steps {
        //         sh '''
        //         export PATH=/var/lib/jenkins/.local/bin:$PATH
        //         export MONGO_URL="${MONGO_URL}"

       
        //         mkdir -p /home/ubuntu/flask-backend
        //         cp -r * /home/ubuntu/flask-backend/
        //         cd /home/ubuntu/flask-backend

        
        //         pkill -f 'gunicorn' || true

        
        //         nohup /usr/bin/python3 -m gunicorn -w 4 -b 0.0.0.0:5000 app:app > flask.log 2>&1 & 

        //         sleep 5
        //         tail -n 200 flask.log
        //         '''
        //     }
     
        // }
        stage('Restart App (Persistent)') {
            steps {
                sh '''
                    # 1. Ensure the Jenkins user's local bin directory is in PATH
                export PATH=/var/lib/jenkins/.local/bin:$PATH

                # 2. Export the credential to the current shell environment
                export MONGO_URL="${MONGO_URL}"

                # 3. Change to the workspace directory
                cd $WORKSPACE

                # 4. Gracefully kill any existing gunicorn processes for cleanup
                pkill -f 'gunicorn' || true
                sleep 2 # Give it time to shut down

                # 5. Start gunicorn using nohup, redirecting output to a log file, and running in the background (&)
                # nohup prevents the process from being killed when the controlling terminal (Jenkins shell) is closed.
                nohup /usr/bin/python3 -m gunicorn -w 4 -b 0.0.0.0:5000 app:app > flask.log 2>&1 &
                
                # 6. Wait a bit for the app to start and check logs for verification
                sleep 5
                tail -n 20 flask.log
                '''
            }
        } 
  
    }
}
