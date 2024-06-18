from xml.etree import ElementTree as etree
import sqlite3
import os
import urllib2
import requests

url = 'https://www.gesetze-im-internet.de/aktuDienst-rss-feed.xml'
response = requests.get(url)
with open('feed.xml', 'wb') as file:
    file.write(response.content)

os.remove('feed.db')

tree = etree.parse('feed.xml')
root = tree.getroot()
items = root.findall('channel/item')

conn = sqlite3.connect('feed.db')
cur = conn.cursor()

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS feed (
          id          INTEGER PRIMARY KEY AUTOINCREMENT
        , guid        TEXT
        , title       TEXT
        , link        TEXT
        , description TEXT
        , pubDate     TEXT
    ) STRICT;
    '''
)

print('Processing RSS feed...')

for item in items:
    title = item.find('title').text
    link = item.find('link').text
    description = item.find('description').text
    guid = item.find('guid').text
    pubDate = item.find('pubDate').text
    print('title', title)
    print('link', link)
    cur.execute(
        '''
        INSERT INTO feed (guid, title, link, description, pubDate)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (title, link, guid, description, pubDate)
    )

conn.commit()
conn.close()

os.remove('feed.xml')

print('Done.')
