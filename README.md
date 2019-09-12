## SpråkFårk ##
![illustrerende gif](https://raw.githubusercontent.com/Roxedus/SprokFork/dev/.assets/vis.gif)


Discord-programvareagent som reagerer på bruken av lånord, og foreslår norske alternativer.
Henter informasjon fra nettsidene til [Språkrådet](https://www.sprakradet.no/sprakhjelp/Skriverad/Avloeysarord/)

## Oppsett
Prosjektet er skrevet i Python, og kan derfor kjøres nesten over alt. Jeg tilbyr også et [docker bilde](https://hub.docker.com/r/si0972/sprokfork).

Jeg drifter også en åpen bot, som du kan invitere som du kan [invitere](https://discordapp.com/oauth2/authorize?client_id=532190477978697748&permissions=2048&scope=bot) til din server.

<details>
    <summary>Manuelt</summary>
  
For å sette opp programvaren, må du ha Python 3,6 eller nyere.
    
    
```bash
git clone https://github.com/Roxedus/SprokFork sprokfork
python -m pip install -r /sprokfork/requirements.txt
cp /sprokfork/data/conf.example.json /sprokfork/data/conf.json
```
 
</details>



<details>
  <summary>Docker</summary>
  
Eksempel docker-compose.yml

```yml
  fork:     
    container_name: SprokFork
    image: si0972/sprokfork:latest
    networks:
      - internal
    volumes:
      - ./sprokfork:/app/data
```
  
</details>


Opprett en [bot-token](https://discordapp.com/developers/docs/topics/oauth2#bots), og fyll inn token-feltet i Opprett en [bot-token](https://discordapp.com/developers/docs/topics/oauth2#bots), og fyll inn token-feltet i `/sprokfork/data/conf.json`

Du er nå klar til å starte. 
