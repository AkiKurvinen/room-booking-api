# Analyysi

## 1. Mitä tekoäly teki hyvin? 

Tekoälyn kanssa pääsi helposti alkuun, koska se osaa kirjoittaa pieniä ohjelmistoja ja funktioita, jotka demonstroivat kirjastojen toimintaa. Kyseinen malli myös selittää uskottavasti, miten kirjasto tai ohjelmisto toimii. Tekoäly on hyvä keksimään vaihtoehtoja ja vertailemaan. Sen avulla löytää myös ratkaisun useimpiin virheilmoituksiin. Tekoälyn kanssa voi keskustella hyvin myös tiedostosta tai koodirivistä ja se osaa selittää laajemmankin ohjelmiston toimintaa.

## 2. Mitä tekoäly teki huonosti?

Mitä suurempaa kokonaisuutta tekoälylle antaa tehtäväksi, sen todennäköisemmin jokin ohjelmistossa hajoaa. Malli on saatettu oppia vanhasta dokumentaatiosta tai keskusteluista ja antaa siksi vastauksena käytöstä poistettuja kirjastoja ja niiden toimintoja. Jos keskusteluhistoriaa ei välillä nollaa AI-agentti saattoi kaivaa takaisin jo korjattuja bugeja tai poistettuja tiedostoja.

## 3. Mitkä olivat tärkeimmät parannukset, jotka teit tekoälyn tuottamaan koodiin ja miksi?

Päätin alkuperäisestä tech stackista, jonka perusteella tekoäly antoi oletuksena yksinkertaisen ohjelmistorakenteen, mikä sopii erinomaisesti demotilanteisiin ja devaaajana opiskeluun. Halusin kuitenkin tehdä ohjelmistosta modulaarisemman ja skaalautuvamman jakamalla API logiikkaa eri tiedostoihin. Lisäsin virtual envin, jotta projektin Python kirjastot eivät sekoita pääympäristöä tietokoneella. Lisäsin dotenvin, jotta kovakoodattuja muuttujia saadaan vähennettyä ja mahdollisella palvelimella julkaistussa versiossa voisi olla oma konfiguraatio esim. tietokannalle. Otin type hintit ja formatterin käyttöön, jotta koodi olisi helpommin ylläpidettävää ja ymmärrettävää. Kirjoitin README dokumentaation ohjelmiston asennukseen ja ajoon yksityiskohtaisesti, jotta taitotasosta riippumatta seuraava devaaja (tai minä itse kuukauden päästä unohtaneena) saa FastAPI projektin käyntiin selaimeen ja löytää Swagger API dokumentaation, jonka pohjalta on hyvä jatkaa.
