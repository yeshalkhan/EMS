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
                // Add Python and Scripts directory to PATH
                bat '''set PATH=%PATH%;C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37;C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\Scripts'''
                
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
