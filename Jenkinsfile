pipeline {
    agent any
    
    environment {
        GITHUB_CREDENTIALS = credentials('my-repo-credentials')  
    }
    
    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'my-repo-credentials', url: 'https://github.com/yeshalkhan/EMS'
            }
        }
        
        stage('Build') {
            steps {
                sh './build.sh'
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
