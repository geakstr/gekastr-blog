Title: Грамотно собираем и конфигурируем nginx
Date: 2015-08-26 17:00
Tags: nginx, nix
Slug: nginx-setup
Status: published

В данной заметке я покажу как скомпилировать nginx из исходников с необходимыми модулями, а также довольно тонко настроить параметры сервера. Некоторые вещи в конфиге специфичны и подойдут далеко не для всех задач, так что аккуратно и внимательно с этапом настройки. Эта конфигурация хорошо подойдет для использования на Raspberry Pi. 

Получим рута, доставим необходимые для сборки пакеты и создадим файл скрипта:
    
    #!bash
    su root
    apt-get -y install curl wget build-essential libz-dev libssl-dev
    nano /tmp/build_nginx.sh

Тело скрипта: 

    #!bash
    #!/usr/bin/env bash

    # Почти полная копия скрипта https://gist.github.com/MattWilcox/402e2e8aa2e1c132ee24
    # с некоторыми модификациями

    export VERSION_PCRE=pcre-8.37
    # Посмотрите номер последней версии openssl здесь https://www.openssl.org/news/changelog.html
    export VERSION_OPENSSL=openssl-1.0.2d
    # Номер последней версии nginx здесь http://nginx.org/en/download.html
    export VERSION_NGINX=nginx-1.9.7

    # Адреса откуда качать исходники
    export SOURCE_OPENSSL=https://www.openssl.org/source/
    export SOURCE_PCRE=ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
    export SOURCE_NGINX=http://nginx.org/download/

    # Переменная с датой для бекапа текущих настроек nginx
    today=$(date +"%Y-%m-%d")

    # Почистим директории, которые могли остаться после предыдущего запуска скрипта
    rm -rf build
    rm -rf /etc/nginx-default
    mkdir build
    
    # Качаем исходники
    wget -P ./build $SOURCE_PCRE$VERSION_PCRE.tar.gz
    wget -P ./build $SOURCE_OPENSSL$VERSION_OPENSSL.tar.gz --no-check-certificate
    wget -P ./build $SOURCE_NGINX$VERSION_NGINX.tar.gz

    # Разархивируем их
    cd build
    tar xzf $VERSION_NGINX.tar.gz
    tar xzf $VERSION_OPENSSL.tar.gz
    tar xzf $VERSION_PCRE.tar.gz
    cd ../

    # Указываем директории, в которых будем компилить nginx и openssl
    export BPATH=$(pwd)/build
    export STATICLIBSSL="$BPATH/staticlibssl"

    # Компилим openssl
    cd $BPATH/$VERSION_OPENSSL
    rm -rf "$STATICLIBSSL"
    mkdir "$STATICLIBSSL"
    make clean
    ./config --prefix=$STATICLIBSSL no-shared \\
    && make depend \\
    && make \\
    && make install_sw

    # Бекапим текущие исходники nginx
    mv /etc/nginx /etc/nginx-$today

    # Собираем nginx
    # Указан небольшой перечень модулей. Если вам нужны дополнительные, список можно посмотреть здесь
    # http://wiki.nginx.org/Modules
    cd $BPATH/$VERSION_NGINX
    mkdir -p $BPATH/nginx
    ./configure --with-cc-opt="-I $STATICLIBSSL/include -I/usr/include" \\
    --with-ld-opt="-L $STATICLIBSSL/lib -Wl,-rpath=$STATICLIBSSL/lib -lssl -lcrypto -ldl -lz" \\
    --sbin-path=/usr/sbin/nginx \\
    --conf-path=/etc/nginx/nginx.conf \\
    --pid-path=/var/run/nginx.pid \\
    --error-log-path=/var/log/nginx/error.log \\
    --http-log-path=/var/log/nginx/access.log \\
    --with-pcre=$BPATH/$VERSION_PCRE \\
    --with-http_ssl_module \\
    --with-file-aio \\
    --with-http_gzip_static_module \\
    --without-mail_pop3_module \\
    --without-mail_smtp_module \\
    --without-mail_imap_module \\
    && make && make install

    # Переименуем директорию с новыми дефолтными конфигами
    mv /etc/nginx /etc/nginx-default

    # Вернем конфиги из бекапа
    mv /etc/nginx-$today /etc/nginx

Запустим процесс компиляции и пойдем пить чай. Много чая.

    #!bash
    chmod +x /tmp/build_nginx.sh && /tmp/build_nginx.sh

Если ранее уже был установлен nginx, скрипт вернул старые конфиги и все продолжит работать как раньше. Если нет, подготовимся к его настройке:

    #!bash
    # Создадим пользователя, от которого будет запускаться nginx
    useradd nginx
    groupadd nginx
    usermod -g nginx -G www-data nginx

    # И директорию для сайтов
    mkdir /var/www
    chmod -R 775 /var/www
    chown -R www-data:www-data /var/www

Приступим к конфигурированию:

    #!bash
    # Скопируем дефолтные конфиги
    cp -R /etc/nginx-default /etc/nginx

    # И начнем править
    nano /etc/nginx/nginx.conf

Удалим все из конфига и создадим такой:

    #!nginx
    # Пользователь, от которого будет запускаться nginx
    user              nginx;

    # Рекомендуется выставлять по количеству ядер в системе
    # Можно узнать командой nproc
    worker_processes  1;

    # Путь до файла с логами ошибок
    error_log  /var/log/nginx/error.log warn;

    # Здесь будет храниться id процесса nginx
    pid        /var/run/nginx.pid;

    events {
      # Говорит, сколько коннектов может обрабатывать 1 процесс
      # Число можно узнать командой ulimit -n
      worker_connections  1024;
    }

    http {
      # Дополнительную информацию можно получить тут
      # http://nginx.org/ru/docs/http/ngx_http_core_module.html

      # Соответствие MIME типов файлов их расширениям
      include       /etc/nginx/mime.types;
      # Тип по умолчанию — бинарный файл без формата
      default_type  application/octet-stream;

      # Лог файл, где будут храниться логи доступа к ресурсам сайта
      access_log /var/log/nginx/access.log;

      # Если вам это неважно, можно отключить ведение этих логов
      #access_log  off;

      # Отдаем файлы напрямую, без лишего копирования веб-сервером
      sendfile     on;
      # Выводим данные полными пакетами 
      tcp_nopush   on;
      # Убираем задержку при передаче последнего пакета, если соединение не закрывается
      tcp_nodelay  on;
      # Для отдачи относительно больших файлов,
      # будем использовать прямое чтение, без обращения в кэш ОС
      directio     5m;

      # Настройки в секции позволяют повысить производительность
      # При неожиданном поведении, следует увеличить числа
      # Снизим таймаут отдачи body клиенту
      client_body_timeout    10;
      # Снизим таймаут отдачи заголовков клиенту 
      client_header_timeout  10;
      # Установим время жизни соединения клиента, а также будем возвращать соответствующий заголовок
      keepalive_timeout      5 5;
      # Установим время ожидания ответа клиенту
      send_timeout           10;

      # Секция позволяет снизить вред от атаки типа "переполнение буфера"
      # Нужно быть аккуратнее с числами, иначе можно столкнуться с неожиданным поведением
      # Размер буфера для body запроса клиента
      client_body_buffer_size      1K;
      # Размер буфера для заголовка запроса клиента
      # Нужно увеличить размер, если собираемся принимать кастомные заголовки или большие куки
      client_header_buffer_size    1k;
      # Если не будем поддерживать загрузку файлов через POST, установим максимальный размер body
      client_max_body_size         1k;
      # Установим максимальное количество и размер этих буферов для чтения заголовков клиента
      large_client_header_buffers  2 1k;

      # Не посылать номер версии nginx в заголовках
      server_tokens  off;
      # Запретить помещать наши страницы во фреймы
      add_header     X-Frame-Options SAMEORIGIN;
      # Отключаем content-type sniffing 
      # https://www.owasp.org/index.php/List_of_useful_HTTP_headers
      add_header     X-Content-Type-Options nosniff;
      # Включаем XSS фильтер в браузерах
      add_header     X-XSS-Protection "1; mode=block";

      # Включаем сжатие трафика
      # http://nginx.org/ru/docs/http/ngx_http_gzip_module.html
      gzip               on; 
      # Разрешаем сжатие трафика для всех проксированных запросов
      gzip_proxied       any;
      # Устанавливаем минимальную длину ответа, при которой нужно применять сжатие
      gzip_min_length    1000;
      # Минимальная версия http для запроса, начиная с которой нужно применять сжатие
      gzip_http_version  1.0;
      # Число и размер буферов, в которые будет сжиматься ответ
      gzip_buffers       16 8k;
      # Уровень компрессии
      gzip_comp_level    4;
      # MIME-типы, для которых применять сжатие
      gzip_types         text/plain text/css application/json text/javascript application/x-javascript text/xml application/xml application/xml+rss;

      # Подключаем дополнительные конфиги с хостами
      include /etc/nginx/conf.d/*.conf;
    }

Теперь создадим хост:

    #!bash
    mkdir /etc/nginx/conf.d && nano /etc/nginx/conf.d/home.conf

Пример конфига для отдачи статики:

    #!nginx
    server {
        listen       80;
        server_name  localhost;

        # По умолчанию будем искать файл index.html
        index index.html;

        # Путь до корня хоста в файловой системы
        root /var/www;

        # Удаляем .html из адреса
        rewrite ^(/.+)\.html$ $scheme://$host$1 permanent;

        # Пути до кастомных страниц с ошибками
        error_page 404 /404.html;
        error_page 500 502 503 504 /50x.html;

        location / {
            # Удаляем /index для директорий
            rewrite ^/(.*)/index$ /$1 permanent;

            # $uri/index.html для отдачи index.html из директории
            # $uri.html для отдачи .html файлов
            # $uri во всех остальных случаях будет искать файлы по имени как есть
            try_files $uri/index.html $uri.html $uri =404;
        }
    }

Добавим в автозагрузку скрипт управления демоном nginx:

    #!bash
    nano /lib/systemd/system/nginx.service

Вставим туда следующее:

    #!bash
    [Unit]
    Description=The NGINX HTTP and reverse proxy server
    After=syslog.target network.target remote-fs.target nss-lookup.target

    [Service]
    Type=forking
    PIDFile=/run/nginx.pid
    ExecStartPre=/usr/sbin/nginx -t
    ExecStart=/usr/sbin/nginx
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s QUIT $MAINPID
    PrivateTmp=true

    [Install]
    WantedBy=multi-user.target

И инициализируем:

    #!bash
    systemctl daemon-reload
    systemctl enable nginx.service
    systemctl start nginx.service