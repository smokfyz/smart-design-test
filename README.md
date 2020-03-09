# smart-design-test

## Инструкция

OS: Ubuntu 18.04

1. `$ git clone https://github.com/smokfyz/smart-design-test`
2. `$ cd ./assaia-test`
3. `$ python3 -m venv venv`
4. `$ source venv/bin/activate`
5. `$ pip install -r requirements.txt`
6. `$ docker run -d -p 27017:27017 mongo`
7. `$ python3 products/app.py`

## Тестовый сценарий

1. `$ curl --request GET http://localhost:8080/products/  | json_pp`

```json
{
   "data" : []
}
```

2. `$ echo '{"name": "Test Product 1", "description": "Product for test", "parameters": [{"key": "size", "value": "M"}, {"key": "color", "value": "red"}]}' | curl --request POST -d @- http://localhost:8080/products/ | json_pp`
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
```json
{
   "data" : [
      {
         "id" : "5e66c97293f5d5bbb062c4ad",
         "name" : "Test Product 1"
      },
      {
         "id" : "5e66c98b93f5d5bbb062c4ae",
         "name" : "Test Product 2"
      },
      {
         "id" : "5e66c99893f5d5bbb062c4af",
         "name" : "Test Product 3"
      }
   ]
}
```
5. `$ curl --request GET http://localhost:8080/products/?name=Test%20Product%201 | json_pp`
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