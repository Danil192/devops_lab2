pipeline {
    agent any

    stages {
        stage('Clean old containers') {
            steps {
                echo '=== Полная очистка ==='
                bat 'docker-compose down --remove-orphans -v'
            }
        }

        stage('Build containers') {
            steps {
                echo '=== Сборка образов ==='
                bat 'docker-compose build'
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Запуск контейнеров (ждём готовности БД автоматически) ==='
                bat 'docker-compose up -d --build'
                // Больше не нужно sleep — depends_on + healthcheck всё решают
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Проверка: данные из PostgreSQL отображаются ==='
                bat '''
                    curl -s http://localhost | findstr /C:"Привет из PostgreSQL!" >nul
                    if %ERRORLEVEL% EQU 0 (
                        echo Успех: данные из БД получены!
                    ) else (
                        echo ОШИБКА: данные не найдены.
                        curl -s http://localhost
                        exit /b 1
                    )
                '''
            }
        }

        stage('Deploy to C:\\deploy2') {
            steps {
                script {
                    echo '=== Копирование в C:\\deploy2 ==='
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
        success { echo '✅ CI/CD успешно завершён!' }
        failure { echo '❌ Ошибка в пайплайне' }
    }
}