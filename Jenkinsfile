// use of pipeline structure & format from Yaniv's repo
pipeline {
    agent any

    environment {
        IMAGE_NAME = "sharonshaked/builder"
        IMAGE_TAG  = "1.0.${BUILD_NUMBER}"
    }

    stages {
        // pull code from my github repo
        stage('Clone') {
            steps {
                git branch: 'feature/docker', url: 'https://github.com/shaked-sharon/devops-aws-terraform.git'
            }
        }

        // build docker image using dockerfile
        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG .'
            }
        }

        // run container > make sure > works
        stage('Run') {
            steps {
                sh 'docker run --rm $IMAGE_NAME:$IMAGE_TAG'
            }
        }

        // push image > docker hub
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh 'docker push $IMAGE_NAME:$IMAGE_TAG'
                }
            }
        }
    }

    // cleanup after pipeline completetion
    post {
        always {
            sh 'docker rmi $IMAGE_NAME:$IMAGE_TAG || true'
        }
    }
}