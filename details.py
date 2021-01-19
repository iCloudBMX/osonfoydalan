import bs4
import requests

class info:
    def NamozVaqtlari(self, api):
        result = requests.get(api)
        soup = bs4.BeautifulSoup(result.text, 'lxml')
        current_time = soup.select('.date_time')[0].getText()
        namaz_time = soup.select(".bugun")[0].getText().split('\n')
        natija = f"""Bugun:<b>{current_time}</b>\n\nNamoz vaqtlari⏱:\nBomdod: <b>{namaz_time[4]}</b>\nQuyosh: <b>{namaz_time[5]}</b>\nPeshin: <b>{namaz_time[6]}</b>\nAsr: <b>{namaz_time[7]}</b>\nShom: <b>{namaz_time[8]}</b>\nXufton: <b>{namaz_time[9]}</b>\n\nManba: islom.uz\n@khanblogs"""

        return natija
    
    def ObHavo(self, api, hudud):
        result = requests.get(api)
        soup = bs4.BeautifulSoup(result.text, 'lxml')

        natija = f"""Hudud: <b>{hudud}</b>\nHavo haroroti: <b>{soup.select('#infTemperature')[0].getText()}</b>\n\n🌧Yog'ingarchilik miqdori: <b>{soup.select('#precipitationValue')[0].getText()}</b>\n💦Namlik: <b>{soup.select('#humidityValue')[0].getText()}</b>\n💨Shamol tezligi: <b>{soup.select('#windValue')[0].getText()}</b>\n💥Bosimgarchlik: <b>{soup.select('#pressureValue')[0].getText()}</b>\n\n🌘Tong: <b>{soup.select('#infSunrise')[0].getText()}</b>\n🌦Harorat: <b>{soup.select('#infTempMorning')[0].getText()}</b>\n\n🌕Kunduzi: <b>{soup.select('#infTransit')[0].getText()}</b>\n🌦Harorat: <b>{soup.select('#infTempDay')[0].getText()}</b>\n\n🌒Kechki payt: <b>{soup.select('#infSunset')[0].getText()}</b>\n🌦Harorat: <b>{soup.select('#infTempEvening')[0].getText()}</b>\n\n🌑Tun: <b>{soup.select('#infTwilight')[0].getText()}</b>\n🌦Harorat: <b>{soup.select('#infTempNight')[0].getText()}</b>\n\n@khanblogs"""
        return natija