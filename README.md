# Jewell Mirror

## Структура


### :one:: GUI

* Интерфейс зеркала
  * Время Шаббата
  * Количество мест на Каббалат шаббат
  * Время
  * Посещаемость
    * Оставшееся время на приход/уход
    * Информация о посещении
* Администрирование
  * Управление сервисами
  * Просмотр Базы Данных

### :two:: Dashboard Camera
* Распознавание лиц 
* Проверка посещаемости 

### :three:: Background
* Выключение/Включение на/после Шаббат(-а)
* Обновление данных
    * Пользователи
    * Расписание

### :four:: MusicPlayer
* Озвучка текста
* Музыкальный плеер

## Комплектущие

- [Процессор AMD Ryzen 3 3200G](https://market.yandex.ru/product--protsessor-amd-ryzen-3-3200g-am4-4-x-3600-mgts/508267136?glfilter=37693330%3A38326419_100709217342&sku=100709217342&cpa=1)
- [Материнская плата ASRock A320M-ITX](https://www.dns-shop.ru/product/4e7cb0d2afad3332/materinskaa-plata-asrock-a320m-itx/)
- [Оперативная память AMD Radeon R7 Performance Series [R748G2400U2S-U] 8 ГБ](https://www.dns-shop.ru/product/3212767aee271b80/operativnaa-pamat-amd-radeon-r7-performance-series-r748g2400u2s-u-8-gb/)
- [256 ГБ 2.5" SATA накопитель Kingston KC600 [SKC600/256G]](https://www.dns-shop.ru/product/d4e603ebe7a3ed20/256-gb-25-sata-nakopitel-kingston-kc600-skc600256g/)
- [Серверный БП Exegate ServerPRO-1U-400ADS](https://www.dns-shop.ru/product/e9090130a6ee3332/servernyj-bp-exegate-serverpro-1u-400ads/)
- [Кулер для процессора DEEPCOOL Gamma Archer [DP-MCAL-GA]](https://www.dns-shop.ru/product/376bac04499230b1/kuler-dla-processora-deepcool-gamma-archer-dp-mcal-ga/)
- [Wi-Fi адаптер USB TP-Link TL-WN727N](https://www.ozon.ru/product/tp-link-tl-wn727n-besprovodnoy-usb-adapter-28103799/?from=share_android&sh=QNJEjhoFNA&utm_campaign=productpage_link&utm_medium=share_button&utm_source=smm)
- [Камера]()
- [Монитор]()

## Устновка

### Операционная система

1. Скачиваем [ОС Ubuntu 20.*](https://releases.ubuntu.com/focal/)
2. Устанавливаем дистрибутив по [инструкции](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview)

### Настройка среды

1. [AnyDesk](https://anydesk.com/en/downloads/linux)
2. [MongoDB](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/)
3. [MongoDB Compass](https://www.mongodb.com/docs/compass/current/install/)
4. [Git](https://git-scm.com/download/linux)

### Установка пакетов

1. `sudo apt-get install build-essential cmake pkg-config`
2. `sudo apt-get install libx11-dev libatlas-base-dev`
3. `sudo apt-get install libgtk-3-dev libboost-python-dev`
4. `sudo apt-get install python-dev python-pip python3-dev python3-pip`
5. `pip install python-dev-tools`
6. Переходим в директории Background & GUI (**от root**) & Dashboard Camera и пишем `pip install -r requirements.txt`

### Настройка [сервисов](https://dzen.ru/media/cyber/sozdaem-systemd-iunit-unit-na-primere-telegram-bota-62383c5d55ea3027de06d7ed?utm_referer=away.vk.com)

1. mirror_background
```
[Unit]
Description=Background
After=syslog.target
After=network.target

[Service]
Type=simple
User=jewell
WorkingDirectory=/home/jewell/Desktop/JewellMirror/Background
ExecStart=/usr/bin/python3 /home/jewell/Desktop/JewellMirror/Background/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. mirror_camera
```
[Unit]
Description=Camera
After=syslog.target
After=network.target

[Service]
Type=simple
User=jewell
WorkingDirectory=/home/jewell/Desktop/JewellMirror/DashboardCamera
ExecStart=/usr/bin/python3 /home/jewell/Desktop/JewellMirror/DashboardCamera/camera.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. mirror_gui
```
[Unit]
Description=GUI
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/jewell/Desktop/JewellMirror/GUI
ExecStart=/usr/bin/python3 /home/jewell/Desktop/JewellMirror/GUI/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. mirror_mp
```
[Unit]
Description=MusicPlayer
After=syslog.target
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/jewell/Desktop/JewellMirror/MusicPlayer
ExecStart=/usr/bin/python3 /home/jewell/Desktop/JewellMirror/MusicPlayer/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### Bash скрипты (```sh *.sh```)

1. start.sh
```
#!/bin/bash

sudo systemctl start mirror_gui.service
sudo systemctl start mirror_background.service
sudo systemctl start mirror_camera.service
sudo systemctl start mirror_mp.service
```

2. stop.sh
```
#!/bin/bash

sudo systemctl stop mirror_gui.service
sudo systemctl stop mirror_background.service
sudo systemctl stop mirror_camera.service
sudo systemctl stop mirror_mp.service
```
