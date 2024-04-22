<h1 align="center">Welcome to fvChars 👋</h1>
<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-0.1.0-blue.svg?style=for-the-badge" />
  <a href="#" target="_blank">
    <img alt="License: MIT License" src="https://img.shields.io/github/license/HyScript7/fvWeb.svg?style=for-the-badge" />
  </a>
</p>

> A character sheet editor and viewer for Fusionverse.

## Built using

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
- ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
- ![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
- ![PNPM](https://img.shields.io/badge/pnpm-%234a4a4a.svg?style=for-the-badge&logo=pnpm&logoColor=f69220)
- ![SolidJS](https://img.shields.io/badge/SolidJS-2c4f7c?style=for-the-badge&logo=solid&logoColor=c8c9cb)
- ![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
- ![DaisyUI](https://img.shields.io/badge/daisyui-5A0EF8?style=for-the-badge&logo=daisyui&logoColor=white)
- ![NGINX](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
- ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
- Memcached

## Install

1. Frontend

```sh
cd frontend
pnpm i
```

2. Backend

```sh
cd backend
poetry install
```

## Usage

1. Run Frontend for Development

```sh
cd frontend
pnpm run dev
```

2. Run Backend for Development

```sh
cd backend
poetry run uvicorn app:app --reload
```

## Run using Docker

Make sure you have [docker](http://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/install/) installed!

```sh
docker-compose up
```

or if you want to detach from output:

```sh
docker-compose up -d
```

## Run tests

1. Backend

```sh
cd backend
poetry run pytest --cov
# or without coverage
poetry run pytest
```

2. Frontend

```sh
# Not implemented
```

## Author

👤 **HyScript7**

- Github: [@HyScript7](https://github.com/HyScript7)

## Show your support

Give a ⭐️ if this project helped you!

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
