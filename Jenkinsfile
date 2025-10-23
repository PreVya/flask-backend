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
        stage('Restart App (Final Deployment)') {
            steps {
                sh '''#!/bin/bash
                # 1. Setup PATH and Environment
                export PATH=/var/lib/jenkins/.local/bin:$PATH
                export MONGO_URL="${MONGO_URL}"
                LOG_FILE="$WORKSPACE/flask.log"

                # 2. Kill existing process gracefully
                echo "Stopping existing gunicorn process..."
                pkill -f 'gunicorn.*0.0.0.0:5000' || true
                sleep 3 # Longer wait for shutdown

                # 3. Start Gunicorn with Double-Forking/Disown for Persistence
                echo "Starting gunicorn on 0.0.0.0:5000 persistently..."
                (
                    # Run nohup in a subshell, redirecting all output to the log file
                    nohup /usr/bin/python3 -m gunicorn -w 4 -b 0.0.0.0:5000 app:app > "$LOG_FILE" 2>&1 &
                )
                # Disown removes the process from the current shell's job control
                # This must be run immediately after the subshell starts.
                disown
                
                # 4. Verification and Final Check
                sleep 5
                
                if ! pgrep -f 'gunicorn.*0.0.0.0:5000' ; then
                    echo "ERROR: Gunicorn failed to start and stay running after disown."
                    echo "Last 20 lines of log file:"
                    tail -n 20 "$LOG_FILE"
                    exit 1
                else
                    echo "SUCCESS: Gunicorn is running persistently in the background."
                    echo "Check the host machine for port 5000 binding (sudo ss -tulpn | grep 5000)."
                fi
                '''
            }
        }
  
    }
}
