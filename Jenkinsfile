// Jenkinsfile (Declarative Pipeline)
pipeline {
    agent any
    environment {
        // REPLACE with your Docker Hub Username
        DOCKER_HUB_USERNAME = 'vanshpnsuriya'
        IMAGE_NAME = "flask-ci-cd-app"
        TAG_NAME = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker Image...'
                script {
                    sh "docker build -t ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:${env.TAG_NAME} ."
                    sh "docker build -t ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:latest ."
                }
            }
        }
        stage('Run Container Tests') {
            steps {
                echo 'Running a quick container test...'
                script {
                    sh "docker run --rm -d --name test-flask ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:${env.TAG_NAME}"
                    sh "sleep 5"
                    sh "docker logs test-flask"
                    sh "docker stop test-flask"
                }
            }
        }
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-cred', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:${env.TAG_NAME}"
                        sh "docker push ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:latest"
                    }
                }
            }
        }
        stage('Deploy Application') {
            steps {
                echo 'Deploying application to local machine (re-deploying latest container)...'
                script {
                    sh 'docker stop flask-prod-app || true'
                    sh 'docker rm flask-prod-app || true'
                    sh """
                        docker run -d \\
                        -p 8000:5000 \\
                        --name flask-prod-app \\
                        ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:latest
                    """
                    echo "Deployment successful! Check http://localhost:8000"
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline finished! Status: ${currentBuild.result}"
        }
    }
}
