#!/bin/bash

nohup sudo /usr/bin/.pyenv/shims/python manage.py  runserver 0.0.0.0:80 > out.log &
