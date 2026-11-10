# A Magical Program to Aggregate Solar Data at EMU

Pulls data from the Satcon 100kW inverter at Sadie-Hartzler Library using POST requests to the API I found while monitoring network requests. This gets the same data visible in the public graphs, down to 5 minutes.

The two installs on Roselawn and University Commons (UC) do not have an API, so I instead download the CSV files from them (accurate to a minute) and parse them with pandas. It appears they might try to rate limit you and eventually block your IP for an amount of time... I need to look into it more.