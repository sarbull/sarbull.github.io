---
title:       "Deploy wordpress with dokku"
description:  "How to deploy a wordpress with dokku"
image:        ""
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
## Step 8: Adjust nginx and wp-config.php
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
```
```sh
$ echo "upload_max_filesize = 128M
post_max_size = 128M
max_execution_time = 600
memory_limit = 256M
max_input_time = 300" > custom_php.ini
```
```sh
echo "<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the website, you can copy this file to "wp-config.php"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://developer.wordpress.org/advanced-administration/wordpress/wp-config/
 *
 * @package WordPress
 */

$url = parse_url(getenv("DATABASE_URL"));

$host = $url["host"];
$username = $url["user"];
$password = $url["pass"];
$database = substr($url["path"], 1);

/** The name of the database for WordPress */
define( 'DB_NAME', $database );

/** MySQL database username */
define( 'DB_USER', $username );

/** MySQL database password */
define( 'DB_PASSWORD', $password );

/** MySQL hostname */
define( 'DB_HOST', $host );

/** Database charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The database collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication unique keys and salts.
 *
 * Change these to different unique phrases! You can generate these using
 * the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}.
 *
 * You can change these at any point in time to invalidate all existing cookies.
 * This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY', getenv('AUTH_KEY'));
define( 'SECURE_AUTH_KEY', getenv('SECURE_AUTH_KEY'));
define( 'LOGGED_IN_KEY', getenv('LOGGED_IN_KEY'));
define( 'NONCE_KEY', getenv('NONCE_KEY'));
define( 'AUTH_SALT', getenv('AUTH_SALT'));
define( 'SECURE_AUTH_SALT', getenv('SECURE_AUTH_SALT'));
define( 'LOGGED_IN_SALT', getenv('LOGGED_IN_SALT'));
define( 'NONCE_SALT', getenv('NONCE_SALT'));

/**#@-*/

/**
 * WordPress database table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 *
 * At the installation time, database tables are created with the specified prefix.
 * Changing this value after WordPress is installed will make your site think
 * it has not been installed.
 *
 * @link https://developer.wordpress.org/advanced-administration/wordpress/wp-config/#table-prefix
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://developer.wordpress.org/advanced-administration/debug/debug-wordpress/
 */
define( 'WP_DEBUG', false );

/* Add any custom values between this line and the "stop editing" line. */

// Force HTTPS URLs to prevent mixed content issues
if (isset($_SERVER['HTTP_X_FORWARDED_PROTO']) && $_SERVER['HTTP_X_FORWARDED_PROTO'] === 'https') {
    $_SERVER['HTTPS'] = 'on';
}

// Set WordPress URLs to use HTTPS
if (isset($_SERVER['HTTP_HOST'])) {
    $wp_home = 'https://' . $_SERVER['HTTP_HOST'];
    $wp_siteurl = $wp_home;

    // Only define if not already set in database
    if (!defined('WP_HOME')) {
        define('WP_HOME', $wp_home);
    }
    if (!defined('WP_SITEURL')) {
        define('WP_SITEURL', $wp_siteurl);
    }
}

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';" > wp-config.php
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
