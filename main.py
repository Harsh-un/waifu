import telebot
import config
from telebot import types
from PIL import Image
from urllib.request import urlopen
from enum import Enum

from Aggregators.ShikimoriAggregator import ShikimoriItemFilter
from ServerApplication import ServerApplication

# серверное приложение
app = ServerApplication()

id = 0
bot = telebot.TeleBot(config.CFG['TOKEN'])
msg = None
searchName = False  # true если мы перешли в "Поиск по названию"
srchType = None
ratingList = config.ratingList
assessmentList = config.assessmentList
typeAnimeList = config.typeAnimeList
typeMangaList = config.typeMangaList

listOfSelectedGenres = []
ratingSelected = []
assesmentSelected = [] 
typeSelected = []

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
      but_2 = types.InlineKeyboardButton(text="Рейтинг", callback_data="Rating")
      but_3 = types.InlineKeyboardButton(text="Оценка", callback_data="Assesment")
      but_4 = types.InlineKeyboardButton(text="Тип", callback_data="TypeMenu")
      but_5 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="Anime")
      but_6 = types.InlineKeyboardButton(text="Применить фильтр", callback_data="ApplyFilterAnime")
      key.row(but_1)
      key.row(but_2)
    elif type is TypeSearch.Manga:
      but_1 = types.InlineKeyboardButton(text="Жанры", callback_data="GenresManga")
      but_3 = types.InlineKeyboardButton(text="Оценка", callback_data="Assesment")
      but_4 = types.InlineKeyboardButton(text="Тип", callback_data="TypeMenu")
      but_5 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="Manga")
      but_6 = types.InlineKeyboardButton(text="Применить фильтр", callback_data="ApplyFilterManga")
      key.row(but_1)
    but_7 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
    key.row(but_3)
    key.row(but_4)
    key.row(but_5, but_7)
    key.row(but_6)
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
    but_4 = types.InlineKeyboardButton(text="Предыдущее", callback_data="BackAnime")
    but_5 = types.InlineKeyboardButton(text="Следующее", callback_data="NextAnime")
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

# получаем меню Поиска по названию для аниме
def searchNameMenuAnime(name, genres, score, description, siteInfo, siteVideo):
      key = types.InlineKeyboardMarkup()
    # если ссылка существует
      if siteVideo is not None:
        but_1 = types.InlineKeyboardButton(text="Смотреть", url=siteVideo)
        key.row(but_1)

      but_3 = types.InlineKeyboardButton(text="В избранное", callback_data="ToFavouritesAnime")
      #but_4 = types.InlineKeyboardButton(text="Назад", callback_data="BackAnime")
      #but_5 = types.InlineKeyboardButton(text="Вперед", callback_data="NextAnime")
      but_6 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="Anime")
      but_7 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
      genres_str = ""
      for genre in genres:
        genres_str += genre + " | "
      descript = "Название: " + name + "\nЖанры: " + genres_str + "\nРейтинг: " + str(score) + "\n\nОписание: " + description[0:800] + "..."

      if siteInfo is not None:
          but_2 = types.InlineKeyboardButton(text="Подробнее", url=siteInfo)
          key.row(but_2)
      key.row(but_3)
      #key.row(but_4, but_5)
      key.row(but_6)
      key.row(but_7)
      return key, descript

# получаем изображение с сайта, изменяем его до нужного размера (чтоб в телеграмме красиво смотрелось)
def getImage(image):
    basewidth = 1200
    baseheight = 800
    #image = Image.open(urlopen(url))
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

def getAnimeForSearchName():
    name = "Ходячий замок / Howl no Ugoku Shiro"
    genres = ["Приключения", "Драма", "Фэнтези", "Романтика"]
    score = 8.67
    description = "Восемнадцатилетняя шляпница Софи ведёт тихую и ничем не примечательную городскую жизнь. Однако \
    типичный её распорядок рушится, когда в окрестностях города объявляется Ходячий замок Хаула — колдуна, \
    заключившего сделку с демоном огня Кальцифером и носящего дурную славу «похитителя» девичьих сердец. \
    Вечером после работы очаровательный голубоглазый красавец, оказавшийся, как ни странно, самим Хаулом, \
    спасает Софи от приставаний двух солдафонов, и девушка тут же влюбляется в своего спасителя. Однако \
    итогом их встречи становится проклятие Ведьмы Пустоши, превратившее Софи в девяностолетнюю старуху. \
    Теперь Софи вынуждена покинуть родной дом и отправиться на поиски ведьмы, просить ту снять проклятие. \
    Дорога же приводит «девушку» к тому самому Ходячему замку, где у неё и появляется шанс начать новую \
    жизнь... "
    image = "https://kawai.shikimori.one/system/animes/original/431.jpg?1617279661"
    siteInfo = "https://shikimori.one/animes/431-howl-no-ugoku-shiro"
    siteVideo = 'https://hd.kinopoisk.ru/film/4c4086bb916d4d01b984e2d5a8a63005/' #хе-хе, ссылка на кинопоиск
    return name, genres, score, description, image, siteInfo, siteVideo

# второй аргумент = true, если мы к главной странице возвращаемся, и false при старте бота
def setMainPage(message, edit):
    photo = open('static/avatarka.jpg', 'rb')
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Аниме", callback_data="Anime")
    but_2 = types.InlineKeyboardButton(text="Манга", callback_data="Manga")
    key.add(but_1, but_2)
    if edit:
        bot.edit_message_media(chat_id=message.chat.id, message_id=message.message_id, media=types.InputMediaPhoto(photo))
        bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption="Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный скрасить твое одиночество.\nЧто желаешь посмотреть?".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=key)
    else:
        global msg
        msg = bot.send_photo(message.chat.id, photo, caption="Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, созданный скрасить твое одиночество.\nЧто желаешь посмотреть?".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=key)
        #bot.send_photo(message.chat.id, photo, caption="Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный скрасить твое одиночество.\nЧто желаешь посмотреть?".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=key)

@bot.message_handler(commands=["start"])
def inline(message):
    setMainPage(message, False)   

# обработка отправки сообщения пользователя
@bot.message_handler(content_types=['text'])
def send_text(message):
  global searchName
  # если мы в "Поиск по названию"
  if searchName:
    user = app.get_user_session(message.from_user.id)
    user.cur_filter.name = message.text.lower()
    user.cur_iterator = user.cur_aggregator.get_items(user.cur_filter)

    # получили результат поиска
    anime_info = user.cur_iterator.get_item(0)

    if anime_info is not None: #если введенное название есть в наше базе
      img = Image.open(urlopen(anime_info.image_url))
      image = getImage(img)
      siteInfo, siteVideo = None,None
      key, descript = searchNameMenuAnime(anime_info.name, anime_info.genres, anime_info.score, anime_info.description, siteInfo, siteVideo) # тут так же для манги
      #bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(image))
      #bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption=descript, parse_mode='Markdown', reply_markup=key)
      global msg
      bot.delete_message(message.chat.id, msg.message_id)
      msg = bot.send_photo(message.chat.id, image, caption=descript,reply_markup=key)
      #bot.send_photo(message.chat.id, image, caption=descript,reply_markup=key)
    else: 
      key = types.InlineKeyboardMarkup()
      global srchType
      if srchType is TypeSearch.Anime:
        but_2 = types.InlineKeyboardButton(text="Назад", callback_data="Anime")
      elif srchType is TypeSearch.Manga:
        but_2 = types.InlineKeyboardButton(text="Назад", callback_data="Manga")
      key.row(but_2)
      image = Image.open(r'static\searchnameAnime.jpg')
      getImage(image)
      bot.delete_message(message.chat.id, msg.message_id)
      msg = bot.send_photo(message.chat.id, image, caption="Ничего не найдено(", reply_markup=key)
      #bot.send_photo(message.chat.id, image, caption="Ничего не найдено(", reply_markup=key)
      #bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Ничего не найдено, мен(", reply_markup=key)
    searchName = False
  else:
    bot.send_message(message.chat.id, "Не стоит спамить!\nНачни заново")
    bot.delete_message(message.chat.id, msg.message_id)
    setMainPage(message, False)
  


@bot.callback_query_handler(func=lambda c:True)
def inline(c):
    user = app.get_user_session(c.from_user.id)

    # перешли по кнопке "Аниме"
    if c.data == 'Anime':
      user.cur_filter = ShikimoriItemFilter()
      user.cur_aggregator = app.shikimori_anime_agg
      global srchType
      srchType = TypeSearch.Anime
      photo = Image.open(r'static\animeMenu.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      but_1 = types.InlineKeyboardButton(text="Поиск по названию", callback_data="SearchByNameAnime")
      but_2 = types.InlineKeyboardButton(text="Поиск по фильтру", callback_data="FilterAnime")
      but_3 = types.InlineKeyboardButton(text="Для тебя!", callback_data="AdviceAnime")
      but_4 = types.InlineKeyboardButton(text="Новинки", callback_data="NewAnime")
      but_6 = types.InlineKeyboardButton(text="Избранное", callback_data="FavouritesAnime")
      but_5 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="BackMainPage")
      key.row(but_1)
      key.row(but_2)
      key.row(but_3)
      key.row(but_4)
      key.row(but_6)
      key.row(but_5)
      
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Чем могу помочь?", reply_markup=key)
      #bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Выбери", reply_markup=key)

    # перешли по кнопке "Манга"
    if c.data == 'Manga':
      user.cur_filter = ShikimoriItemFilter()
      user.cur_aggregator = app.shikimori_manga_agg
      srchType = TypeSearch.Manga
      photo = Image.open(r'static\mangaMenu.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      but_1 = types.InlineKeyboardButton(text="Поиск по названию", callback_data="SearchByNameManga")
      but_2 = types.InlineKeyboardButton(text="Поиск по фильтру", callback_data="FilterManga")
      but_3 = types.InlineKeyboardButton(text="Для тебя!", callback_data="AdviceManga")
      but_4 = types.InlineKeyboardButton(text="Новинки", callback_data="NewManga")
      but_6 = types.InlineKeyboardButton(text="Избранное", callback_data="FavouritesManga")
      but_5 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="BackMainPage")
      key.row(but_1)
      key.row(but_2)
      key.row(but_3)
      key.row(but_4)
      key.row(but_6)
      key.row(but_5)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Чем могу помочь?", reply_markup=key)
      #bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Выбери", reply_markup=key)

    # кнопка "Вернуться на главную"
    if c.data == "BackMainPage":
      setMainPage(c.message, True)
    
    # кнопка "Новинки" для Аниме
    if c.data == "NewAnime":
      name, genres, score, description, url, siteInfo, siteVideo = getAnime()
      img = Image.open(urlopen(url))
      image = getImage(img)
      key, descript = getNovinkiMenuAnime(name, genres, score, description, siteInfo, siteVideo)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(image))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption=descript, parse_mode='Markdown', reply_markup=key)

    # кнопка "Новинки" для Манги
    if c.data == "NewManga":
      name, genres, score, description, url, siteInfo, siteVideo = getAnime() # тут для манги написать функцию
      img = Image.open(urlopen(url))
      image = getImage(img)
      key, descript = getNovinkiMenuAnime(name, genres, score, description, siteInfo, siteVideo) # тут так же для манги
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(image))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption=descript, parse_mode='Markdown', reply_markup=key)
    
    #поиск по названию аниме
    if c.data == "SearchByNameAnime":
      global searchName
      searchName = True
      photo = Image.open(r'static\searchnameAnime.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Введи название:", reply_markup=key)
      key = types.KeyboardButton

    #поиск по названию аниме
    if c.data == "SearchByNameManga":
      searchName = True
      photo = Image.open(r'static\searchnameAnime.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Введи название:", reply_markup=key)
      key = types.KeyboardButton
        

    # избранное для аниме
    if c.data == "ToFavouritesAnime":
      bot.answer_callback_query(c.id, show_alert=True, text="Добавлено в избранное")
    #просмотреть избранное для аниме
    if c.data == "FavouritesAnime":
      bot.answer_callback_query(c.id, show_alert=True, text="Здесь будет все, что Вы добавили в избранное")
    #посмотреть избранное для манги
    if c.data == "FavouritesManga":
      bot.answer_callback_query(c.id, show_alert=True, text="Здесь будет все, что Вы добавили в избранное")
    
    # фильтры для аниме
    if c.data == "FilterAnime":
      photo = Image.open(r'static\filter.jpg')
      photo = getImage(photo)
      key = getFilterMenu(TypeSearch.Anime)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Укажи свои предпочтения:", reply_markup=key)

    # фильтры для манги
    if c.data == "FilterManga":
      photo = Image.open(r'static\filterManga.jpg')
      photo = getImage(photo)
      key = getFilterMenu(TypeSearch.Manga)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Укажи свои предпочтения:", reply_markup=key)
    
    # жанры для аниме
    if c.data == "GenresAnime":
      photo = Image.open(r'static\genres.jpg')
      photo = getImage(photo)
      key = getGenresMenu(genresAnime, TypeSearch.Anime)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери жанры:", reply_markup=key)

    # жанры для манги
    if c.data == "GenresManga":
      photo = Image.open(r'static\genresMangu.jpg')
      photo = getImage(photo)
      key = getGenresMenu(genresMangu, TypeSearch.Manga)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери жанры:", reply_markup=key)

    # при выборе жанра
    if c.data in genresAnime or c.data in genresMangu:
      bot.answer_callback_query(c.id, show_alert=True, text="Выбран жанр: " + c.data + " с id = " + str(genresAnime[c.data]))
      listOfSelectedGenres.append(c.data)

    # меню для выбора Рейтинга
    if c.data == "Rating":
      photo = Image.open(r'static\ratingAnime.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      for item, id in ratingList.items():
        but = types.InlineKeyboardButton(text=item, callback_data=item)
        key.row(but)
      if srchType is TypeSearch.Anime:
        but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterAnime")
      elif srchType is TypeSearch.Manga:
        but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterManga")
      but_2 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
      key.row(but_1, but_2)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери рейтинг", reply_markup=key)

    # при выборе рейтинга
    if c.data in ratingList:
      bot.answer_callback_query(c.id, show_alert=True, text="Выбран рейтинг: " + c.data + " с id = " + str(ratingList[c.data]))
      ratingSelected.append(c.data)

    # меню для выбора Оценки
    if c.data == "Assesment":
      photo = Image.open(r'static\assesment.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      for item, id in assessmentList.items():
        but = types.InlineKeyboardButton(text=item, callback_data=item)
        key.row(but)
      if srchType is TypeSearch.Anime:
        but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterAnime")
      elif srchType is TypeSearch.Manga:
        but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterManga")
      but_2 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
      key.row(but_1, but_2)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери оценку:", reply_markup=key)

    # при выборе оценки
    if c.data in assessmentList:
      bot.answer_callback_query(c.id, show_alert=True, text="Выбрана оценка: " + c.data + " с id = " + str(assessmentList[c.data]))
      assesmentSelected.append(c.data)

    # меню для выбора Типы для аниме
    if c.data == "TypeMenu":
      photo = Image.open(r'static\typeAnime.jpg')
      photo = getImage(photo)
      key = types.InlineKeyboardMarkup()
      if srchType is TypeSearch.Anime:
        lst = typeAnimeList
      else:
        lst = typeMangaList
      for item, id in lst.items():
        but = types.InlineKeyboardButton(text=item, callback_data=item)
        key.row(but)
      if srchType is TypeSearch.Anime:
        but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterAnime")
      elif srchType is TypeSearch.Manga:
        but_1 = types.InlineKeyboardButton(text="Вернуться назад", callback_data="FilterManga")
      but_2 = types.InlineKeyboardButton(text="На главную", callback_data="BackMainPage")
      key.row(but_1, but_2)
      bot.edit_message_media(chat_id=c.message.chat.id, message_id=c.message.message_id, media=types.InputMediaPhoto(photo))
      bot.edit_message_caption(chat_id=c.message.chat.id, message_id=c.message.message_id, caption="Выбери тип:", reply_markup=key)

    # при выборе Типа
    if c.data in typeAnimeList or c.data in typeMangaList:
      if srchType is TypeSearch.Anime:
        bot.answer_callback_query(c.id, show_alert=True, text="Выбран Тип: " + c.data + " с id = " + str(typeAnimeList[c.data]))
      else:
        bot.answer_callback_query(c.id, show_alert=True, text="Выбран Тип: " + c.data + " с id = " + str(typeMangaList[c.data]))
      typeSelected.append(c.data)

    # Применить фильтры
    if c.data == "ApplyFilterAnime" or c.data == "ApplyFilterManga":
      bot.answer_callback_query(c.id, show_alert=True, text= "Жанры: " + ', '.join(listOfSelectedGenres) + "\nРейтинг: " + ''.join(ratingSelected) + "\nТип: " + ''.join(typeSelected) + "\nОценка: " + ''.join(assesmentSelected))

    # при запросе следующего аниме
    if c.data == "NextAnime":
      bot.answer_callback_query(c.id, show_alert=True, text="Хотим получить следующее аниме")

    # при запросе следующего аниме
    if c.data == "BackAnime":
      bot.answer_callback_query(c.id, show_alert=True, text="Хотим получить предыдущее аниме")

    # при запросе следующего манги
    if c.data == "NextManga":
      bot.answer_callback_query(c.id, show_alert=True, text="Хотим получить следующее аниме")

    # при запросе следующего манги
    if c.data == "BackManga":
      bot.answer_callback_query(c.id, show_alert=True, text="Хотим получить предыдущее аниме")


if __name__ == "__main__":
    bot.polling(none_stop=True)