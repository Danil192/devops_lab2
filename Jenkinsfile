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
                echo 'Ждём, пока Flask поднимется...'
                sleep 10
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Проверяем доступность Flask приложения ==='
                sh '''
                    echo "Отправляем запрос на localhost:5000"
                    if curl -s --head --request GET http://localhost:5000 | grep "200 OK" > /dev/null; then
                        echo "Flask отвечает нормально!"
                    else
                        echo "Flask не отвечает!"; exit 1
                    fi
                '''
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
            echo 'Пайплайн выполнен успешно, Flask работает!'
        }
        failure {
            echo 'Ошибка при сборке или тестировании. Проверь логи пайплайна.'
        }
    }
}
