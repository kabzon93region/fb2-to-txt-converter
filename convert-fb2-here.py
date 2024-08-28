from bs4 import BeautifulSoup
from os import system, listdir
from loguru import logger
import warnings
warnings.filterwarnings("ignore")

logger.add("./log.log", format="{time:DD.MM.YYYY HH:mm:ss:(x)} - {level} - {message}", level="DEBUG", rotation="35 MB", compression="zip")
logger.info("Программа запущена.")

def get_chapters(section):
    try:
        rows = '\n'.join([p.get_text(strip=True) for p in section])
        logger.info('Глава добавлена')
    except Exception as e:
            logger.warning(f"Ошибка (get_chapters): {e}")
            #system('pause')
    return f'{rows}'

def get_authors(soupfile):
    try:
        authors = ''
        it = 0
        for author in soupfile.find_all('author'):            
            it+=1
            if len(author.find("first-name").get_text(strip=True)) > 1 and len(author.find("last-name").get_text(strip=True)) > 1:
                if authors == (author.find("first-name").get_text(strip=True)) + (' ') + (author.find("last-name").get_text(strip=True)) :
                    ''
                else:
                    if it > 1 and len(author.find("first-name").get_text(strip=True)) > 2 :
                        authors += ', '
                    authors += (author.find("first-name").get_text(strip=True)) + (' ') + (author.find("last-name").get_text(strip=True))
                    logger.info('Автор добавлен')
        logger.info('Авторы добавлены')
    except Exception as e:
            logger.warning(f"Ошибка (get_authors): {e}")
            #system('pause')
    return f'{authors}'

def get_book_title(soupfile):
    try:
        book_title = soupfile.find("book-title").get_text(strip=True)
        logger.info('Название книги добавлено')
    except Exception as e:
            logger.warning(f"Ошибка (get_book_title): {e}")
            #system('pause')
    return f'{book_title}'

def get_book(soupfile):
    try:
        book = ''
        book += 'Авторы: ' + get_authors(soupfile) + ('\n')
        book += 'Название книги: ' + (get_book_title(soupfile)) + ('\n\n')
        for section in soupfile.find_all('section'):
            book += get_chapters(section) + '\n\n'
    except Exception as e:
            logger.warning(f"Ошибка (get_book): {e}")
            #system('pause')
    return book


for filename in listdir('.'):
    if filename.endswith(".fb2"):
        logger.info(filename)

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), 'lxml')
            logger.info('Файл открыт')
        except Exception as e:
            logger.error(f"Ошибка 1: {e}")
            system('pause')
            exit(1)

        try:
            with open(filename + '.txt', 'w', encoding='utf-8') as f:
                f.write(get_book(soup))
            logger.info('Файл сохранен)
        except Exception as e:
            logger.error(f"Ошибка 2: {e}")
            system('pause')
            exit(2)

logger.info('Скрипт завершен.')
system('pause')