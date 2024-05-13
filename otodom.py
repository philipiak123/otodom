import requests
from bs4 import BeautifulSoup
import mysql.connector
import datetime
import re

mydb = mysql.connector.connect(
    host="Filippoxox123.mysql.pythonanywhere-services.com",
    user="Filippoxox123",
    password="Scrapping",
    database="Filippoxox123$default"
)

mycursor = mydb.cursor()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
a=3
d=0
mieszkanie = []
mie = []
linki = []
cena = []
cenam = []
pokoje = []
metr = []
pietr = []

for a in range(1, 3):
    b=str(a)
    url = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie,rynek-wtorny/podlaskie/bialystok/bialystok/bialystok?limit=72&ownerTypeSingleSelect=ALL&priceMax=500000&pricePerMeterMax=8000&by=DEFAULT&direction=DESC&viewType=listing"
    response = requests.get(url, headers=headers)
    respone = response.text
    soup = BeautifulSoup(respone, 'lxml')
    ceny = soup.find_all('span', class_="css-1uwck7i e1a3ad6s0")
    mieszkania = soup.find_all('a', class_="css-16vl3c1 e1x0p3r10")
    others = soup.find_all('div', class_="css-1c1kq07 e12r8p6s0")
    for c in ceny:
        cena_text = c.text.replace(' zł', '').replace('zł', '').replace('\xa0', '').replace(' ', '') # Usunięcie 'zł', spacji i niepotrzebnych znaków
        cena_int = int(cena_text) # Konwersja na liczbę całkowitą
        cena.append(cena_int)
    for m in mieszkania:
        mieszkanie.append(m.text)
    for m in mieszkania:
        linki.append("otodom.pl/"+m['href'])
for i in others:
    tekst = i.text
    liczba_pokoi = int(re.search(r'Liczba pokoi(\d+)', tekst).group(1))
    powierzchnia = float(re.search(r'Powierzchnia([\d.]+) m²', tekst).group(1))
    cena_metr = int(re.search(r'Cena za metr kwadratowy(\d+)\s*zł/m²', tekst).group(1))
    pietro_match = re.search(r'Piętro(\d+)', tekst)
    pietro = pietro_match.group(1) if pietro_match else None

    pietr.append(pietro)
    metr.append(powierzchnia)
    pokoje.append(liczba_pokoi)
    cenam.append(cena_metr)

for i in range(len(mieszkanie)):

    sql = "INSERT INTO mieszkania (nazwa, cena, cenam, pokoi, metrow, pietro, link) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (mieszkanie[i], cena[i], cenam[i], pokoje[i], metr[i], pietr[i], linki[i])
    mycursor.execute(sql, val)

    mydb.commit()
mydb.close()
