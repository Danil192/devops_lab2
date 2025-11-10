pipeline {
    agent any

    stages {
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
                echo '=== Останавливаем контейнеры ==='
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
