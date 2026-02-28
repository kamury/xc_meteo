import os
import logging
from flask import Flask

def setup_logger(app: Flask):
    """
    Настраивает логирование для Flask приложения.
    Создает папку для логов, если её нет, и добавляет файловый обработчик.
    """
    # Определяем, где будут храниться логи
    log_dir = 'logs'
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Путь к файлу с логами
    log_file = os.path.join(log_dir, 'app.log')
    
    # Создаем обработчик для записи в файл
    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    
     # Задаем формат логов
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # Устанавливаем уровень логирования
    file_handler.setLevel(logging.INFO)
    
    # Добавляем обработчик к логгеру Flask
    app.logger.addHandler(file_handler)

     # Устанавливаем уровень логирования для приложения
    app.logger.setLevel(logging.INFO)
    
    return app.logger

def get_logger(app: Flask):
    """
    Возвращает настроенный логгер приложения.
    Удобно использовать в других модулях.
    """
    return app.logger