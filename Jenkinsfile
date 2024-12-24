pipeline {
       agent any
       stages {
           stage('Checkout') {
               steps {
                   checkout scm
               }
           }
           stage('Build') {
               steps {
                   sh './build.sh'
               }
           }
           stage('Test') {
               steps {
                   sh 'pytest tests/'
               }
           }
           stage('Deploy') {
               steps {
                   sh './deploy.sh'
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