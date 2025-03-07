build:
        docker build -t flask-app:latest .

run:
        docker run -p 5000:5000 flask-app:latest

test:
        pytest --cov=app tests/

format:
        black app/ tests/

lint:
        pylint app/ tests/