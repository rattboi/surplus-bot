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
echo "*/5 * * * * cd /home/rattboi/surplus-bot && /home/rattboi/.virtualenvs/surplus-bot/bin/python /home/rattboi/surplus-bot/surplus/irc.py"
echo "*/5 * * * * cd /home/rattboi/surplus-bot && /home/rattboi/.virtualenvs/surplus-bot/bin/python /home/rattboi/surplus-bot/surplus/collect.py"
#install new cron file
crontab mycron
rm mycron
```

## IRC

The IRC emitter uses IRCFlu (https://github.com/muesli/ircflu) as a client to cat to. IRCFlu opens a socket, and if you netcat something at the port, it says it in the connected channel. You'll need to set up and run the ircflu client as well, if you want to use the IRC emitter.

Now you're done!
