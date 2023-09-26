
# Hakaton BACK
---

### Команды для работы с приложением
Команда | Код
--------|-------
Сборка контейнера | docker build -t hakaton_back .
Запуск докера | docker run -it --name hakaton_back -p 55002:55002 --ip="172.20.1.102" --network="mlbase_network" --privileged hakaton_back bash
Запуск сервера uvicorn | python -m uvicorn main:app --host 0.0.0.0 --port 55002 --reload
Запуск сервера gunicorn | gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:55002 main:app --reload

##### Настройки nginx 
```
location /api/hakaton_back/ {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    add_header Cache-Control "no-cache";
    proxy_pass http://172.20.1.102:55002/;
}
```

