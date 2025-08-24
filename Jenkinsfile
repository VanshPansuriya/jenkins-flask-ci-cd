// Jenkinsfile (Declarative Pipeline)
pipeline {
    // Define the agent where the pipeline will run (in this case, on the Jenkins controller)
    agent any

    // Define environment variables
    environment {
        // REPLACE with your Docker Hub Username
        DOCKER_HUB_USERNAME = 'your-dockerhub-username'
        // Define the image name (unique for marks)
        IMAGE_NAME = "flask-ci-cd-app"
        // Use a unique tag for the build
        TAG_NAME = "${env.BUILD_NUMBER}"
    }

    // Stages of the CI/CD Pipeline
    stages {
        // 1. Stage: Build
        stage('Build Docker Image') {
            steps {
                echo 'Building the Docker Image...'
                // Use the Docker tool to build the image
                // t: tag the image with the username/image-name:build-number
                script {
                    sh "docker build -t ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:${env.TAG_NAME} ."
                    sh "docker build -t ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:latest ." // Also tag as 'latest'
                }
            }
        }

        // 2. Stage: Test
        stage('Run Container Tests') {
            steps {
                echo 'Running a quick container test...'
                // Run the built image in a temporary container and verify it starts
                script {
                    sh "docker run --rm -d --name test-flask ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:${env.TAG_NAME}"
                    // Wait for a few seconds for the app to start
                    sh "sleep 5"
                    // Try to access the app's output (optional, but good for real projects)
                    // This is a placeholder for a more complex test
                    sh "docker logs test-flask"
                    sh "docker stop test-flask"
                }
            }
        }

        // 3. Stage: Push
        stage('Push to Docker Hub') {
            steps {
                echo 'Pushing image to Docker Hub...'
                script {
                    // Authenticate with Docker Hub using the credentials ID defined earlier
                    // The 'withCredentials' block securely exposes the credentials
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:${env.TAG_NAME}"
                        sh "docker push ${env.DOCKER_HUB_USERNAME}/${env.IMAGE_NAME}:latest"
                    }
                }
            }
        }

        // 4. Stage: Deployment
        stage('Deploy Application') {
            steps {
                echo 'Deploying application to local machine (re-deploying latest container)...'
                script {
                    // Stop and remove any previous running container with the same name
                    sh 'docker stop flask-prod-app || true'
                    sh 'docker rm flask-prod-app || true'

                    // Run the container from the newly pushed 'latest' image
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
    // Post-actions (e.g., send email notification)
    post {
        always {
            echo "Pipeline finished! Status: ${currentBuild.result}"
        }
    }
}