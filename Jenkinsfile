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
                bat 'set PATH=%PATH%;C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\Scripts'  
                
                bat 'python --version'
                bat 'pip --version'
                
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
