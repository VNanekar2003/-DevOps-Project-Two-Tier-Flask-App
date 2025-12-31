pipeline {
    agent any

    stages {
        stage('Clone Code') {
            steps {
                git branch: 'master',
                    url: 'https://github.com/VNanekar2003/-DevOps-Project-Two-Tier-Flask-App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-app:latest .'
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                sh 'docker compose down || true'
                sh 'docker compose up -d --build'
            }
        }
    }
}
