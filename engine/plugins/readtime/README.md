
readtime - Plugin For Pelican
=============================

This plugin adds a variable to the context of Pelican with an stimation of minutes for reading the article.

Usage
-----

To use it you have to add the plugin name to the **pelicanconf.py** file.

    PLUGINS=[ ... , 'readtime']

Then you can access the minutes variable to show on your **article.html** template. 

    {% if article.readtime %}
    <div><b>Read in {{article.readtime.minutes}} min.</b></div>
    {% endif %}
