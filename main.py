from app import app, logger

if __name__ == '__main__':
    logger.info('Start service')
    app.run(debug=True)
