<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

<a href="https://github.com/german-taxi/starcraft-II-bot">
    <img src="assets/images/german-taxi-gif-logo.gif" alt="animated-logo" height="160" width="160" id="german-taxi-animated-logo" >
</a>

![](/assets/readme_objects/project_title.svg)

<h3 align="center" id="project-title">starcraft-II-bot</h3>

<p align="center" >
    A (not very) intelligent StarCraft II bot
    <br />
    <br />
    <a href="https://github.com/german-taxi/starcraft-II-bot/blob/documentation/README.md"><strong>Explore the docs »</strong></a>
    <br />
</p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary><strong>Table of Contents</strong></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <!-- <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul> -->
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#running">Running the bot</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#docker">Docker</a></li>
    <li><a href="#wsl">WSL</a></li>
    <!-- <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li> -->
  </ol>
</details>
<br /><br />

<!-- ABOUT THE PROJECT -->

## **Prerequisites**

---

-   ### **StarCraft II**

    You'll need a StarCraft II executable. If you are running Windows or macOS, just install the normal SC2 from blizzard app. [The free starter edition works too.](https://us.battle.net/account/sc2/starter-edition/). Linux users get the best experience by installing the Windows version of StarCraft II with [Wine](https://www.winehq.org). Linux user can also use the [Linux binary](https://github.com/Blizzard/s2client-proto#downloads), but it's headless so you cannot actually see the game.
    <br/>

-   ### **Maps**

    You probably want some maps too.
    <br/>

*   #### **Official maps**

    Official Blizzard map downloads are available from [Blizzard/s2client-proto](https://github.com/Blizzard/s2client-proto#downloads).  
     Extract these maps into their respective _subdirectories_ in the SC2 maps directory.  
     e.g. `install-dir/Maps/Ladder2017Season1/`
    <br/>

*   #### **Bot ladder maps**

    Maps that are run on the [SC2 AI Ladder](http://sc2ai.net/) and [SC2 AI Arena](https://aiarena.net/) can be downloaded [from the sc2ai wiki](http://wiki.sc2ai.net/Ladder_Maps) and [the aiarena wiki](https://aiarena.net/wiki/bot-development/getting-started/#wiki-toc-maps).
    **Extract these maps into the *root* of the SC2 maps directory** (otherwise ladder replays won't work).
    e.g. `install-dir/Maps/AcropolisLE.SC2Map`
    <br/>

-   ### [python 3.8](https://www.python.org/downloads/)

```sh
sudo apt install python3.8
```

-   ### [pip](https://pypi.org/project/pip/#description)

```sh
python -m ensurepip --upgrade
```

<br/>
<br/>

## **Installation**

---

### **1. Manual install**

Install the pypi package:

```sh
pip install --upgrade burnysc2
```

or install ir directly from the branch:

```sh
pip install poetry
pip install --upgrade --force-reinstall https://github.com/BurnySc2/python-sc2/archive/develop.zip
```

<br/>

### **2. Using poetry**

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [poetry](https://python-poetry.org/) dependency manager:

```bash
pip install poetry
```

Install the dependencies using poetry:

```bash
poetry install
```

<br/>

## **Running**

---

Simply run the command:

```bash
python3 src/bot.py
```

## **Roadmap**

---

**TODO:**
_Add the roadmap i.e. future updates & features_

<br/>

## **Docker**
---
To containerize the german-taxi bot, simply run:
 ```sh
docker-compose up -d
```

<br/>

## **WSL**

---

Add the following environment variables:

```bash
SC2CLIENTHOST=<IPv4 Address>
SC2SERVERHOST=0.0.0.0
```

You can find your IPv4 Address by typing `ipconfig /all' and searching for the field 'IPv4 Address'

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/german-taxi/starcraft-II-bot?style=for-the-badge
[contributors-url]: https://github.com/german-taxi/starcraft-II-bot/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues-raw/german-taxi/starcraft-II-bot?style=for-the-badge
[issues-url]: https://github.com/german-taxi/starcraft-II-bot/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/german-taxi/starcraft-II-bot/blob/master/LICENSE
