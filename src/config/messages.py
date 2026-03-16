from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parents[1] / "assets"

TG_EYE = '<tg-emoji emoji-id="6251187387360085896">👁️</tg-emoji>'
TG_FIRE = '<tg-emoji emoji-id="5440848567524677660">🔥</tg-emoji>'
TG_FISHING = '<tg-emoji emoji-id="5188322825735267247">🎣</tg-emoji>'
TG_CAR = '<tg-emoji emoji-id="5190458184690588640">🏎️</tg-emoji>'
TG_GIFT = '<tg-emoji emoji-id="5242716091163101659">🎁</tg-emoji>'
TG_HUNDRED = '<tg-emoji emoji-id="5341498088408234504">💯</tg-emoji>'
TG_ICE = '<tg-emoji emoji-id="5334544901428229844">🧊</tg-emoji>'
TG_ROCKET = '<tg-emoji emoji-id="5188481279963715781">🚀</tg-emoji>'
TG_LIGHTNING = '<tg-emoji emoji-id="5456140674028019486">⚡</tg-emoji>'
TG_MONEY = '<tg-emoji emoji-id="5316709465616031741">💸</tg-emoji>'
TG_TARGET = '<tg-emoji emoji-id="5213297669719491128">🎯</tg-emoji>'
TG_ARROW = '<tg-emoji emoji-id="5416117059207572332">➤</tg-emoji>'
TG_WHEEL = '<tg-emoji emoji-id="5213149166930267840">🎡</tg-emoji>'
TG_LINK = '<tg-emoji emoji-id="5460795821576443427">🔗</tg-emoji>'
TG_ONE = '<tg-emoji emoji-id="5440377203453885642">1️⃣</tg-emoji>'
TG_TWO = '<tg-emoji emoji-id="5438538369040678177">2️⃣</tg-emoji>'
TG_THREE = '<tg-emoji emoji-id="5440601121573861927">3️⃣</tg-emoji>'
TG_DOWN = '<tg-emoji emoji-id="5231102735817918643">👇</tg-emoji>'

BOT_PLAY_URL = "https://t.me/jet_slotmania_bot?start=cfrWd8oo4au"
SITE_PLAY_URL = "https://jetton.direct/cfrWd8oo4au?click_id=%7Bclick_id%7D"
PLAY_BUTTONS = [
    {"text": "Играть в боте", "url": BOT_PLAY_URL},
    {"text": "Играть на сайте", "url": SITE_PLAY_URL},
]

RANDOM_MESSAGES = [
    {
        "image_path": str(ASSETS_DIR / "random_message_1.jpg"),
        "caption": f"""
{TG_FIRE}<b>ТУРБИНА УДАЧИ ДЛЯ НОВЫХ ИГРОКОВ</b>{TG_ROCKET}

{TG_ARROW} <b>Регистрируйся</b> и заходи с промо
{TG_GIFT} <b>Крути колесо</b> — забирай до <b>80 000₽</b> на баланс
{TG_HUNDRED} <b>Бонус:</b> <b>250 FS + 425%</b> к депозиту

{TG_LIGHTNING}<b>Время ограничено</b> — активируй бонус прямо сейчас
""".strip(),
        "buttons": PLAY_BUTTONS,
    },
    {
        "image_path": str(ASSETS_DIR / "random_message_2.jpg"),
        "caption": f"""
{TG_MONEY}<b>ТЫ ПОЛУЧИЛ БОНУС ДЛЯ СТАРТА</b>

{TG_TARGET} <b>425% + 250 FS</b> новым игрокам
{TG_WHEEL} <b>Без депа</b> — крути колесо после регистрации
{TG_FIRE} <b>Доп. бонусы</b> и акции доступны сразу после входа

{TG_DOWN} Нажимай кнопку ниже и активируй предложение
""".strip(),
        "buttons": PLAY_BUTTONS,
    },
    {
        "image_path": str(ASSETS_DIR / "random_message_3.jpg"),
        "caption": f"""
{TG_GIFT}<b>ЗАБЕРИ СВОЙ БОНУС ПРЯМО СЕЙЧАС</b>

{TG_ONE} <b>Зарегистрируйся</b> по ссылке ниже
{TG_TWO} <b>Крути турбину</b> и забирай до <b>80 000₽</b>
{TG_THREE} <b>Пополняй баланс</b> и получай <b>250 FS + 425%</b>

{TG_LINK} <b>Промо уже активно</b> — не пропусти
""".strip(),
        "buttons": PLAY_BUTTONS,
    },
    {
        "image_path": str(ASSETS_DIR / "random_message_4.jpg"),
        "caption": f"""
{TG_EYE}<b>ВСЕ ИГРЫ ИЗ ВИДЕО ТУТ</b>{TG_EYE}

{TG_FIRE} <b>MINESLOT 2</b> — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>
{TG_CAR} <b>RUSH HOUR</b> — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>
{TG_FISHING} <b>ICE FISHING</b> — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>

{TG_GIFT} <b>Бонус:</b> до <b>80 000₽</b> на баланс
{TG_HUNDRED} <b>Депозит:</b> <b>250 FS + 425%</b>
""".strip(),
        "buttons": PLAY_BUTTONS,
    },
]

JOIN_REQUEST_MESSAGE = {
    "image_path": str(ASSETS_DIR / "random_message_1.jpg"),
    "caption": f"""
{TG_EYE}<b>ВСЕ ИГРЫ ИЗ ВИДЕО ТУТ</b>{TG_EYE}

{TG_FIRE}MINESLOT 2 (NEW) — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>
{TG_CAR}RUSH HOUR (МАШИНЫ) — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>
{TG_FISHING}ICE FISHING(РЫБАЛКА) — <a href="https://clck.ru/3QbX4Q">ИГРАТЬ</a>

{TG_GIFT}<i>КРУТИ КОЛЕСО И ЗАБИРАЙ ДО 80.000₽ НА БАЛАНС К ДЕПОЗИТУ:</i>

{TG_HUNDRED}Вноси депозит и получай бонус: <b><u>250FS + 425% к пополнениям</u></b> {TG_ICE}
""".strip(),
    "buttons": PLAY_BUTTONS,
}

FIXED_MESSAGE_IMAGE_PATH = str(ASSETS_DIR / "fixed_message.jpg")

FIXED_MESSAGE = f"""
{TG_FIRE}<b>ПОДПИСЫВАЙСЯ НА МОЙ ТЕЛЕГРАММ</b>

<i>Регулярные конкурсы и розыгрыши бонусов</i>
<i>Индивидуальные мемы для тгк</i>
<i>Топовое комьюнити - уважаем друг друга</i>

{TG_LINK} https://t.me/budkamelona
{TG_LINK} https://t.me/budkamelona
{TG_LINK} https://t.me/budkamelona
""".strip()
