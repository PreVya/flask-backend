// We define the MONGO_URL variable inside the credential block for secure passing.
// The variable definition is removed to fix the Groovy scoping error.
// The literal string 'MONGO_URL' will be used directly in the withCredentials step.

pipeline {
    agent any
    
    environment {
        // Set the path to the main workspace directory for reference
        APP_ROOT = "${WORKSPACE}"
        # Path to where pip installs local executables (gunicorn)
        JENKINS_LOCAL_BIN = "/var/lib/jenkins/.local/bin"
    }

    stages {
        stage('Declarative: Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Checkout') {
            steps {
                // Ensure we are in the correct directory for the app code
                git branch: 'main', credentialsId: '', url: 'https://github.com/PreVya/flask-backend.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies (using --break-system-packages for modern Python versions)'
                sh "sudo /usr/bin/python3 -m pip install --upgrade pip --break-system-packages"
                sh "sudo /usr/bin/python3 -m pip install -r requirements.txt --break-system-packages"
            }
        }

        stage('Systemd Deployment & Restart') {
            steps {
                script { 
                    // Use withCredentials to access the secret securely.
                    // The credential ID is now hardcoded as a string constant to resolve the scoping issue.
                    withCredentials([string(credentialsId: 'MONGO_URL', variable: 'SECRET_MONGO_URL')]) {
                        
                        // 1. Create the .env file (Optional, but good practice for local debugging)
                        sh "echo MONGO_URL=\"${SECRET_MONGO_URL}\" > .env"

                        // --- FIX APPLIED HERE: Replacing complex Groovy string with a Here Document ---

                        // 2. Define the Systemd Service Content and write it using a Here Document
                        echo 'Creating /etc/systemd/system/flask.service file using Here Document...'
                        sh """
                        # Use a Here Document (EOF) with sudo tee to write the entire file reliably
                        # This avoids shell quoting issues when injecting multi-line content.
                        sudo tee /etc/systemd/system/flask.service > /dev/null <<EOF
[Unit]
Description=Flask Gunicorn Application deployed by Jenkins
After=network.target

[Service]
# Set the current Jenkins workspace as the application's working directory
WorkingDirectory=${env.APP_ROOT}

# The user running the service MUST be the user who installed the Python packages
User=jenkins 
Group=nogroup 

# Set the necessary environment variables for the service
Environment="PATH=${env.JENKINS_LOCAL_BIN}:/usr/bin"
Environment="MONGO_URL=${SECRET_MONGO_URL}"

# The ExecStart command uses the full path to python3
ExecStart=/usr/bin/python3 -m gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF
                        """
                        
                        // 3. Execute Systemctl Commands (Requires SUDO permissions set up)
                        echo 'Reloading systemd, enabling, and restarting the service...'
                        sh '''
                        # Reload daemon to pick up the new file
                        sudo systemctl daemon-reload
                        # Enable the service to run on boot (idempotent)
                        sudo systemctl enable flask
                        # Restart the service immediately
                        sudo systemctl restart flask
                        
                        sleep 5
                        
                        // 4. Final Verification Check
                        echo "--- Service Status Check (Journal output will be available via 'sudo journalctl -u flask') ---"
                        sudo systemctl status flask --no-pager || true // Allow status check to fail without failing the job

                        echo "--- Port Binding Check ---"
                        // Check the port binding directly
                        sudo ss -tulpn | grep 5000 || echo "Port 5000 is NOT bound (Check journal logs for application errors!)"
                        '''
                    }
                }
            }
        }
    }
}
