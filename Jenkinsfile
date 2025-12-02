pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "danil192/flask-web"  // Можно оставить, но не обязательно
    }

    stages {
        stage('Clean old containers') {
            steps {
                echo '=== Полная очистка: останавливаем и удаляем всё (контейнеры, тома, сеть) ==='
                bat '''
                    docker-compose down --remove-orphans -v
                '''
            }
        }

        stage('Build containers') {
            steps {
                echo '=== Собираем Docker-образы локально ==='
                bat 'docker-compose build'
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Запускаем свежие контейнеры ==='
                bat 'docker-compose up -d --build'
                sleep 15 // даём PostgreSQL время запуститься
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Проверяем Flask + БД через Nginx (порт 80) ==='
                bat '''
                    curl -s http://localhost | find "✅ Подключение к БД успешно"
                    if %ERRORLEVEL% NEQ 0 (
                        echo Тест не пройден! Ответ сервера:
                        curl -s http://localhost
                        exit /b 1
                    )
                '''
            }
        }

        stage('Deploy to C:\\deploy2') {
            steps {
                script {
                    echo '=== Копируем файлы в C:\\deploy2 ==='
                    bat """
                        if exist "C:\\deploy2" rmdir /s /q "C:\\deploy2"
                        mkdir "C:\\deploy2"
                        robocopy . "C:\\deploy2" /E /XD .git >nul
                        if %errorlevel% leq 1 exit 0
                        exit %errorlevel%
                    """
                }
            }
        }

        stage('Check running') {
            steps {
                bat 'docker ps'
            }
        }
    }

    post {
        success { echo '✅ CI/CD с БД и локальным деплоем в C:\\deploy2 завершён!' }
        failure { echo '❌ Ошибка в пайплайне' }
    }
}