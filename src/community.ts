import { TwitterApi } from 'twitter-api-v2';
import { Client as DiscordClient } from 'discord.js';
import TelegramBot from 'node-telegram-bot-api';

export class CommunityManager {
  private twitter: TwitterApi;
  private discord: DiscordClient;
  private telegram: TelegramBot;

  constructor(twitter: TwitterApi, discord: DiscordClient, telegram: TelegramBot) {
    this.twitter = twitter;
    this.discord = discord;
    this.telegram = telegram;
  }

  async broadcastMessage(message: string) {
    try {
      // Post to Twitter
      await this.twitter.v2.tweet(message);

      // Send to Discord channels
      const channels = await this.discord.channels.cache.filter(channel => 
        channel.isTextBased() && !channel.isDMBased()
      );
      channels.forEach(async channel => {
        if (channel.isTextBased() && !channel.isDMBased()) {
          await channel.send(message);
        }
      });

      // Broadcast to Telegram
      const chatId = process.env.TELEGRAM_CHAT_ID;
      if (chatId) {
        await this.telegram.sendMessage(chatId, message);
      }
    } catch (error) {
      console.error('Error broadcasting message:', error);
      throw error;
    }
  }
} 