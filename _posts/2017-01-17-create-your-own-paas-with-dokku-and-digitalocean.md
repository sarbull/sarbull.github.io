---
title: "Create your own PaaS with Dokku and DigitalOcean"
description: "Historical setup notes for a Dokku PaaS on DigitalOcean: Ubuntu, swap space, PostgreSQL, and a Rails deployment through Git."
author: "sarbull"
tags: [deployment, dokku]
---

Dokku is a self-hosted platform as a service that deploys applications from Git. This walkthrough records an Ubuntu and DigitalOcean setup with PostgreSQL and a sample Rails application.

**Historical setup:** the installer below is pinned to Dokku 0.10.5. For a new server, use the [current Dokku installation guide](https://dokku.com/docs/getting-started/installation/) and its supported operating systems and resource requirements.

## Create a DigitalOcean droplet
Create a DigitalOcean droplet with an Ubuntu release supported by the Dokku version you plan to install. Choose memory for your application and database workload; swap uses disk space and does not replace physical RAM.

## Install Dokku on Ubuntu
```bash
$ wget https://raw.githubusercontent.com/dokku/dokku/v0.10.5/bootstrap.sh
$ sudo DOKKU_TAG=v0.10.5 bash bootstrap.sh
```

## Add 1GB of SWAP Memory
```bash
$ sudo swapon --show
$ free -h
$ df -h
$ sudo fallocate -l 1G /swapfile
$ sudo chmod 600 /swapfile
$ sudo mkswap /swapfile
$ sudo swapon /swapfile
$ sudo swapon --show
$ free -h
$ sudo cp /etc/fstab /etc/fstab.bak
$ echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
$ cat /proc/sys/vm/swappiness # 60
$ sudo sysctl vm.swappiness=10 # vm.swappiness = 10
$ sudo vim /etc/sysctl.conf # add vm.swappiness=10
$ cat /proc/sys/vm/vfs_cache_pressure # 100
$ sudo sysctl vm.vfs_cache_pressure=50 # vm.vfs_cache_pressure = 50
$ sudo vim /etc/sysctl.conf # vm.vfs_cache_pressure=50
$ sudo reboot
```

## Deploy a simple application
### Dokku app required instances
```bash
$ ssh root@DROPLET_IP
$ dokku apps:create ruby-rails-sample
$ dokku plugin:install https://github.com/dokku/dokku-postgres.git
$ dokku postgres:create rails-database
$ dokku postgres:link rails-database ruby-rails-sample
```

### Ruby on Rails sample app push to dokku instance
```bash
$ git clone git@github.com:heroku/ruby-rails-sample.git
$ cd ruby-rails-sample
$ git remote add dokku dokku@DROPLET_IP:ruby-rails-sample
$ git push dokku master
```

## Related deployment notes

- [Deploy WordPress with Dokku and MariaDB]({% post_url 2025-11-02-deploy-wordpress-with-dokku %}).
- [Dokku Git deployment documentation](https://dokku.com/docs/deployment/methods/git/).
