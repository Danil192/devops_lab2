pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = 1
    }

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
                echo '=== Проверяем, что контейнеры запущены ==='
                sh 'docker ps -a'
            }
        }

        stage('Stop containers') {
            steps {
                echo '=== Останавливаем и очищаем окружение ==='
                sh 'docker-compose down'
            }
        }
    }

    post {
        success {
            echo 'Сборка и запуск контейнеров завершены успешно!'
        }
        failure {
            echo 'Что-то пошло не так, проверь лог пайплайна.'
        }
    }
}
