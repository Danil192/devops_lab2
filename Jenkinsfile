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
                bat '''
                    docker-compose down --remove-orphans -v
                '''
            }
        }

        stage('Build containers') {
            steps {
                echo '=== Building Docker images ==='
                bat '''
                    docker-compose build
                '''
            }
        }

        stage('Run containers') {
            steps {
                echo '=== Starting containers (waiting for DB to be ready) ==='
                bat '''
                    docker-compose up -d --build
                '''
            }
        }

stage('Test Flask app') {
    steps {
        echo '=== Waiting for app to be ready ==='
        bat 'timeout /t 15 /nobreak >nul'
        echo '=== Testing: data from PostgreSQL is displayed ==='
        bat '''
            curl -s http://localhost | findstr /I "PostgreSQL"
            if %ERRORLEVEL% EQU 0 (
                echo SUCCESS: Data from database received!
            ) else (
                echo ERROR: Data not found.
                curl -s http://localhost
                exit /b 1
            )
        '''
    }
}

        stage('Deploy to C:\\deploy2') {
            steps {
                echo '=== Deploying to C:\\deploy2 ==='
                bat '''
                    mkdir -p C:\\deploy2
                    copy .\\* C:\\deploy2\\
                    echo Deployment completed.
                '''
            }
        }

        stage('Check running') {
            steps {
                echo '=== Checking if containers are running ==='
                bat '''
                    docker-compose ps
                '''
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