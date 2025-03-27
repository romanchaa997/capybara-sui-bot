import { TwitterApi } from 'twitter-api-v2';
import { Client as DiscordClient } from 'discord.js';
import TelegramBot from 'node-telegram-bot-api';
import { SuiClient } from '@mysten/sui.js/client';
import { PriceMonitor } from './price';
import { CommunityManager } from './community';
import { DeFiMonitor } from './defi';

export class CapybaraBot {
  private twitter: TwitterApi;
  private discord: DiscordClient;
  private telegram: TelegramBot;
  private provider: SuiClient;
  private priceMonitor: PriceMonitor;
  private communityManager: CommunityManager;
  private defiMonitor: DeFiMonitor;

  constructor() {
    // Initialize clients
    this.twitter = new TwitterApi({
      appKey: process.env.TWITTER_APP_KEY!,
      appSecret: process.env.TWITTER_APP_SECRET!,
      accessToken: process.env.TWITTER_ACCESS_TOKEN!,
      accessSecret: process.env.TWITTER_ACCESS_SECRET!,
    });

    this.discord = new DiscordClient({
      intents: ['GuildMessages', 'MessageContent', 'Guilds'],
    });

    this.telegram = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, {
      polling: true,
    });

    this.provider = new SuiClient({
      url: process.env.SUI_RPC_URL || 'https://fullnode.mainnet.sui.io:443'
    });
    this.priceMonitor = new PriceMonitor();
    this.communityManager = new CommunityManager(this.twitter, this.discord, this.telegram);
    this.defiMonitor = new DeFiMonitor(this.provider);
  }

  // ... rest of the class implementation
} 