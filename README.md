# protobuflib
Версия 0.0

Автор: Шушарин Николай (prefie@bk.ru)


## Описание
protobuflib - библиотека, использующая такой формат сериализации данных, как protobuf


## Требования
* Python версии не ниже 3.6


## Состав
* Библиотека: `protobuflib.py`
* Модули: `modules/`
* Примеры .proto файлов `examples/`
* Тесты: `test_protobuflib.py`


## Пример .proto файла
```
syntax = "proto2";

message Car {
  required string model = 1;

  enum BodyType {
    sedan = 0;
    hatchback = 1;
    SUV = 2;
  }

  required BodyType type = 2 [default = sedan];
  optional string color = 3;
  required int32 year = 4;

  message Owner {
    required string name = 1;
    required string lastName = 2;
    required int64 driverLicense = 3;
  }

  repeated Owner previousOwner = 5;
}
``` 
# Типы атрибутов
`required` - Поле обязательно и его нужно указать при инциализации класса

`optional` - Необязательное поле

`repeated` - Повторяющееся поле


## Пример использования:

`import protobuflib as pb`

`Car = pb.create('examples/good/car_normal.proto')`

`car1 = Car('model', Car.BodyType.hatchback, 2008)`

`Student = pb.create('examples/good/student_normal.proto')`

`student = Student('Alex')`

## Подробности реализации
Модули, отвечающие за парсинг и внутреннее представление .proto-файлов находятся в пакете `modules`.
При вызове функции `create` из `protobuflib.py` открывается указанный в качестве первого аргумента файл.
Из него создаётся внутреннее представление класса, описанного в .proto-файле.
По этому представлению создаётся класс.