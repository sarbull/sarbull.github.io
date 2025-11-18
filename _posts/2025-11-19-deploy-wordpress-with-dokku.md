---
title:        "Deploy wordpress with dokku"
# jekyll-seo-tag
description:  "How to deploy a wordpress with dokku"
image:        "http://placehold.it/400x200"
author:       "sarbull"
---

## Step 1: Make sure you have dokku installed on your server
```sh
$ ssh root@server
root@server $ dokku --version
dokku version 0.36.3
```
## Step 2: Install MariaDB plugin and create a database
```sh
$ sudo dokku plugin:install https://github.com/dokku/dokku-mariadb.git --name mariadb
$ dokku mariadb:create database
```
## Step 3: Create dokku application
```sh
$ dokku apps:create wordpress
```
## Step 4: Link database to application
```sh
$ dokku mariadb:link database wordpress # it will also add a specific ENV variable
```
## Step 5: Mount storage for the application
```sh
$ mkdir -p /var/lib/dokku/data/storage/wordpress/wp-content/plugins
$ mkdir /var/lib/dokku/data/storage/wordpress/wp-content/uploads
$ mkdir /var/lib/dokku/data/storage/wordpress/wp-content/themes
$ chown -R 32767:32767 /var/lib/dokku/data/storage/wordpress/wp-content
$ dokku storage:mount wordpress /var/lib/dokku/data/storage/wordpress/wp-content:/app/wp-content
```
## Step 6: Add ENV variables for application
```sh
$ dokku config:set wordpress AUTH_KEY=auth-key \
  SECURE_AUTH_KEY=secure-auth-key \
  LOGGED_IN_KEY=logged-in-key \
  NONCE_KEY=nonce-key \
  AUTH_SALT=auth-salt \
  SECURE_AUTH_SALT=secure-auth-salt \
  LOGGED_IN_SALT=logged-in-salt \
  NONCE_SALT=nonce-salt
```
## Step 7: Download latest wordpress version
```sh
$ curl -LO https://wordpress.org/latest.zip
$ unzip latest
$ mv latest wordpress
```
## Step 8: Adjust nginx configuration
```sh
$ cd wordpress
$ echo "# Disable directory listings
autoindex off;

# Set index files (WordPress needs index.php first)
index index.php index.html index.htm;

# Handle PHP files FIRST (before other location blocks)
# This ensures all PHP files are processed, including those from rewrites
location ~ \.php$ {
    try_files $uri =404;
    fastcgi_pass heroku-fcgi;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_param REQUEST_URI $request_uri;
    fastcgi_param QUERY_STRING $query_string;
    include fastcgi_params;
    fastcgi_index index.php;

    # Ensure proper content type
    default_type text/html;
}

# Handle WordPress static files (themes, plugins, uploads)
# Note: PHP files in wp-content will be caught by the PHP location block above
location ~ ^/wp-content/(.*\.(jpg|jpeg|gif|png|css|js|ico|svg|woff|woff2|ttf|eot))$ {
    try_files $uri =404;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# Handle WordPress includes (static JS/CSS files)
location ~ ^/wp-includes {
    try_files $uri =404;
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# REST API rewrite
location ~ ^/wp-json/ {
    rewrite ^/wp-json/(.*?)$ /?rest_route=/$1 last;
}

# WordPress URL rewrite rules - handle root and all paths
# This must come after PHP handler to allow rewrites to index.php
location / {
    # Try the requested URI, then as a directory, then fallback to index.php
    # This ensures root "/" routes to index.php
    try_files $uri $uri/ /index.php?$args;
}

# Deny access to hidden files
location ~ /\. {
    deny all;
    access_log off;
    log_not_found off;
}

# Deny access to sensitive WordPress files
location ~ /(readme\.html|license\.txt|wp-config\.php|wp-config-sample\.php|xmlrpc\.php|wp-config\.bak) {
    deny all;
    access_log off;
    log_not_found off;
}" > .nginx.conf
$ echo "upload_max_filesize = 128M
post_max_size = 128M
max_execution_time = 600
memory_limit = 256M
max_input_time = 300" > custom_php.ini
```
## Step 9: Add git
```sh
$ git init
$ git add .
$ git commit -m "First commit"
```
## Step 9: Hook it up to dokku server
```sh
$ git remote add dokku dokku@server:wordpress
```
## Step 10: Deploy
```sh
$ git push dokku main
```
