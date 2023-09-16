# Deepsea Project

Video 1 Overview: https://youtu.be/voJkZl06sJk

Video 2 Code review: https://youtu.be/g8XcRRyUcRQ

The purpose of the project is to setup an environment to emulate a vessel emitting sensor data a to server, which normalizes and graphs the data.

The environment is configured with Docker Compose. There are 3 containers which represent the following elements:

•	Emitter – This container emulates a vessel sending sensor info to Project.

•	Meteo – This container emulates a meteorological endpoint that can be queried for sea currents data. The endpoint updates every 10 minutes.

•	Project – This container is the main component which processes the data. It receives sensor data from Emitter, queries Meteo for sea current. It runs the frontend for graphing and backend, both in Django. It hosts the DB as a SQLite file.
