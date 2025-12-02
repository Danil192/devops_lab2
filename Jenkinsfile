pipeline {
    agent any

    stages {
        stage('Checkout SCM') {
            steps {
                checkout scm
            }
        }

        stage('Clean old containers') {
            steps {
                echo '=== Cleaning up old containers ==='
                bat 'docker-compose down --remove-orphans -v'
            }
        }

        stage('Build containers') {
            steps {
                echo '=== Building Docker images ==='
                bat 'docker-compose build'
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Starting containers (waiting for DB to be ready) ==='
                bat 'docker-compose up -d --build'
            }
        }

        stage('Test Flask app') {
            steps {
                echo '=== Waiting ~15 seconds for services to initialize ==='
                bat 'ping 127.0.0.1 -n 16 >nul'

                echo '=== Testing: data from PostgreSQL is displayed ==='
                bat '''
                    @echo off
                    set attempts=0
                    :retry
                    set /a attempts+=1
                    if %attempts% GTR 5 (
                        echo ERROR: Max retries exceeded.
                        curl -s http://localhost
                        exit /b 1
                    )

                    echo Attempt %attempts%...
                    curl -s http://localhost | findstr /I "PostgreSQL" >nul
                    if %ERRORLEVEL% EQU 0 (
                        echo SUCCESS: Data from database received!
                        exit /b 0
                    )

                    echo Data not found. Waiting 5 seconds...
                    ping 127.0.0.1 -n 6 >nul
                    goto retry
                '''
            }
        }

        stage('Deploy to C:\\deploy2') {
            steps {
                echo '=== Deploying to C:\\deploy2 ==='
                bat '''
                    if not exist "C:\\deploy2" mkdir "C:\\deploy2"
                    xcopy /E /Y /Q ".\\*" "C:\\deploy2\\"
                    echo Deployment completed.
                '''
            }
        }

        stage('Check running') {
            steps {
                echo '=== Checking if containers are running ==='
                bat 'docker-compose ps'
            }
        }
    }

    post {
        always {
            echo '✅ Pipeline finished.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}