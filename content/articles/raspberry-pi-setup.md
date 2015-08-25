Title: Вдумчивая настройка Raspberry Pi
Date: 2015-08-24 23:30
Tags: rpi, nix
Slug: raspberry-pi-setup

[TOC]

### Скачиваем и конфигурируем образ 

Детально про используемый образ можно почитать [в репозитории проекта] [raspbian-ua-netinst]. Для начала необходимо узнать номер последней версии образа [тут] [raspbian-ua-netinst-latest].

    #!bash
    # Замените <version-number> на номер версии
    rpi_inst_v=v<version-number>

    # Скачиваем образ
    wget https://github.com/debian-pi/raspbian-ua-netinst/releases/download/$rpi_inst_v/raspbian-ua-netinst-$rpi_inst_v.zip

    # Разархивируем
    unzip raspbian-ua-netinst-${rpi_inst_v}.zip -d ./raspbian-ua-netinst-${rpi_inst_v}
    cd raspbian-ua-netinst-${rpi_inst_v}

    # Укажем пароль (свой) для root пользователя
    echo "rootpw=<password>" > ./installer-config.txt

    # (опционально) Указываем имя дистрибутива и дополнительные нужные вам пакеты
    echo "release=wheezy" >> ./installer-config.txt
    echo "packages=sudo,curl,nano" >> ./installer-config.txt

### Записываем образ на SD карту

Инструкция для OS X. Всё это можно сделать и через GUI.

    #!bash
    # Узнаём имя карточки (/dev/diskX, где X — число)
    diskutil list

    # Форматируем в FAT 32
    diskutil eraseDisk FAT32 RPI MBRFormat /dev/diskX

    # Копируем образ на карточку
    cp -R ./* /Volumes/RPI

    # И извлекаем её
    diskutil eject /dev/diskX

Теперь вставляем карту в пай и ждем. Если он подключен к телевизору, сможете наблюдать за процессом. Если нет, можно посматривать на лампочку Ethernet на пае, и когда она перестанет хаотично мигать, скорее всего можно идти дальше. Установка занимает минут 15.

### Первоначальная настройка

    #!bash
    # Заходим на пай (пароль тот, что указали вначале)
    ssh root@pi.ip.addr.ess

    # Обновим пакеты
    apt-get update && apt-get dist-upgrade && apt-get upgrade

    # Обновим ядро и прошивку
    # Не используйте утилиту rpi-update, она не работает с этим образом (https://github.com/debian-pi/raspbian-ua-netinst/issues/267)
    # Вместо этого воспользуемся пакетом raspberrypi-bootloader.
    # Он включает в себя ядро и прошивку. Это пакет проекта raspberry pi на github (https://github.com/raspberrypi/linux)
    apt-get install -y raspberrypi-bootloader
    sed -i 's/kernel=/#kernel=/g' /boot/config.txt
    sed -i 's/initramfs /#initramfs /g' /boot/config.txt

    # Сконфигурируем локали и временную зону
    dpkg-reconfigure locales
    dpkg-reconfigure tzdata

    # Добавим нового пользователя
    groupadd pi
    useradd pi -m -K UMASK=0066 -s /bin/bash -g pi -G users,ssh,sudo
    passwd pi

    # Перезагрузимся, чтобы изменения вступили в силу
    reboot

    # Теперь можно зайти на пай под новым пользователем
    ssh pi@pi.ip.addr.ess

### Настраиваем SSH

Если смогли успешно войти под пользователем `pi` на предыдущем шаге, можно приступить к дальшейшей настройке. Усилим безопасность системы.
    
    #!bash
    # Запретим входить под рутом
    sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config

    # Можно разрешить сессии только определенным юзерам
    # [ОПАСНАЯ ОПЦИЯ, проверьте правильность имен несколько раз]
    echo "AllowUsers root pi" | sudo tee --append /etc/ssh/sshd_config

    # Можно ограничить время бездействия пользовательской сессии (здесь 5 минут)
    echo "ClientAliveInterval 300" | sudo tee --append /etc/ssh/sshd_config > /dev/null
    echo "ClientAliveCountMax 0" | sudo tee --append /etc/ssh/sshd_config > /dev/null

    # Перезапустим SSH демон
    sudo /etc/init.d/ssh restart

#### Настраиваем авторизацию по ключу

    #!bash
    # На _своей_ машине сгенерируем ключ (если еще этого не делали)
    # Не оставляем пароль ключа пустым
    mkdir .ssh
    ssh-keygen -t rsa -C "your_email@example.com"
    ssh-add ~/.ssh/id_rsa
    # Скопируем свой _публичный_ ключ в буфер обмена
    pbcopy < ~/.ssh/id_rsa.pub

    # Дальнейшие действия делаем на пае под пользователем pi
    mkdir ~/.ssh

    # Сюда вставим в новую строку скопированный публичный ключ
    nano ~/.ssh/authorized_keys

    # Выставим правильные права
    chmod 700 ~/.ssh/
    chmod 600 ~/.ssh/authorized_keys

    # Пробуем выйти и зайти опять, должно пустить без пароля

    # Можно запретить вход по паролю, разрешить только по ключу
    # Нужно помнить, что в случае, если у нас не останется
    # ни одного авторизованного на пае ключа, по SSH войти не сможем
    sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/g' /etc/ssh/sshd_config
    sudo sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config

    # Перезапустим SSH демон
    sudo /etc/init.d/ssh restart

Всё дальнейшее — опционально (впрочем, как и всё, что выше). Ваши потребности естественно могут отличаться от моих, поэтому выполняем команды _вдумчиво_. Рекомендую для удобства действовать от рута (`su root`).

### Конфигурируем параметры пая

    #!bash
    # Выделяем минимальное количество видеопамяти
    echo "gpu_mem=16" >> /boot/config.txt

    # Выключаем модуль камеры
    echo "start_x=0" >> /boot/config.txt

    # Выключаем так называемые "вылеты развертки", они не актуальны для современных телевизоров
    echo "disable_overscan=1" >> /boot/config.txt

    # Разгоняем (подробно можно почитать тут http://elinux.org/RPiconfig)
    echo "arm_freq=1000" >> /boot/config.txt
    echo "core_freq=500" >> /boot/config.txt
    echo "sdram_freq=600" >> /boot/config.txt
    echo "over_voltage=6" >> /boot/config.txt

    # Форсируем Turbo режим в первые 60 секунд работы
    echo "initial_turbo=60" >> /boot/config.txt

    # Делает так, чтобы пай разгонялся только при необходимости
    echo "force_turbo=0" >> /boot/config.txt

### Повышаем производительность

    #!bash
    # Улучшает производительность генератора случайных чисел
    apt-get install -y rng-tools

    # Будет выдано сообщение о том, что скрипт не смог стартовать.
    # Ничего страшного, необходимый модуль станет доступен после перезагрузки
    echo bcm2708-rng >> /etc/modules

    # Улучшает производительность служб управления памятью
    apt-get install -y raspi-copies-and-fills 

    # Можно настроить сеть на статику
    # [ОСТОРОЖНО, нужно быть уверенным в написанном, иначе можно потерять доступ по SSH]
    # Заменяем dhcp
    sed -i 's/iface eth0 inet dhcp/#iface eth0 inet dhcp/g' /etc/network/interfaces
    # На что-то вроде такого, но специфичного для вашей сети
    echo "iface eth0 inet static" >> /etc/network/interfaces
    echo "address 192.168.1.100" >> /etc/network/interfaces
    echo "gateway 192.168.1.1" >> /etc/network/interfaces
    echo "netmask 255.255.255.0" >> /etc/network/interfaces
    echo "network 192.168.1.0" >> /etc/network/interfaces
    echo "broadcast 192.168.1.255" >> /etc/network/interfaces

#### Убираем лишнее

    #!bash
    # Оставляем один getty, т.к. работаем в основном по SSH
    sed -i '/[2-6]:23:respawn:\\/sbin\\/getty 38400 tty[2-6]/s%^%#%g' /etc/inittab
    sed -i '/T0:23:respawn:\\/sbin\\/getty -L ttyAMA0 115200 vt100/s%^%#%g' /etc/inittab

    # Выключаем ipv6
    echo "net.ipv6.conf.all.disable_ipv6=1" > /etc/sysctl.d/disableipv6.conf
    sed -i '/::/s%^%#%g' /etc/hosts

    # Выключаем неиспользуемые модули ядра
    echo "blacklist ipv6" >> /etc/modprobe.d/raspi-blacklist.conf
    echo "blacklist spi-bcm2708" >> /etc/modprobe.d/raspi-blacklist.conf
    echo "blacklist i2c-bcm2708" >> /etc/modprobe.d/raspi-blacklist.conf
    chmod 644 /etc/modprobe.d/raspi-blacklist.conf

    # Планировщик ввода/вывода "noop" лучше подходит для флеш памяти
    sed -i 's/deadline/noop/g' /boot/cmdline.txt

#### Тюним файловую систему

    #!bash
    # noatime и nodiratime отключают запись информации
    # о последнем времени доступа к файлам и директориям
    sed -i 's/errors=remount-ro,noatime /errors=remount-ro,noatime,nodiratime /g' /etc/fstab

    # Разрешаем автоматически восстанавливать файловые системы при загрузке,
    # если с ними что-то не так
    sed -i "s/#FSCKFIX=no/FSCKFIX=yes/g" /etc/default/rcS

    # Каждые 3 перезагрузки проверяем главный раздел файловой системы
    tune2fs -c 3 /dev/mmcblk0p2

    # writeback тип записи в журнал дает больше производительности.
    # однако при падении системы данные могут потеряться
    # [ВЫПОЛНЯТЬ ТОЛЬКО С ПОНИМАНИЕМ РИСКОВ]
    tune2fs -o journal_data_writeback /dev/mmcblk0p2

    # Перезагружаемся
    reboot

#### Логгируем в оперативной памяти

Это, во-первых, увеличит производительность, во-вторых, снизит нагрузку на SD карту. Для этого воспользуемся утилитой [`ramlog`] [ramlog]. Но, если у вас в системе демонами рулит `systemd` (например, потому что вы установили Debian 8 Jessie), то ничего не получится — `ramlog`, по крайней мере в версии 2.0.0, не совместим с ним.

    #!bash
    # Скачиваем и устанавливаем ramlog
    cd /tmp
    wget http://www.tremende.com/ramlog/download/ramlog_2.0.0_all.deb
    apt-get install -y lsof rsync && dpkg -i ramlog_2.0.0_all.deb

    # Задаем максимальный объем логов в памяти
    sed -i 's/TMPFS_RAMFS_SIZE=\\t/TMPFS_RAMFS_SIZE=40m\\t/g' /etc/default/ramlog

    # Говорим, что ramlog надо запускать/останавливать до/после rsyslog
    sed -i 's/# Provides: ramlog/# Provides: ramlog\\n# X-Start-Before: rsyslog\\n# X-Stop-After: rsyslog/g' /etc/init.d/ramlog

    # Дадим знать об этом автозагрузке
    insserv -v /etc/init.d/ramlog

    # Теперь нужно 2 (!) раза перезагрузить пай
    reboot

    # Проверить состояние ramlog можно так
    /etc/init.d/ramlog status

    # Напоследок уберем абсолютно неважные логи крона про успешную авторизацию
    sed -i 's/(the "Additional" block)/(the "Additional" block)\\nsession [success=1 default=ignore] pam_succeed_if.so service in cron quiet use_uid/g' /etc/pam.d/common-session-noninteractive

### Настраиваем фаервол

Рекомендую не полениться и сконфигурировать фаервол — это хороший способ повысить безопасность системы. Установим `iptables` (самый популярный фаервол на Debian подобных системах).

    #!bash
    # Устанавливаем iptables
    apt-get install iptables

    # Скачиваем скрипт для управления демоном
    wget http://git.io/vs7i5 -O /etc/init.d/iptables
    chmod 755 /etc/init.d/iptables && insserv -v /etc/init.d/iptables

Теперь зададим несколько базовых правил `nano /etc/iptables.rules`:

    #!bash
    *filter

    # Принимаем все пакеты для loopback трафика
    -A INPUT -i lo -j ACCEPT -m comment --comment "Allow all loopback traffic"

    # Запрещаем все, что на 127 сети и не использует loopback трафик
    -A INPUT ! -i lo -d 127.0.0.0/8 -j REJECT -m comment --comment "Drop all traffic to 127 that doesnt use lo"

    # Принимаем все входящие пакеты от уже установленных соединений
    -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT -m comment --comment "Allow all incoming on established connections"

    # Разрешаем весь исходящий трафик
    -A OUTPUT -j ACCEPT -m comment --comment "Accept all outgoing"

    # Разрешаем Ping
    -A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT -m comment --comment "Allow Ping"

    # SSH 
    -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
    
    # ... остальные нужные вам правила. По iptables очень много информации в сети

    # Все остальное отклонять. Эти две инструкции должны быть в конце файла
    -A INPUT -j REJECT -m comment --comment "Reject all incoming"
    -A FORWARD -j REJECT -m comment --comment "Reject all forwarded"

    # Говорим фаерволу применить инструкции
    COMMIT

Также необходимо задать правила фаерволу перед поднятием сетевых интерфейсов:

    #!bash
    # Немного правим файл /etc/network/interfaces
    sed -i 's/iface lo inet loopback/iface lo inet loopback\\npre-up iptables-restore < \\/etc\\/iptables.rules/g' /etc/network/interfaces

Наконец, стартуем фаервол:

    #!bash
    /etc/init.d/iptables start

#### Баним ботов пачками с помощью fail2ban

Если ваш пай будет смотреть наружу в интернет, то в него точно начнут ломиться боты. Если у вас в SSH настроена авторизация по ключу и отключена возможность входа по паролю, то смысла в fail2ban не слишком много. Однако он может работать не только с SSH, а со многими утилитами, поэтому всё же стоит рассмотреть вариант его применения. Да и вообще приятно в логах видеть `NOTICE  [ssh] fckn.bot.ip.addr already banned` :)

    #!bash
    # Если не хотим заморачиваться с установкой последней версии fail2ban
    # то просто ставим пакет и переходим к следующему шагу
    apt-get install -y fail2ban

    # Если хотим, будем ставить свежую версию из репозитория
    # fail2ban написан на питоне, поэтому нужно его установить
    apt-get install -y python 

    # Скачаем сам fail2ban
    # Можете посмотреть номер последней релизной версии тут
    # https://github.com/fail2ban/fail2ban/releases
    cd /tmp
    wget https://github.com/fail2ban/fail2ban/archive/0.9.2.tar.gz -O fail2ban.tar.gz

    # Разархивируем
    mkdir fail2ban && tar -xzvf fail2ban.tar.gz -C ./fail2ban --strip-components=1 && cd fail2ban

    # Установим
    python setup.py install

    # Скопируем скрипт для управления fail2ban демоном
    cp ./files/debian-initd /etc/init.d/fail2ban
    chmod 755 /etc/init.d/fail2ban && insserv -v /etc/init.d/fail2ban

Теперь создадим конфиг `nano /etc/fail2ban/jail.local` с примерно таким текстом:

    #!bash
    [DEFAULT]
    # Игнорировать запросы из нашей сети
    ignoreip = 192.168.1.0/24

    # Наблюдаем за авторизацией по ssh
    # Я выставляю очень жесткие настройки, может быть разумнее сделать лояльнее
    [ssh]
    enabled  = true
    port     = ssh
    filter   = sshd
    logpath  = /var/log/auth.log
    # Наблюдать за IP в течение часа
    findtime    = 3600
    # Если 3 попытки входа неудачны
    maxretry    = 3
    # Бан на сутки
    bantime     = 86400

Наконец, запустим fail2ban:

    #!bash
    /etc/init.d/fail2ban start

Логи, чтобы посмотреть успешно прошло или нет, лежат тут:

    #!bash
    cat /var/log/fail2ban.log

На этом, пожалуй, пока что остановимся. Спасибо, что дочитали :)


[raspbian-ua-netinst]: https://github.com/debian-pi/raspbian-ua-netinst
[raspbian-ua-netinst-latest]: https://github.com/debian-pi/raspbian-ua-netinst/releases/latest
[ramlog]: http://www.tremende.com/ramlog/



