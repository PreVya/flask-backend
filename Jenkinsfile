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
        stage('Restart App (Hardened Persistence)') {
            steps {
                // Use 'sh returnStdout: true, script: '...' to capture output 
                // OR explicitly specify the shell for the step.
                // However, the simplest fix is to use the shebang line.
                
                sh '''#!/bin/bash
                # 1. Ensure the Jenkins user's local bin directory is in PATH
                export PATH=/var/lib/jenkins/.local/bin:$PATH

                # 2. Export the credential to the current shell environment
                export MONGO_URL="${MONGO_URL}"

                # 3. Gracefully kill any existing gunicorn process.
                pkill -f 'gunicorn.*0.0.0.0:5000' || true
                sleep 2

                # 4. Set the log file path clearly
                LOG_FILE="$WORKSPACE/flask.log"
                
                # 5. Start gunicorn using the double-forking technique in BASH
                # The 'nohup' and '&' run the process, and 'disown' removes it from job control.
                (
                    nohup /usr/bin/python3 -m gunicorn -w 4 -b 0.0.0.0:5000 app:app > "$LOG_FILE" 2>&1
                ) &
                disown
                
                # 6. Wait a bit for the app to start and check process
                sleep 5
                
                # 7. Check if the process is actually running
                if ! pgrep -f 'gunicorn.*0.0.0.0:5000' ; then
                    echo "ERROR: Gunicorn process failed to start or shut down immediately."
                    echo "Checking last 20 lines of log file for errors:"
                    tail -n 20 "$LOG_FILE"
                    exit 1
                else
                    echo "SUCCESS: Gunicorn process started successfully. Running on 0.0.0.0:5000."
                    echo "Last 20 lines of log file:"
                    tail -n 20 "$LOG_FILE"
                fi
                '''
            }
        }
  
    }
}
