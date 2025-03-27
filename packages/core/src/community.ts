import { TwitterApi } from 'twitter-api-v2';
import { OpenAI } from 'openai';
import { Client as DiscordClient } from 'discord.js';
import TelegramBot from 'node-telegram-bot-api';

export interface CommunityMetrics {
  followers: number;
  engagement_rate: number;
  active_users: number;
}

export class CommunityEngagement {
  private twitter: TwitterApi;
  private openai: OpenAI;
  private discord: DiscordClient;
  private telegram: TelegramBot;
  private targetAccounts = [
    'SuiNetwork',
    'Mysten_Labs',
    'SuiChiefEcon',
    'SuiCorner',
    'Community_Sui'
  ];
  private cache: Map<string, { data: CommunityMetrics; timestamp: number }> = new Map();
  private readonly CACHE_DURATION = 15 * 60 * 1000; // 15 minutes

  constructor(twitter: TwitterApi, openai: OpenAI) {
    this.twitter = twitter;
    this.openai = openai;

    // Initialize Discord client
    this.discord = new DiscordClient({
      intents: ['GuildMembers', 'GuildMessages', 'MessageContent'],
    });

    // Initialize Telegram client
    this.telegram = new TelegramBot(process.env.TELEGRAM_BOT_TOKEN!, { polling: true });
  }

  async getMetrics(): Promise<CommunityMetrics> {
    const cacheKey = 'metrics';
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      return cached.data;
    }

    const [twitter, discord, telegram] = await Promise.all([
      this.getTwitterMetrics(),
      this.getDiscordMetrics(),
      this.getTelegramMetrics()
    ]);

    const metrics: CommunityMetrics = {
      followers: twitter.followers + discord.members + telegram.members,
      engagement_rate: (twitter.engagement + discord.engagement + telegram.engagement) / 3,
      active_users: 0 // TODO: Implement active users tracking
    };

    this.cache.set(cacheKey, {
      data: metrics,
      timestamp: Date.now()
    });

    return metrics;
  }

  private async getTwitterMetrics(): Promise<{ followers: number; engagement: number }> {
    try {
      const me = await this.twitter.v2.me();
      const metrics = await this.twitter.v2.userByUsername(me.data.username);
      
      return {
        followers: metrics.data.public_metrics?.followers_count || 0,
        engagement: 0 // TODO: Calculate engagement rate
      };
    } catch (error) {
      console.error('Error fetching Twitter metrics:', error);
      return { followers: 0, engagement: 0 };
    }
  }

  private async getDiscordMetrics(): Promise<{ members: number; engagement: number }> {
    try {
      const guilds = await this.discord.guilds.fetch();
      let totalMembers = 0;
      
      for (const [, partialGuild] of guilds) {
        const guild = await partialGuild.fetch();
        totalMembers += guild.memberCount;
      }

      return {
        members: totalMembers,
        engagement: 0 // TODO: Calculate engagement rate
      };
    } catch (error) {
      console.error('Error fetching Discord metrics:', error);
      return { members: 0, engagement: 0 };
    }
  }

  private async getTelegramMetrics(): Promise<{ members: number; engagement: number }> {
    try {
      const chatId = process.env.TELEGRAM_CHAT_ID!;
      const chat = await this.telegram.getChat(chatId);
      
      return {
        members: (chat as any).member_count || 0,
        engagement: 0 // TODO: Calculate engagement rate
      };
    } catch (error) {
      console.error('Error fetching Telegram metrics:', error);
      return { members: 0, engagement: 0 };
    }
  }

  async engageWithTweets(): Promise<void> {
    for (const account of this.targetAccounts) {
      try {
        // Get recent tweets from the account
        const tweets = await this.twitter.v2.userByUsername(account);
        if (!tweets.data) continue;

        const userId = tweets.data.id;
        const userTweets = await this.twitter.v2.userTimeline(userId, {
          max_results: 5,
          'tweet.fields': 'created_at'
        });

        // Generate and post responses
        for (const tweet of userTweets.data.data || []) {
          const response = await this.generateResponse(tweet.text);
          await this.twitter.v2.reply(response, tweet.id);
        }
      } catch (error) {
        console.error(`Error engaging with ${account}:`, error);
      }
    }
  }

  private async generateResponse(tweetText: string): Promise<string> {
    const prompt = `Generate a friendly and engaging response to this tweet about Sui blockchain:
      "${tweetText}"
      
      Make it informative and add value to the conversation. Include relevant hashtags.`;

    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
    });

    return completion.choices[0].message.content || 'Error generating response';
  }

  async runGiveaway(): Promise<void> {
    try {
      // Generate giveaway tweet
      const giveawayTweet = await this.generateGiveawayTweet();
      
      // Post the giveaway tweet
      const tweet = await this.twitter.v2.tweet(giveawayTweet);
      
      // Monitor engagement
      this.monitorGiveawayEngagement(tweet.data.id);
    } catch (error) {
      console.error('Error running giveaway:', error);
    }
  }

  private async generateGiveawayTweet(): Promise<string> {
    const prompt = `Generate an engaging giveaway tweet for Sui ecosystem:
      - Prize: 100 SUI tokens
      - Duration: 24 hours
      - Requirements: Follow, Like, Retweet
      - Include relevant hashtags and emojis`;

    const completion = await this.openai.chat.completions.create({
      model: "gpt-4",
      messages: [{ role: "user", content: prompt }],
    });

    return completion.choices[0].message.content || 'Error generating giveaway tweet';
  }

  private async monitorGiveawayEngagement(tweetId: string): Promise<void> {
    // Monitor likes, retweets, and comments for 24 hours
    const endTime = Date.now() + 24 * 60 * 60 * 1000;
    
    while (Date.now() < endTime) {
      try {
        const engagement = await this.twitter.v2.singleTweet(tweetId, {
          'tweet.fields': ['public_metrics']
        });
        
        // Process engagement metrics
        console.log('Giveaway engagement:', engagement.data);
        
        // Wait for 1 hour before next check
        await new Promise(resolve => setTimeout(resolve, 60 * 60 * 1000));
      } catch (error) {
        console.error('Error monitoring giveaway:', error);
      }
    }
  }
}

export class CommunityManager {
  private readonly twitter: TwitterApi;
  private readonly discord: DiscordClient;
  private readonly telegram: TelegramBot;
  private readonly cache: Map<string, { data: CommunityMetrics; timestamp: number }>;
  private readonly CACHE_DURATION = 15 * 60 * 1000; // 15 minutes

  constructor(twitter: TwitterApi, discord: DiscordClient, telegram: TelegramBot) {
    this.twitter = twitter;
    this.discord = discord;
    this.telegram = telegram;
    this.cache = new Map();
  }

  async getMetrics(): Promise<CommunityMetrics> {
    const cacheKey = 'metrics';
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      return cached.data;
    }

    const [twitter, discord, telegram] = await Promise.all([
      this.getTwitterMetrics(),
      this.getDiscordMetrics(),
      this.getTelegramMetrics()
    ]);

    const metrics: CommunityMetrics = {
      followers: twitter.followers + discord.members + telegram.members,
      engagement_rate: (twitter.engagement + discord.engagement + telegram.engagement) / 3,
      active_users: 0 // TODO: Implement active users tracking
    };

    this.cache.set(cacheKey, {
      data: metrics,
      timestamp: Date.now()
    });

    return metrics;
  }

  private async getTwitterMetrics(): Promise<{ followers: number; engagement: number }> {
    try {
      const me = await this.twitter.v2.me();
      const metrics = await this.twitter.v2.userByUsername(me.data.username);
      
      return {
        followers: metrics.data.public_metrics?.followers_count || 0,
        engagement: 0 // TODO: Calculate engagement rate
      };
    } catch (error) {
      console.error('Error fetching Twitter metrics:', error);
      return { followers: 0, engagement: 0 };
    }
  }

  private async getDiscordMetrics(): Promise<{ members: number; engagement: number }> {
    try {
      const guilds = await this.discord.guilds.fetch();
      let totalMembers = 0;
      
      for (const [, partialGuild] of guilds) {
        const guild = await partialGuild.fetch();
        totalMembers += guild.memberCount;
      }

      return {
        members: totalMembers,
        engagement: 0 // TODO: Calculate engagement rate
      };
    } catch (error) {
      console.error('Error fetching Discord metrics:', error);
      return { members: 0, engagement: 0 };
    }
  }

  private async getTelegramMetrics(): Promise<{ members: number; engagement: number }> {
    try {
      const chatId = process.env.TELEGRAM_CHAT_ID!;
      const chat = await this.telegram.getChat(chatId);
      
      return {
        members: (chat as any).member_count || 0,
        engagement: 0 // TODO: Calculate engagement rate
      };
    } catch (error) {
      console.error('Error fetching Telegram metrics:', error);
      return { members: 0, engagement: 0 };
    }
  }

  async start() {
    // Start periodic metrics collection
    setInterval(async () => {
      try {
        await this.getMetrics();
      } catch (error) {
        console.error('Error collecting metrics:', error);
      }
    }, this.CACHE_DURATION);
  }

  async stop() {
    // Nothing to clean up yet
  }
} 