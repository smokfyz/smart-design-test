# smart-design-test

## Инструкция

OS: Ubuntu 18.04

1. `$ sudo apt install docker.io git python3-pip python3-venv curl`  
If Docker is not installed before.  
2. `$ sudo usermod -aG docker $USER`  
Restart (or logout)  
3. `$ sudo systemctl start docker`
4. `$ sudo systemctl enable docker`
5. `$ git clone https://github.com/smokfyz/smart-design-test`
6. `$ cd ./smart-design-test`
7. `$ python3 -m venv venv`
8. `$ source venv/bin/activate`
9. `$ pip install -r requirements.txt`

## Конфигурация

В файле config/products.yaml

## Запуск

1. `$ docker run -d -p 27017:27017 mongo`
2. `$ python3 products/app.py`

## Тестовый сценарий

1. `$ curl --request GET http://localhost:8080/products/  | json_pp`  
Получаем список всех продуктов.
```json
{
   "data" : []
}
```

2. `$ echo '{"name": "Test Product 1", "description": "Product for test", "parameters": [{"key": "size", "value": "M"}, {"key": "color", "value": "red"}]}' | curl --request POST -d @- http://localhost:8080/products/ | json_pp`  
Добавляем продукт.  
Response:
```json
{
   "data" : {
      "description" : "Product for test",
      "id" : "5e66c97293f5d5bbb062c4ad",
      "name" : "Test Product 1",
      "parameters" : [
         {
            "key" : "size",
            "value" : "M"
         },
         {
            "key" : "color",
            "value" : "red"
         }
      ]
   }
}
```
3. `$ echo '{"name": "Test Product 2", "description": "Product for test", "parameters": [{"key": "size", "value": "L"}, {"key": "color", "value": "blue"}]}' | curl --request POST -d @- http://localhost:8080/products/ | json_pp`  
Добавляем продукт.  
Response:
```json
{
   "data" : {
      "description" : "Product for test",
      "id" : "5e66c98b93f5d5bbb062c4ae",
      "name" : "Test Product 2",
      "parameters" : [
         {
            "key" : "size",
            "value" : "L"
         },
         {
            "key" : "color",
            "value" : "blue"
         }
      ]
   }
}
```
4. `$ echo '{"name": "Test Product 3", "description": "Product for test", "parameters": [{"key": "size", "value": "L"}, {"key": "color", "value": "yellow"}]}' | curl --request POST -d @- http://localhost:8080/products/ | json_pp`  
Добавляем продукт.  
Response:
```json
{
   "data" : {
      "description" : "Product for test",
      "name" : "Test Product 3",
      "parameters" : [
         {
            "value" : "L",
            "key" : "size"
         },
         {
            "value" : "yellow",
            "key" : "color"
         }
      ],
      "id" : "5e676e13fc7297fc53a73af3"
   }
}
```
5. `$ curl --request GET http://localhost:8080/products/?name=Test%20Product%201 | json_pp`  
Фильрация списка продуктов по названию.  
Response:
```json
{
   "data" : [
      {
         "id" : "5e66c97293f5d5bbb062c4ad",
         "name" : "Test Product 1"
      }
   ]
}
```
6. `$ curl -G -d "parameters[color]=blue&parameters[size]=L" http://localhost:8080/products/ | json_pp`  
Фильтрация списка продукта по параметрам (color = blue и size = L)  
Response:
```json
{
   "data" : [
      {
         "id" : "5e66c98b93f5d5bbb062c4ae",
         "name" : "Test Product 2"
      }
   ]
}
```
7. `$ curl -G http://localhost:8080/products/5e66c98b93f5d5bbb062c4ae | json_pp`  
Получение сведений о товаре по ID.  
Response:
```json
{
   "data" : {
      "description" : "Product for test",
      "id" : "5e66c98b93f5d5bbb062c4ae",
      "name" : "Test Product 2",
      "parameters" : [
         {
            "key" : "size",
            "value" : "L"
         },
         {
            "key" : "color",
            "value" : "blue"
         }
      ]
   }
}
```
