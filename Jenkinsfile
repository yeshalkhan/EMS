pipeline {
    agent any

    environment {
        GITHUB_CREDENTIALS = credentials('my-repo-credentials')
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'my-repo-credentials', url: 'https://github.com/yeshalkhan/EMS', branch: 'main'
            }
        }

        stage('Build') {
            steps {
                // Directly use the full path for python and pip
                bat '''"C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\python.exe" --version'''
                bat '''"C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\Scripts\\pip.exe" --version'''

                // Install dependencies using the absolute path for pip
                bat '''"C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\Scripts\\pip.exe" install -r requirements.txt'''
                
                // Run the build script
                bat './build.bat'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished!'
        }
        success {
            echo 'Build, Test, and Deployment Successful!'
        }
        failure {
            echo 'An error occurred during execution.'
        }
    }
}
