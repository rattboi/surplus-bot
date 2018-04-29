# surplus-bot

## Installation

Initial checkout and install:

```
git clone https://github.com/rattboi/surplus-bot
cd surplus-bot
mkvirtualenv -p python3 surplus-bot
pip install -r requirements.txt
```

Setup Slack webhook secret:

```
echo "webhook_url = <your hook>" > surplus/secret.py
```

Setup crontab:

```
#write out current crontab
crontab -l > mycron
echo "*/5 * * * * cd /home/rattboi/surplus-bot && /home/rattboi/.virtualenvs/surplus-bot/bin/python /home/rattboi/surplus-bot/surplus/slack.py"
echo "*/5 * * * * cd /home/rattboi/surplus-bot && /home/rattboi/.virtualenvs/surplus-bot/bin/python /home/rattboi/surplus-bot/surplus/collect.py"
#install new cron file
crontab mycron
rm mycron
```

Now you're done!
