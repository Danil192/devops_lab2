pipeline {
    agent any

    stages {
        stage('Clean old containers') {
            steps {
                echo '=== Удаляем старые контейнеры, если остались ==='
                bat '''
                    docker ps -a
                    docker rm -f flask_web || echo "flask_web не найден"
                    docker rm -f postgres_db || echo "postgres_db не найден"
                '''
            }
        }

        stage('Build containers') {
            steps {
                echo '=== Собираем контейнеры ==='
                bat 'docker-compose build'
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Запускаем контейнеры ==='
                bat 'docker-compose up -d'
                echo 'Ждём, пока Flask поднимется...'
                sleep 10
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Проверяем доступность Flask приложения ==='
                bat '''
                    echo Отправляем запрос на localhost:5000
                    curl -s --head http://localhost:5000 | find "200 OK"
                    if %ERRORLEVEL%==0 (
                        echo Flask отвечает нормально!
                    ) else (
                        echo Flask не отвечает!
                        exit /b 1
                    )
                '''
            }
        }

        stage('Check running containers') {
            steps {
                echo '=== Проверяем запущенные контейнеры ==='
                bat 'docker ps -a'
            }
        }

        stage('Stop containers') {
            steps {
                echo '=== Останавливаем контейнеры и очищаем окружение ==='
                bat 'docker-compose down'
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
