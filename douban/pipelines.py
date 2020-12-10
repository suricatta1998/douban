# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import os
from urllib.request import urlretrieve


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class Top100Pipeline:
    def __init__(self, sqlite_file: str, images_dir: str) -> None:
        self.sqlite_file = sqlite_file
        self.images_dir = images_dir

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file=crawler.settings.get('SQLITE_FILE'),
            images_dir=crawler.settings.get('IMAGES_DIR')
        )

    def open_spider(self, spider):
        self.db = sqlite3.connect(self.sqlite_file)
        self.cursor = self.db.cursor()
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS top100 (
                no, title, director, starrings, movie_type, region, years, cover_image
            )
        ''')
    
    def close_spider(self, spider):
        self.cursor.close()
        self.db.close()

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        sql = f'INSERT INTO top100 ({keys}) VALUES ({values})'
        image_name = f"{data['title']}.png"
        urlretrieve(data['cover_image'], os.path.join(self.images_dir, image_name))
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item

