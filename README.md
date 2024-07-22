# astro-rankings

A small Flask server that gets rankings for AstroGame.co

## installation and development

this app uses Docker to build and deploy, run the python script directly to develop locally

install `requirements.txt` locally on your machine use `pip` to develop

see at `http://localhost:8000`

**update**

fixing `docker compose up --watch` TKTK

## endpoints

`/` sends a default message

`/ping` sends `/pong`

`/getRanking` sends the rankings JSON object

`/indun?CharName={CharName}` gets indun info for the day for all characters on that account add `&region={region}` to specify the region, defaults to NA. Regions can be NA/EU/UAE/TH

## data-shape(s)

open data shapes below, try to keep these updated as we expand the API

<details>
<summary>rankings</summary>
once the app hits the 4 game server databases you should receive a JSON object with the following shape

```TypeScript
interface Rankings {
  key: 'NA' | 'EU' | 'TH' | 'UAE'
  data: {
    CharacterImageUrl: URL        // character icon that goes into the badge
    Rank: number                  // 1-5 if possible, EU only has 2 rn
    Value1: number                // character level, see designs
    szID1: string                 // user name
    szID2: string                 // number, used in the char img url but not needed for frontend
  }[]                             // len: 2 - 5 items
}
```

e.g.

```JSON
"EU": [
  {
    "CharacterImageURL": "https://static.latale.com/static/v3/web/img/character/character_41.png",
    "Rank": 1,
    "Value1": 98,
    "szID1": "Popstar988",
    "szID2": "41"
  },
  {
    "CharacterImageURL": "https://static.latale.com/static/v3/web/img/character/character_60.png",
    "Rank": 2,
    "Value1": 95,
    "szID1": "CryBaby",
    "szID2": "60"
  }
]
```
</details>
<details>
  <summary>induns</summary>

    `[
    {
    ActivityType: "Dungeon",
    Count: 1,
    Difficulty: "No Difficulty Set",
    Duration: "0 hours 20 minutes 30 seconds ",
    EntryDate: "Mon, 22 Jul 2024 07:58:07 GMT",
    ExitDate: "Mon, 22 Jul 2024 08:18:37 GMT",
    IndunName: "Theater Eugamon (*Lv. 4000+)",
    ReEnters: 1,
    charName: "KojinGoji"
    }
    ]`



</details>
