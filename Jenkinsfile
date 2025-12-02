pipeline {
    agent any

    stages {
        stage('Clean old containers') {
            steps {
                echo '=== Полная очистка: останавливаем и удаляем всё (контейнеры, тома, сеть) ==='
                bat 'docker-compose down --remove-orphans -v'
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
                sleep 15 // даём PostgreSQL время инициализироваться
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Проверяем, что Flask отображает данные из PostgreSQL ==='
                bat '''
                    curl -s http://localhost | findstr /C:"Привет из PostgreSQL" >nul
                    if %ERRORLEVEL% EQU 0 (
                        echo Успех: данные из базы отображаются!
                    ) else (
                        echo ОШИБКА: данные из БД не найдены. Ответ сервера:
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
                echo '=== Текущие запущенные контейнеры ==='
                bat 'docker ps'
            }
        }
    }

    post {
        success {
            echo '✅ CI/CD успешно завершён: Flask + PostgreSQL работают, файлы скопированы в C:\\deploy2'
        }
        failure {
            echo '❌ Пайплайн завершился с ошибкой'
        }
    }
}