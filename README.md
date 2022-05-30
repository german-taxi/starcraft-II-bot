<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]

[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
<style>
    #german-taxi-logo {
        border-radius: 20px;
        height: 160px;
        width: 160px;
    }
</style>

  <a href="https://github.com/github_username/repo_name">
    <img src="assets/images/german-taxi-logo.jpg" alt="Logo" width="160" height="160" id='german-taxi-logo' >
  </a>

<style>
    #project-title {
        font-size: 24px;
        font-weight: bold;
        line-height: 32px;
        margin: 10px;
    }
</style>

<h2 align="center" id="project-title">starcraft-II-bot</h2>

<p align="center" >
    A (not very) intelligent StarCraft II bot
    <br />
</p>
</div>

<!-- ABOUT THE PROJECT -->

## Installation

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [poetry](https://python-poetry.org/) dependency manager.

```bash
pip install poetry
```

2. Install the dependencies using poetry

```bash
poetry install
```

## Running the bot

Simply run the command:

```bash
python3 src/Bot.py
```

## WSL config

Add the following environment variables:

```bash
SC2CLIENTHOST=<IPv4 Address>
SC2SERVERHOST=0.0.0.0
```

You can find your IPv4 Address by typing `ipconfig /all' and searching for the field 'IPv4 Address'

## Comments

Po to dar apiforminta labiau bus

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/german-taxi/starcraft-II-bot?style=for-the-badge
[contributors-url]: https://github.com/german-taxi/starcraft-II-bot/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues-raw/german-taxi/starcraft-II-bot?style=for-the-badge
[issues-url]: https://github.com/german-taxi/starcraft-II-bot/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/german-taxi/starcraft-II-bot/blob/master/LICENSE
