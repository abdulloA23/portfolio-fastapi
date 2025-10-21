FROM php:8.2-fpm

# Установка Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libpng-dev \
    libonig-dev \
    libxml2-dev \
    libzip-dev \
    libpq-dev \
    zip \
    unzip \
    nginx \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Установка PHP расширений
RUN docker-php-ext-install \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    mbstring \
    exif \
    pcntl \
    bcmath \
    gd \
    zip

# Установка Composer
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Рабочая директория
WORKDIR /var/www

# Копирование composer файлов сначала (для кэширования слоев)
COPY composer.json composer.lock ./

# Установка зависимостей
RUN composer install --no-scripts --no-autoloader --no-dev

# Копирование package.json и package-lock.json
COPY package*.json ./

# Установка npm зависимостей
RUN npm ci

# Копирование остальных файлов проекта
COPY . .

# Сборка фронтенда
RUN npm run build

# Завершение установки Composer
RUN composer dump-autoload --optimize --no-dev

# Создание директории для SQLite и файла БД
RUN mkdir -p /var/www/database && \
    touch /var/www/database/database.sqlite

# Настройка прав
RUN chown -R www-data:www-data \
    /var/www/storage \
    /var/www/bootstrap/cache \
    /var/www/database

# Копирование конфигурации Nginx
COPY docker/nginx.conf /etc/nginx/sites-available/default

# Скрипт запуска
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8080

CMD ["/start.sh"]
