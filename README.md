[python-download]: https://www.python.org/downloads/
[redis-download]: https://redis.io/download/

![Python Badge](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=flat&logo=redis&logoColor=white)
[![Docker](https://badgen.net/badge/icon/docker?icon=docker&label)](https://https://docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build](https://github.com/amssdias/py-task/actions/workflows/testing.yml/badge.svg)](https://github.com/amssdias/py-task/actions/workflows/testing.yml)

<h1 align=center>Py Task</h1>

This is a simple Python-based todo application that allows users to manage their tasks using the command line interface (CLI). Users can create an account, log in, and add, edit or delete tasks.

The app uses a basic text-based interface to display tasks, and users can navigate the interface using simple keyboard commands. Tasks are stored in a local database, which means that users can easily access and manage their tasks without an internet connection.

This app is designed for users who prefer a simple, no-frills approach to task management. It's ideal for people who spend a lot of time working on the command line or who want to quickly add or manage tasks without navigating a complex interface.

## :hammer: Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Pre requisites

- [Python][python-download] - 3.9
- [Redis][redis-download]
- [Docker](https://www.docker.com/) (Optional)

### Installing


1. Clone this repository to your local machine
2. Navigate to the project directory


```
git clone https://github.com/amssdias/py-task.git
cd py-task
```


#### Run with Docker

1. Build the Docker image:

```
docker build -t py-task .
```

2. Run the Docker container:

```
docker run -it py-task
```

#### Run


1. Install requirements with pip:

```python
pip install -r requirements.txt
```

2. Run program:

```python
python main.py
```


## :mag_right: Usage

You can register so after login and save tasks from your terminal.

Have fun :smile:
