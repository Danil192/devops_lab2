pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "danil192/flask-web"
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
                echo '=== Собираем Docker-образ ==='
                bat 'docker-compose build'
                bat "docker build -t ${env.DOCKER_IMAGE} ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo '=== Публикуем образ на Docker Hub ==='
                    withCredentials([usernamePassword(
                        credentialsId: 'docker-hub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        bat """
                            echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin
                            docker push ${env.DOCKER_IMAGE}
                            docker logout
                        """
                    }
                }
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Запускаем свежие контейнеры ==='
                // --build гарантирует, что будет использована новая сборка
                bat 'docker-compose up -d --build'
                sleep 10
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Проверяем Flask + БД через Nginx (порт 80) ==='
                bat '''
                    curl -s http://localhost | find "✅ Подключение к БД успешно"
                    if %ERRORLEVEL% NEQ 0 (
                        echo Тест не пройден!
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
        success { echo '✅ CI/CD с БД, Docker Hub и деплоем в C:\\deploy2 завершён!' }
        failure { echo '❌ Ошибка в пайплайне' }
    }
}