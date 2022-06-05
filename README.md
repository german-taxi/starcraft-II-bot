<!-- PROJECT SHIELDS -->

# starcraft-II-bot

[![Contributors][contributors-shield]][contributors-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

---

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
python3 src/bot.py
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

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/german-taxi/starcraft-II-bot/graphs/contributors
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/german-taxi/starcraft-II-bot/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/german-taxi/starcraft-II-bot/blob/master/LICENSE
