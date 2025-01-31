
# My first Python project ever - Library

This is my first python project I created during Python course as an midterm assesment of Python basics. 


Download project:
```python
git clone https://github.com/gts446/1_tarpinis.git
```

Install streamlit
```python
pip install streamlit
```

Start app


```python
streamlit run main.py
```

Once streamlit server is running, you should be able to access app through web browser on `http://localhost:8501/` 


Demo libriarian
username `admin919` 
pass `admin`
## Project requirements (LT)

### Privalomas funkcionalumas

Įsivaizduokite, kad buvote pasamdyti sukurti paprastą bibliotekos valdymo python programą, ši programa turėtų galėti atlikti šias funkcijas:

- Turėtų būti galima pridėti naują į knygą į biblioteką (knyga, privalo turėti bent, autorių pavadinimą išleidimo metus ir žanrą .
- Turėtų būti galima pašalinti senas/nebenaudojamas knygas, galima daryti pagal išleidimo metus, jeigu senesnis nei x išmetam.
- Skaitytojai turėtų galėti pasiimti knygą išsinešimui (knygų kiekis ribotas)
- Turėtų būti galimybė ieškoti knygų bibliotekoje, pagal knygos pavadinimą arba autorių.
- Knygos išduodamos tik tam tikram laikui, jeigu knygos negrąžinamos iki išduotos datos, jos skaitomos vėluojančiomis (angl. Overdue).
- Turi būti galima peržiūrėti visas bibliotekos knygas
- Turi būti galima peržiūrėti visas vėluojančias knygas
- Turi būti neleidžiama pasiimti knygos, jeigu skaitytojas turi vėluojančią knygą ir jis turi būti įspėtas, kad knyga vėluoja
 

 

### Papildomas funkcionalumas

- Knygas galima pasiimti tik su skaitytoje kortele, skaitytojo korteles reikia galėti užregistruoti ir priskirti naudotojui.
- Turėtų būti galimybė išvesti statistiką, koks yra vidutinis vėluojančių knygų kiekis ir kitus aktualius rodiklius, tokius kaip, kokio žanro knygų yra daugiausiai, kokio žanro knygas, dažniausiai ima skaitytojai ir t.t
- Dvi rolės bibliotekininkas ir skaitytojas, bibliotekininkas prisijungia įvedę naudotojo vardą ir slaptažodį, o skaitytojas savo skaitytojo kortelės numerį. Skaitytojas negali pridėti/išimti knygų.
- Paleiskite programą per streamlit
- Naudojama virtuali aplinka viso darbo metu (tinka tiek venv tiek poetry)
 

 

 

### Būtinos sąlygos

- Nerašome visko viename faile (turi būti laikomasi, bent minimalios struktūros)
- Programa turi veikti tol, kol bus išjungta, naudotojo pageidavimu
- Pridėtos/pašalintos knygos, turi išlikti tarp programos paleidimų (vadinasi viskas saugoma faile)
- Informacija saugome pkl/csv/json/txt failuose
- Programa negali "nulūžti" (už kiekvieną vietą, kurioje lūžta, minus balai)
- Programoje viskas turi būti funkcijose/metoduose klasėse. Globaliai jie gali būti tik -  kviečiami, bet visi skaičiavimai būtent šiose struktūrose.
- Privaloma naudoti GitHub ir turėti logiškus commit pavadinimus, bent 3 šakas sukurtas projekto metu ir bent 5 commitai (commitai neturėtų būti labai dideli, po vieną funkcionalumą vienas commitas)