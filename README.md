# Telegram Bot on Vercel (Python + Flask)

## Quick Start
1) Create a bot with @BotFather and copy your **token**.
2) Deploy this repo to Vercel.
3) In Vercel → Project → **Settings → Environment Variables**, add:
   - `BOT_TOKEN` = `123456789:ABCDEF...`
   Make sure it's set for **Production** and **Preview**.
4) After deploy, copy your project domain (e.g. `https://your-bot.vercel.app/`).
5) Set Telegram webhook (replace `<TOKEN>` and `<YOUR_DOMAIN>`):
```
https://api.telegram.org/bot<TOKEN>/setWebhook?url=<YOUR_DOMAIN>/
```
6) Test: send a message to the bot in Telegram.

## Useful
- Check webhook:
```
https://api.telegram.org/bot<TOKEN>/getWebhookInfo
```
- Delete webhook:
```
https://api.telegram.org/bot<TOKEN>/deleteWebhook
```
