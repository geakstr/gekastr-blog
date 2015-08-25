Title: Делаем Raspberry Pi доступным из интернета при динамичном IP
Date: 2015-08-25 12:00
Tags: rpi, nix, dns, yandex
Slug: yandex-dns-for-raspberry-pi
Status: published

Если вы хотите сделать пай доступным извне по доменному имени, у вас не статичный IP и у вас есть, собственно, домен, который можно делегировать, то, как вариант, предлагаю воспользоваться сервисом от Яндекса — [Почта для домена] [ya_pdd]. Помимо предоставления почты Яндекс позволяет настраивать DNS параметры домена через REST API.

Этим мы и воспользуемся, написав соответствующий скрипт, который будет автоматически обновлять IP адрес пая в DNS Яндекса. Для начала, конечно, домен должен быть делегирован Яндексу. [Тут] [ya_pdd_help] написано как это сделать.

Создадим скрипт:

    #!bash
    mkdir ~/bin && cd ~/bin && nano ya_dns

Тело скрипта:
    
    #!/usr/bin/env bash

    # Использование:
    # ./ya_dns <id> <domain> <subdomain> <ttl>

    # Получим токен для доступа к API
    # Нужно заменить <yourdomain.com> на имя домена
    # https://pddimp.yandex.ru/token/index.xml?domain=<yourdomain.com>
    token="<put token here>"

    # Посмотреть информацию о DNS параметрах тут
    # Необходимо найти A запись для нужного домена/поддомена.
    # Для использования скрипта нужно узнать следующее: id, domain, subdomain, ttl
    # https://pddimp.yandex.ru/nsapi/get_domain_records.xml?token=<your_token_here>&domain=<yourdomain.com>

    # Подробнее про редактирование записи по API можно почитать тут:
    # https://tech.yandex.ru/pdd/doc/reference/dns-edit-docpage/

    args=("$@")

    # Тут будем хранить IP
    ip_file="/tmp/cur_ip.txt"

    old_ip=$(cat $ip_file)

    # Получим текущий IP
    cur_ip=$(/usr/bin/curl -sL http://icanhazip.com)

    # Если IP изменился с прошлого раза
    if [ "$cur_ip" != "$old_ip" ]
    then
      # Сохраним новый IP
      echo $cur_ip > $ip_file

      record_id=${args[0]}
      domain=${args[1]}
      subdomain=${args[2]}
      ttl=${args[3]}

      # Обновим IP на яндексе
      ya_pdd_url="https://pddimp.yandex.ru/nsapi/edit_a_record.xml?"
      query_url="${ya_pdd_url}token=${token}&record_id=${record_id}&domain=${domain}&subdomain=${subdomain}&ttl=${ttl}&content=${cur_ip}"
      ya_pdd_response=$(/usr/bin/curl -sL $query_url)

      #echo $ya_pdd_response
    fi

Делаем скрипт исполняемым `chmod +x ./ya_dns`, и используем так: 
    
    #!bash
    ./ya_dns <id> <domain> <subdomain> <ttl>

Остается добавить его на запуск по расписанию: `crontab -e`

    #!bash
    # Запускать каждые 5 минут
    */5 * * * * /home/pi/bin/ya_dns <id> <domain> <subdomain> <ttl>

Не забудьте открыть нужные вам порты на устройстве, с помощью которого подключаетесь к интернету.

_P.S. Если у вас нет домена, но все же хотите иметь доступ к паю, можно переделать скрипт так, чтобы пай отправлял вам смс с новым IP (например, через [sms.ru] [sms_ru]). Или еще что-нибудь такое._

[ya_pdd]: https://pdd.yandex.ru
[ya_pdd_help]: https://yandex.ru/support/pdd/hosting.xml
[sms_ru]: http://sms.ru/?panel=main&subpanel=programmer