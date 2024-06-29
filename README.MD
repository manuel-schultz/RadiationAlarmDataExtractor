# RadiationAlarmDataExtractor

# What is RadiationAlarmDataExtractor
Well, the austrian government has about 110 (at this time 111) sensors in the country that store data once an hour. This data is available by the public, so I build a script that can grab this data from their API and save it in a local db. Unfortunately the data is only available for 200 days so we have to store it on our end so that we have a full overfiew.

In another step, I will create a frontend program that can retrieve the data from the database and display it for an understandable User Experience because right now it only saves the data to the database but will not display it.

# Used Technologies
- **Python** 3.10.12
- **SQLite**

# More Links about the system
- [Bundesministerium zum Thema Strahlenfrühwarnsystem](https://www.bmk.gv.at/themen/klima_umwelt/strahlenschutz/fruehwarnsystem/strahlenfruehwarnsystem.html)
- [**PDF**: Das österreichische Strahlenfrühwarnsystem - Jahresbericht 2023 - By Bundesministerium Klimaschutz, Umwelt, Mobilität, Innovation und Technologie](https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.bmk.gv.at/dam/jcr:9d2f1bfe-e6fc-4b09-b607-7c0df5c9d25f/SFWS_2023_20240402.pdf&ved=2ahUKEwibk4yN24CHAxWR8LsIHe1gB9UQFnoECA8QAw&usg=AOvVaw1htti6_z2J2QsAsz-3-IuS)
- [Österreich Karte mit aktuellen Messungen](https://sfws.lfrz.at/)
- [Strahlenfrühwarnsystem API Dokumentation](https://sfws.lfrz.at/json.php)