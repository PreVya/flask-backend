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
        stage('Restart App (Crash Diagnosis)') {
            steps {
                sh '''#!/bin/bash
                export PATH=/var/lib/jenkins/.local/bin:$PATH
                export MONGO_URL="${MONGO_URL}"

                # 1. Gracefully kill any existing process
                pkill -f 'gunicorn.*0.0.0.0:5000' || true
                sleep 2

                # 2. Start Gunicorn in the foreground for a short duration
                # Use --log-level debug to get maximum startup info
                # The 'timeout' command will run gunicorn for 10 seconds and then kill it,
                # ensuring the stage doesn't hang and capturing all logs.
                echo "--- Attempting Foreground Start for Diagnosis (10s Timeout) ---"
                
                # Run Gunicorn in a subshell with a timeout
                # Note: This will likely fail the build, which is what we want for diagnosis.
                timeout 10 /usr/bin/python3 -m gunicorn -w 4 -b 0.0.0.0:5000 app:app --log-level debug
                
                # Check the exit status of the timeout command
                if [ $? -eq 124 ]; then
                    echo "Gunicorn ran for the full 10 seconds. App is likely stable."
                else
                    echo "Gunicorn process terminated prematurely within 10 seconds! CHECK THE ABOVE LOGS FOR THE TRACEBACK (PYTHON ERROR)."
                fi

                echo "--- END DIAGNOSIS ---"
                '''
            }
        }
  
    }
}
