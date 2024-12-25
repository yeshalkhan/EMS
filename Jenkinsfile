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
                bat '"C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\python.exe" --version'
                
                bat './build.bat'
            }
        }
	stage('Test') {
            steps {
                bat '"C:\\Users\\computer point\\AppData\\Local\\Programs\\Python\\Python37\\python.exe" -m pytest tests/'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished!'
        }
        success {
            echo 'Build and Test Successful!'
        }
        failure {
            echo 'An error occurred during execution.'
        }
    }
}
