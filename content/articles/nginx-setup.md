Title: Установка и настройка nginx
Date: 2012-08-24 12:51
Tags: nginx, nix
Slug: nginx-setup
status: draft

#!/usr/bin/env bash

# names of latest versions of each package
export VERSION_PCRE=pcre-8.37
export VERSION_OPENSSL=openssl-1.0.2d
export VERSION_NGINX=nginx-1.9.4

# URLs to the source directories
export SOURCE_OPENSSL=https://www.openssl.org/source/
export SOURCE_PCRE=ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
export SOURCE_NGINX=http://nginx.org/download/

# make a 'today' variable for use in back-up filenames later
today=$(date +"%Y-%m-%d")

# clean out any files from previous runs of this script
rm -rf build
rm -rf /etc/nginx-default
mkdir build

# ensure that we have the required software to compile our own nginx
apt-get -y install curl wget build-essential libz-dev libssl-dev

# grab the source files
wget -P ./build $SOURCE_PCRE$VERSION_PCRE.tar.gz
wget -P ./build $SOURCE_OPENSSL$VERSION_OPENSSL.tar.gz --no-check-certificate
wget -P ./build $SOURCE_NGINX$VERSION_NGINX.tar.gz

# expand the source files
cd build
tar xzf $VERSION_NGINX.tar.gz
tar xzf $VERSION_OPENSSL.tar.gz
tar xzf $VERSION_PCRE.tar.gz
cd ../

# set where OpenSSL and nginx will be built
export BPATH=$(pwd)/build
export STATICLIBSSL="$BPATH/staticlibssl"

# build static openssl
cd $BPATH/$VERSION_OPENSSL
rm -rf "$STATICLIBSSL"
mkdir "$STATICLIBSSL"
make clean
./config --prefix=$STATICLIBSSL no-shared\
&& make depend \
&& make \
&& make install_sw

# rename the existing /etc/nginx directory so it's saved as a back-up
mv /etc/nginx /etc/nginx-$today

# build nginx, with various modules included/excluded
cd $BPATH/$VERSION_NGINX
mkdir -p $BPATH/nginx
./configure --with-cc-opt="-I $STATICLIBSSL/include -I/usr/include" \
--with-ld-opt="-L $STATICLIBSSL/lib -Wl,-rpath=$STATICLIBSSL/lib -lssl -lcrypto -ldl -lz" \
--sbin-path=/usr/sbin/nginx \
--conf-path=/etc/nginx/nginx.conf \
--pid-path=/var/run/nginx.pid \
--error-log-path=/var/log/nginx/error.log \
--http-log-path=/var/log/nginx/access.log \
--with-pcre=$BPATH/$VERSION_PCRE \
--with-http_ssl_module \
--with-file-aio \
--with-http_gzip_static_module \
--without-mail_pop3_module \
--without-mail_smtp_module \
--without-mail_imap_module \
&& make && make install

# rename the compiled 'default' /etc/nginx directory so its accessible as a reference to the new nginx defaults
mv /etc/nginx /etc/nginx-default

# now restore the previous version of /etc/nginx to /etc/nginx so the old settings are kept
mv /etc/nginx-$today /etc/nginx

echo "All done.";
echo "This build has not edited your existing /etc/nginx directory.";
echo "If things aren't working now you may need to refer to the";
echo "configuration files the new nginx ships with as defaults,";
echo "which are available at /etc/nginx-default";



cp -R /etc/nginx-default /etc/nginx

useradd nginx
groupadd nginx
usermod -g nginx -G www-data nginx

mkdir /var/www
chmod -R 775 /var/www
chown -R www-data:www-data /var/www





user              nginx;
worker_processes  2;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;

events {
  worker_connections  1024;
}

http {
  include       /etc/nginx/mime.types;
  default_type  application/octet-stream;

  access_log  off;

  sendfile     on;
  tcp_nopush   on;
  tcp_nodelay  on;
  expires      max;
  directio     5m;

  client_body_timeout    10;
  client_header_timeout  10;
  keepalive_timeout      5 5;
  send_timeout           10;

  client_body_buffer_size      1K;
  client_header_buffer_size    1k;
  client_max_body_size         1k;
  large_client_header_buffers  2 1k;

  server_tokens  off;
  add_header     X-Frame-Options SAMEORIGIN;
  add_header     X-Content-Type-Options nosniff;
  add_header     X-XSS-Protection "1; mode=block";

  gzip               on; 
  gzip_proxied       any;
  gzip_min_length    1000;
  gzip_http_version  1.0;
  gzip_buffers       16 8k;
  gzip_comp_level    4;
  gzip_types         text/plain text/css application/json text/javascript application/x-javascript text/xml application/xml application/xml+rss;

  include /etc/nginx/conf.d/*.conf;
}

server {
  listen       80;
  server_name  localhost;

  index  index.html;
  root   /var/www/dkharitonov.me;

  location ~ /\. {
    return 404;
  }

  location / {
    index      index.html;
    try_files  $uri.html $uri $uri/index.html =404;
  }
}