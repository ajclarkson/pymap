# PyMAP
Pythonic control of all of your inboxes.

PyMAP exists to provide scripting support for email processing that is client agnostic. After too long trying to maintain various AppleScript solutions and such I decided to start building this collection.

At present, it focuses on a key area of email processing "Followups"

## PyMAP ReplyReminder

It's all too easy to forget that you have an email sat waiting for you to reply to it. We've all done it. Personally I started keeping them in a folder called "Pending", but how often do I remember to check that?

**PyMAP ReplyReminder** is designed to interrogate your "Pending" folder and send you a helpful reminder as to how much you are neglecting it. Simply see the instructions below on how to configure with a `~/.pymaprc` file, then schedule pymap to run as a cronjob as often as you would like. (The following cron command will also create a log file in your pymap directory, rather than having output emailed to you.)

```
50 08 * * * /path/to/repo/pymap/bin/pymap > /path/to/repo/pymap.log
```

When it runs, you'll get a friendly reminder of how many emails are in your pending folder, and a random selection of 5 subjects and from addresses to jog your memory. PyMAP ReplyReminder should intelligently ignore messages that are all within one conversation, so you **should** only see the most recent email from that thread. It is still under development, so bear with me if that isn't the case, it's early days!

## Future

I'm also aiming to expand it to do the other side of reminders too. Namely a 'waiting' folder where you can dump all of the mail you are waiting for a reply on, and if you haven't had one in a set number of days, PyMAP will prompt you to follow up on the email. That's coming real soon.

## Configuration

PyMAP simply requires you to have a correctly formatted `~/.pymaprc` file:

```
[config]
name = Adam # The name PyMAP should address you by

[account_personal]
host = imap.server.com # imap host...
user = me@example.com # your login username
pass = mypassword # your password
email_address = me@example.com # incase it's different to your username
followup_folder = Pending # name of your neglected follow up folder

[account_work]
host = imap.server.com
...
followup_folder = Pending

[account_anythingyouwant]
host = imap.server.com
...
followup_folder = Pending
```

It's that simple. You can have as many accounts listed as you like, as long as they start with `account_` in the section name, they'll be processed just the same.

## Changelog

- `v0.1` It's pretty basic, but it works! ReplyReminders fire straight into your inbox