# Краткое описание

Настоящий репозиторий содержит проект, выполненный в рамках курса Python
Basics.

# Задачи проекта

0. Найти актуальную базу данных по стоимости недвижимости в Санкт-Петербурге,
   Москве, Екатеринбурге.

На основе собранных данных реализовать следующие виды визуализации:

1. Тепловая карта цен на недвижимость. Представляет из себя карту города с
   наложенным на неё слоем, в котором цветом показана цена недвижимости в
   пересчёте на квадратный метр.

2. Гистограмма с отображением средних цен по муниципальным округам указанных
   выше городов.

3. Гистограмма с отображением средней площади квартиры по муниципальным округам
   указанных выше городов.

# Реализация

## Поиск информации

С целью получения исходных данных, были изучены популярные сайты по размещению
объявлений о продаже недвижимости:

- www.domofond.ru
- www.realty.yandex.ru
- www.cian.ru
- www.avito.ru

Для работы над проектом был выбран сайт [ЦИАН](www.cian.ru), поскольку данные
проще всего получить именно с этого ресурса.

## Получение и хранение данных

С целью получения и хранения данных реализован модуль _data_fetching.py_.
Основная функция _data_fetching_ отправляет запросы с заданными параметрами к
API ресурса. В качестве аргументов функция принимает строку с кодом региона и
конфигурационный словарь. Результатом работы функции являются данные,
сохраненные в файле формата csv.

## Обработка данных

Для обработки данных реализован модуль _data_processing.py_. Главными этапами
обработки данных являются:

- Очистка и подготовка сырых данных
- Построение тепловой карты стоимости квадратного метра жилья
- Построение гистограмм стоимости и площади жилья

### Очистка и подготовка данных

Принципиально важна предварительная обработка данных, что бы исключить
искажение результата экстремальными значениями, которые могут присутствовать
в "сырых" данных. Модуль _data_processing.py_ содержит функцию
_data_preparation_, которая принимает в качестве аргумента строку с кодом
региона и конфигурационный словарь. Функция возвращает структуру данных
DataFrame. Из данных удаляются дублирующие записи, выбросы и объекты, которые
выходят за пределы исследуемой зоны более чем на 1 градус долготы или широты.

## Построение тепловой карты

Построение тепловой карты выполняет функция _create_heat_map_. В качестве
аргументов функция принимает структуру данных, строку с кодом региона и
конфигурационный словарь. Работа функции основана на создании интерполянта при
помощи функции LinearNDInterpolator из модуля scipy. Изображение интерполянта
накладывается на заранее подготовленное изображение карты.

## Построение гистограмм

Реализованы функции _create_graph_average_price_ и _
create_graph_average_square_. Аргументами функции являются структура данных и
строка с кодом региона. Графики строятся по вычисленным средним значениям
полей _price_ и _square_ соответственно, данные сгруппированы по муниципальным
районам.

# Выполнение скрипта

### Конфигурационный файл

Основным файлом программы является файл _main.py_. Перед запуском файла
необходимо корректно настроить конфигурационный файл _config.py_.

Конфигурационный файл хранит словарь, ключами которого являются сокращенные
наименования или "коды" городов. Эти коды могут быть произвольной строкой.

Значением ключа является словарь, который содержит в себе следующие параметры,
необходимые для выполнения программы:

- _region code_, код региона в базе данных сайта ЦИАН, определяется опытным
  путем.
- _first page_, страница, с которой программа начнет выполнение.
- _last page_, страница, на которой выполнение программы закончится.
- _adress code_, код адреса, элемент адреса объекта, название региона, района,
  улицы и т.д. Стандартно код 2 хранит информацию о районе, но для
  Санкт-Петербурга код будет 1. Определяется опытным путем.

- параметры _right_, _top_, _left_, _bottom_ хранят информацию о правой,
  верхней, левой и нижней границах карты соответственно.

### Карта

Карты для выполнения программы следует подготовить заранее. Подготовка
существующих карт, была выполнена при помощи сервиса OpenStreetMap. Крайние
координаты выбранной карты следует указать в параметрах конфигурационного
словаря. Карты необходимо сохранить в директории _maps_.

### Выполнение программы

Когда конфигурационный файл и карты подготовленны, можно начинать выполнение
программы. Для этого нужно запустить на выполнение файл _main.py_,
конфигурационный файл будет импортирован.

Сырые данные будут сохранены в формате _csv_ в директории _data_, если
директории не существует, она будет создана. Имена файлов формируются путем
конкатенации строки кода региона и суффикса ".csv".

Результаты визуализации будут сохранены в формате _png_ в директории _output_,
если директории не существует, она будет создана. Имена файлов формируются
путем конкатенации строки кода региона и суффиксов:

- "_heatmap.png" для тепловой карты цен.
- "_graph_average_price.png" для графика средней стоимости недвижимости.
- "_graph_average_square.png" для графика средней площади недвижимости.#
  final_task
