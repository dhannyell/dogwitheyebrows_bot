import os
print "Trying to Install required module: telegram\n"
os.system('pip3 install telegram')
os.system('pip3 install python-telegram-bot')
os.system('pip3 install redis')
os.system('pip3 install BeautifulSoup4')

from main import updater
updater.start_polling()


from main import updater
updater.start_polling()
