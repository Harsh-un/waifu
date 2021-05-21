import telebot
import config
from telebot import types
from keyboa import Keyboa
from PIL import Image
from urllib.request import urlopen
from enum import Enum

id = 0
bot = telebot.TeleBot(config.TOKEN)

class TypeSearch(Enum):
    Anime = 1
    Manga = 2

# получаем список жанров для аниме и манги из всего списка (находится в config)
def getGenresAnimeOrMangu():
    items = config.genresList
    genresAnime = {}
    genresMangu = {}
    k1 = 0
    k2 = 0
    for item in items:
      if item['kind'] == "anime":
        genresAnime[item['russian']] = item['id']
        k1 += 1
      elif item['kind'] == "manga":
        genresMangu[item['russian']] = item['id']
        k2 += 1
    return genresAnime, genresMangu

genresAnime, genresMangu = getGenresAnimeOrMangu() 

# получить меню для Фильтра
def getFilterMenu(type):
    key = types.InlineKeyboardMarkup()
    if type is TypeSearch.Anime:
      but_1 = types.InlineKeyboardButton(text="Жанры", callback_data="GenresAnime")
      but_2 = types.InlineKeyboardButton(text="Рейтинг", callback_data="RatingAnime")
      but_3 = types.InlineKeyboardButton(text="Тип (Полн/Коротк)", callback_data="TypeAnime")
      but_4 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="Anime")
    elif type is TypeSearch.Manga:
      but_1 = types.InlineKeyboardButton(text="Жанры", callback_data="GenresManga")
      but_2 = types.InlineKeyboardButton(text="Рейтинг", callback_data="RatingManga")
      but_3 = types.InlineKeyboardButton(text="Тип (Полн/Коротк)", callback_data="TypeManga")
      but_4 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="Manga")
    but_5 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
    key.row(but_1)
    key.row(but_2)
    key.row(but_3)
    key.row(but_4, but_5)
    return key

# получить меню жанров
def getGenresMenu(genresList, type):
    key = types.InlineKeyboardMarkup()
    count_col = 0
    but_row = []
    for item, id in genresList.items():
      if count_col < 2:
        but_row.append(types.InlineKeyboardButton(text=item, callback_data=item))
        count_col += 1
      elif count_col == 2:
        but_row.append(types.InlineKeyboardButton(text=item, callback_data=item))
        count_col = 0
        key.row(but_row[0], but_row[1], but_row[2])
        but_row = []
    if count_col == 1:  
      key.add(but_row[0])
    elif count_col == 2:
      key.row(but_row[0], but_row[1])
    
    if type is TypeSearch.Anime:
      but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterAnime")
    elif type is TypeSearch.Manga:
      but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterManga")
    but_2 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
    key.row(but_1, but_2)
    return key

# получаем меню Новинок для аниме
def getNovinkiMenuAnime(name, genres, score, description, siteInfo, siteVideo):
    key = types.InlineKeyboardMarkup()
    # если ссылка существует
    if siteVideo is not None:
      but_1 = types.InlineKeyboardButton(text="Смотреть", url=siteVideo)
      key.row(but_1)
    but_2 = types.InlineKeyboardButton(text="Подробнее", url=siteInfo)
    but_3 = types.InlineKeyboardButton(text="В избранное", callback_data="ToFavouritesAnime")
    but_4 = types.InlineKeyboardButton(text="Назад", callback_data="BackAnime")
    but_5 = types.InlineKeyboardButton(text="Вперед", callback_data="NextAnime")
    but_6 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="Anime")
    but_7 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
    genres_str = ""
    for genre in genres:
      genres_str += genre + " | "
    descript = "*Название:* " + name + "\n*Жанры:* " + genres_str + "\n*Рейтинг:* " + str(score) + "\n\n*Описание:* " + description[0:800] + "..." 
    
    key.row(but_2)
    key.row(but_3)
    key.row(but_4, but_5)
    key.row(but_6)
    key.row(but_7)
    return key, descript

# получаем изображение с сайта, изменяем его до нужного размера (чтоб в телеграмме красиво смотрелось)
def getImage(url):
    basewidth = 1200
    baseheight = 800
    image = Image.open(urlopen(url))
    if image.size[1] < baseheight:
      ratio = (baseheight / float(image.size[1]))
      width = int((float(image.size[0]) * float(ratio)))
      image = image.resize((width, baseheight), Image.ANTIALIAS)
    image_fon = Image.new('RGB', (basewidth, image.size[1]), (255, 255, 255))
    image_fon.paste(image, (round((basewidth-image.size[0])/2), 0))
    return image_fon

def getAnime():
    name = "Виви: Песнь флюоритового глаза / Vivy: Fluorite Eye's Song"
    genres = ["Экшен", "Музыка", "Фантастика", "Триллер"]
    score = 8.47
    description = "Добро пожаловать в Ниаленд — выставку искусственного интеллекта и парк, \
    объединивший в себе мечты, надежды и науку. Именно здесь была создана Дива — первый в истории \
    автономный искин-гуманоид, полностью подобный человеку, но существующий только для \
    одной-единственной цели — петь песни и дарить своим слушателям счастье. Не сыскав \
    популярности, Дива Виви, как её назвала одна из первых поклонниц, 12-летняя девочка Момока, \
    продолжала выходить на сцену. Каждый раз она стремилась вложить в свои песни душу, \
    до тех пор пока её размеренному существованию внезапно не пришел конец. Посреди дня к ней \
    подключается Мацумото — таинственный ИИ, представившийся именем своего создателя. По его словам, \
    он прибыл из будущего с задачей предотвратить войну между человечеством и искусственным интеллектом, \
    случившуюся сто лет спустя. Какое будущее ждёт этот мир? Правду ли говорит Мацумото? Сможет ли Дива \
    отказаться от своего первоначального назначения ради спасения человечества? Так начинается история Виви длиной в сотню лет."
    image = "https://nyaa.shikimori.one/system/animes/original/46095.jpg?1620639091"
    siteInfo = "https://shikimori.one/animes/46095-vivy-fluorite-eye-s-song"
    siteVideo = 'https://www.wakanim.tv/ru/v2/catalogue/show/1292/vivi-pesn-flyuoritovogo-glaza-vivy-fluorite-eyes-song'
    return name, genres, score, description, image, siteInfo, siteVideo

# второй аргумент = true, если мы к главной странице возвращаемся, и false при старте бота
def setMainPage(message, edit):
    photo = open('static/avatarka.jpg', 'rb')
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Аниме", callback_data="Anime")
    but_2 = types.InlineKeyboardButton(text="Манги", callback_data="Manga")
    key.add(but_1, but_2)
    if edit:
        bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=types.InputMediaPhoto(photo))
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption="Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный скрасить твое одиночество.\nЧто желаешь посмотреть?".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=key)
    else:
        bot.send_photo(message.chat.id, photo, caption="Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный скрасить твое одиночество.\nЧто желаешь посмотреть?".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=key)

@bot.message_handler(commands=["start"])
def inline(message):
    setMainPage(message, False)    

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    # перешли по кнопке "Аниме"
    if c.data == 'Anime':
      photo = open('static/avatarka.jpg', 'rb')
      key = types.InlineKeyboardMarkup()
      but_1 = types.InlineKeyboardButton(text="Поиск по названию", callback_data="SearchByNameAnime")
      but_2 = types.InlineKeyboardButton(text="Поиск по фильтру", callback_data="FilterAnime")
      but_3 = types.InlineKeyboardButton(text="Посоветуй", callback_data="AdviceAnime")
      but_4 = types.InlineKeyboardButton(text="Новинки", callback_data="NewAnime")
      but_5 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="BackMainPage")
      key.row(but_1)
      key.row(but_2)
      key.row(but_3)
      key.row(but_4)
      key.row(but_5)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Что именно ты хочешь из Аниме?", reply_markup=key)
      #bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Выбери", reply_markup=key)

    # перешли по кнопке "Мангу"
    if c.data == 'Manga':
      photo = open('static/avatarka.jpg', 'rb')
      key = types.InlineKeyboardMarkup()
      but_1 = types.InlineKeyboardButton(text="Поиск по названию", callback_data="SearchByNameManga")
      but_2 = types.InlineKeyboardButton(text="Поиск по фильтру", callback_data="FilterManga")
      but_3 = types.InlineKeyboardButton(text="Посоветуй", callback_data="AdviceManga")
      but_4 = types.InlineKeyboardButton(text="Новинки", callback_data="NewManga")
      but_5 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="BackMainPage")
      key.row(but_1)
      key.row(but_2)
      key.row(but_3)
      key.row(but_4)
      key.row(but_5)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Что именно ты хочешь из Манги?", reply_markup=key)
      #bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Выбери", reply_markup=key)

    # кнопка "Вернуться на главную"
    if c.data == "BackMainPage":
      setMainPage(c.message, True)

    # кнопка "Новинки" для Аниме
    if c.data == "NewAnime":
      name, genres, score, description, url, siteInfo, siteVideo = getAnime()
      image = getImage(url)
      key, descript = getNovinkiMenuAnime(name, genres, score, description, siteInfo, siteVideo)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(image))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption=descript, parse_mode='Markdown', reply_markup=key)

    # кнопка "Новинки" для Мангу
    if c.data == "NewManga":
      name, genres, score, description, url, siteInfo, siteVideo = getAnime() # тут для мангу написать функцию
      image = getImage(url)
      key, descript = getNovinkiMenuAnime(name, genres, score, description, siteInfo, siteVideo) # тут так же для манги
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(image))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption=descript, parse_mode='Markdown', reply_markup=key)

    # избранное для аниме
    if c.data == "ToFavouritesAnime":
      bot.answer_callback_query(c.id, show_alert=True, text="Добавлено в избранное")

    # фильтры для аниме
    if c.data == "FilterAnime":
      photo = open('static/filter.jpg', 'rb')
      key = getFilterMenu(TypeSearch.Anime)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Что отфильтровать?", reply_markup=key)

    # фильтры для мангу
    if c.data == "FilterManga":
      photo = open('static/filterManga.jpg', 'rb')
      key = getFilterMenu(TypeSearch.Manga)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Что отфильтровать?", reply_markup=key)

    # жанры для аниме
    if c.data == "GenresAnime":
      photo = open('static/genres.jpg', 'rb')
      key = getGenresMenu(genresAnime, TypeSearch.Anime)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери жанры", reply_markup=key)

    # жанры для манги
    if c.data == "GenresManga":
      photo = open('static/genresMangu.jpg', 'rb')
      key = getGenresMenu(genresMangu, TypeSearch.Manga)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери жанры", reply_markup=key)

    # при выборе жанра
    if c.data in genresAnime or c.data in genresMangu:
      bot.answer_callback_query(c.id, show_alert=True, text="Выбран жанр: " + c.data + " с id = " + str(genresAnime[c.data]))

bot.polling(none_stop=True)