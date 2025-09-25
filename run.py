from src.app import create_app
from utils import prepare_database

app = create_app('data-metrics')
prepare_database()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9292, debug=True)
