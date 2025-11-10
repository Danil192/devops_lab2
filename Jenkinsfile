pipeline {
    agent any

    stages {
        stage('Build containers') {
            steps {
                echo '=== Собираем контейнеры ==='
                sh 'docker-compose build'
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Запускаем контейнеры ==='
                sh 'docker-compose up -d'
            }
        }

        stage('Check running containers') {
            steps {
                echo '=== Проверяем запущенные контейнеры ==='
                sh 'docker ps -a'
            }
        }

        stage('Stop containers') {
            steps {
                echo '=== Останавливаем контейнеры ==='
                sh 'docker-compose down'
            }
        }
    }

    post {
        success {
            echo '✅ Пайплайн выполнен успешно!'
        }
        failure {
            echo '❌ Что-то пошло не так, проверь лог пайплайна.'
        }
    }
}
