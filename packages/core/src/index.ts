import { SuiClient } from '@mysten/sui.js/client';
import TelegramBot from 'node-telegram-bot-api';
import { TwitterApi } from 'twitter-api-v2';
import { Client as DiscordClient } from 'discord.js';
import { DeFiMonitor } from './defi';
import { CommunityManager } from './community';
import { PriceMonitor } from './price';

export class CapybaraBot {
  private telegram: TelegramBot;
  private suiClient: SuiClient;
  public readonly priceMonitor: PriceMonitor;
  public readonly communityManager: CommunityManager;
  private defiMonitor: DeFiMonitor;

  constructor() {
    // Initialize Telegram bot
    this.telegram = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, {
      polling: true
    });

    // Initialize Sui client
    this.suiClient = new SuiClient({
      url: process.env.SUI_RPC_URL!
    });

    // Initialize Twitter client
    const twitter = new TwitterApi({
      appKey: process.env.TWITTER_API_KEY!,
      appSecret: process.env.TWITTER_API_SECRET!,
      accessToken: process.env.TWITTER_ACCESS_TOKEN!,
      accessSecret: process.env.TWITTER_ACCESS_SECRET!
    });

    // Initialize Discord client
    const discord = new DiscordClient({
      intents: ['Guilds', 'GuildMessages', 'DirectMessages']
    });

    // Initialize monitors
    this.priceMonitor = new PriceMonitor();
    this.communityManager = new CommunityManager(twitter, discord, this.telegram);
    this.defiMonitor = new DeFiMonitor(this.suiClient);
  }

  private async broadcast(message: string) {
    try {
      // Send to Telegram
      await this.telegram.sendMessage(process.env.TELEGRAM_CHAT_ID!, message);
    } catch (error) {
      console.error('Error broadcasting message:', error);
    }
  }

  async start() {
    try {
      // Start monitoring DeFi activity
      await this.defiMonitor.start();

      // Start monitoring community metrics
      await this.communityManager.start();

      // Start monitoring price
      await this.priceMonitor.start();

      // Set up Telegram command handlers
      this.telegram.onText(/\/price/, async () => {
        const price = await this.priceMonitor.getPrice();
        await this.broadcast(`💰 Current price: $${price.toFixed(2)}`);
      });

      this.telegram.onText(/\/metrics/, async () => {
        const metrics = await this.communityManager.getMetrics();
        await this.broadcast(
          `👥 Community Metrics:\nFollowers: ${metrics.followers}\nEngagement Rate: ${metrics.engagement_rate}%\nActive Users: ${metrics.active_users}`
        );
      });

      this.telegram.on('message', async () => {
        // TODO: Implement message handling
      });

      console.log('Bot started successfully!');
    } catch (error) {
      console.error('Error starting bot:', error);
      throw error;
    }
  }

  async stop() {
    await this.defiMonitor.stop();
    await this.communityManager.stop();
    await this.priceMonitor.stop();
    this.telegram.stopPolling();
  }
}

export { PriceMonitor, CommunityManager, DeFiMonitor };

// Start the bot if this file is run directly
if (import.meta.url === fileURLToPath(process.argv[1])) {
  const bot = new CapybaraBot();
  bot.start().catch(console.error);

  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('Shutting down...');
    bot.stop();
    process.exit(0);
  });
} 