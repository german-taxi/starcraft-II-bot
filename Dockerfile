# Set up StarCraft II Test Environment for python-sc2 bots
ARG PYTHON_VERSION=3.8

# Use an official debian stretch slim release as a base image
FROM python:$PYTHON_VERSION-slim
LABEL GERMANTAXI="germantaxi@fakegmail.com"

ARG SC2_VERSION=4.10

# Debugging purposes
RUN echo $PYTHON_VERSION
RUN echo $SC2_VERSION

USER root

# Update system
RUN apt-get update \
    && apt-get upgrade --assume-yes --quiet=2

RUN apt-get install --assume-yes --no-install-recommends --no-show-upgraded \
    git  \
    unzip \
    wget \
    rename \
    tree

WORKDIR /root/

# Download and uncompress StarCraftII from https://github.com/Blizzard/s2client-proto#linux-packages and remove zip file
RUN wget --quiet --show-progress --progress=bar:force http://blzdistsc2-a.akamaihd.net/Linux/SC2.$SC2_VERSION.zip \
    && unzip -q -P iagreetotheeula SC2.$SC2_VERSION.zip \
    && rm SC2.$SC2_VERSION.zip

# Remove Battle.net folder
RUN rm -rf /root/StarCraftII/Battle.net/* \
    # Remove Shaders folder
    && rm -rf /root/StarCraftII/Versions/Shaders*

# Create a symlink for the maps directory
RUN ln -s /root/StarCraftII/Maps /root/StarCraftII/maps \
    # Remove the Maps that come with the SC2 client
    && rm -rf /root/StarCraftII/maps/*

# Change to maps folder
WORKDIR /root/StarCraftII/maps/

# Get sc2ai.net ladder maps
RUN wget --quiet --show-progress --progress=bar:force \
    http://archive.sc2ai.net/Maps/Season1Maps.zip \
    http://archive.sc2ai.net/Maps/Season2Maps.zip \
    http://archive.sc2ai.net/Maps/Season3Maps.zip \
    http://archive.sc2ai.net/Maps/Season4Maps.zip \
    http://archive.sc2ai.net/Maps/Season5Maps.zip \
    http://archive.sc2ai.net/Maps/Season6Maps.zip \
    http://archive.sc2ai.net/Maps/Season7Maps.zip \
    http://archive.sc2ai.net/Maps/Season8Maps.zip \
    http://archive.sc2ai.net/Maps/Season9Maps.zip \
    http://archive.sc2ai.net/Maps/Season10Maps.zip \
    && unzip -q -o '*.zip' \
    && rm *.zip 

# Get official blizzard maps
RUN wget --quiet --show-progress --progress=bar:force http://blzdistsc2-a.akamaihd.net/MapPacks/Ladder2019Season3.zip \
    && unzip -q -P iagreetotheeula -o 'Ladder2019Season3.zip' \
    && mv Ladder2019Season3/* . \
    && rm Ladder2019Season3.zip \
    && rm -r Ladder2019Season3 

# Get v5.0.6 maps
RUN wget --quiet --show-progress --progress=bar:force https://github.com/shostyn/sc2patch/raw/master/Maps/506.zip \
    && unzip -q -o '506.zip' \
    && rm 506.zip

# Get flat and empty maps
RUN wget --quiet --show-progress --progress=bar:force http://blzdistsc2-a.akamaihd.net/MapPacks/Melee.zip \
    && unzip -q -P iagreetotheeula -o 'Melee.zip' \
    && mv Melee/* . \
    && rm Melee.zip \
    && rm -r Melee

# Remove LE suffix from file names

# List all map files
RUN tree

WORKDIR /root/

COPY src/. /root/StarCraftII/bots/germantaxi/
RUN python -m pip install --upgrade https://github.com/BurnySc2/python-sc2/archive/develop.zip 
WORKDIR /root/StarCraftII/

CMD ["/root/StarCraftII/bots/germantaxi/bot.py"]



# ENTRYPOINT [ "python", "/root/StarCraftII/bots/germantaxi/bot.py" ]
# ENV PYTHONPATH=/root/aiarena-client/:/root/aiarena-client/arenaclient/:/root/.local/bin
# ENV HOST 0.0.0.0