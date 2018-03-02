setup(
    name='exemplo',
    install_requires=[
        'telegram',
        'python-telegram-bot',
        'redis',
        'BeautifulSoup4'
    ],
)

from main import updater
updater.start_polling()
