import { CommunityEngagement } from '../community';
import { TwitterApi } from 'twitter-api-v2';
import { OpenAI } from 'openai';
import { Client as DiscordClient } from 'discord.js';
import TelegramBot from 'node-telegram-bot-api';

describe('CommunityEngagement', () => {
  let communityEngagement: CommunityEngagement;
  let mockTwitter: jest.Mocked<TwitterApi>;
  let mockOpenAI: jest.Mocked<OpenAI>;
  let mockDiscord: jest.Mocked<DiscordClient>;
  let mockTelegram: jest.Mocked<TelegramBot>;

  beforeEach(() => {
    mockTwitter = new TwitterApi({}) as jest.Mocked<TwitterApi>;
    mockOpenAI = new OpenAI() as jest.Mocked<OpenAI>;
    mockDiscord = new DiscordClient({}) as jest.Mocked<DiscordClient>;
    mockTelegram = new TelegramBot('', { polling: true }) as jest.Mocked<TelegramBot>;

    communityEngagement = new CommunityEngagement(mockTwitter, mockOpenAI);
  });

  describe('getMetrics', () => {
    it('should return cached metrics if available and not expired', async () => {
      const mockMetrics = {
        followers: {
          twitter: 1000,
          discord: 500,
          telegram: 300
        },
        engagement: {
          twitter: 100,
          discord: 50,
          telegram: 30
        },
        totalEngagement: 60
      };

      // @ts-ignore - accessing private property for testing
      communityEngagement.cache.set('community_metrics', {
        data: mockMetrics,
        timestamp: Date.now()
      });

      const result = await communityEngagement.getMetrics();
      expect(result).toEqual(mockMetrics);
    });

    it('should fetch fresh metrics if cache is expired', async () => {
      const mockTwitterMetrics = { followers: 1000, engagement: 100 };
      const mockDiscordMetrics = { members: 500, engagement: 50 };
      const mockTelegramMetrics = { members: 300, engagement: 30 };

      jest.spyOn(communityEngagement as any, 'getTwitterMetrics').mockResolvedValue(mockTwitterMetrics);
      jest.spyOn(communityEngagement as any, 'getDiscordMetrics').mockResolvedValue(mockDiscordMetrics);
      jest.spyOn(communityEngagement as any, 'getTelegramMetrics').mockResolvedValue(mockTelegramMetrics);

      // @ts-ignore - accessing private property for testing
      communityEngagement.cache.set('community_metrics', {
        data: {},
        timestamp: Date.now() - 16 * 60 * 1000 // 16 minutes old
      });

      const result = await communityEngagement.getMetrics();
      expect(result).toEqual({
        followers: {
          twitter: 1000,
          discord: 500,
          telegram: 300
        },
        engagement: {
          twitter: 100,
          discord: 50,
          telegram: 30
        },
        totalEngagement: 60
      });
    });

    it('should handle errors gracefully', async () => {
      jest.spyOn(communityEngagement as any, 'getTwitterMetrics').mockRejectedValue(new Error('API Error'));

      await expect(communityEngagement.getMetrics()).rejects.toThrow('Error fetching community metrics');
    });
  });

  describe('engageWithTweets', () => {
    it('should engage with target accounts', async () => {
      const mockUser = { data: { id: '123' } };
      const mockTweets = {
        data: {
          data: [
            { id: '1', text: 'Test tweet 1' },
            { id: '2', text: 'Test tweet 2' }
          ]
        }
      };

      mockTwitter.v2.userByUsername.mockResolvedValue(mockUser);
      mockTwitter.v2.userTimeline.mockResolvedValue(mockTweets);
      mockTwitter.v2.reply.mockResolvedValue({ data: { id: 'reply1' } });

      // Mock OpenAI response
      mockOpenAI.chat.completions.create.mockResolvedValue({
        choices: [{ message: { content: 'Test response' } }]
      });

      await communityEngagement.engageWithTweets();

      expect(mockTwitter.v2.userByUsername).toHaveBeenCalledWith('SuiNetwork');
      expect(mockTwitter.v2.userTimeline).toHaveBeenCalledWith('123', expect.any(Object));
      expect(mockTwitter.v2.reply).toHaveBeenCalledTimes(2);
    });

    it('should handle errors for individual accounts', async () => {
      mockTwitter.v2.userByUsername.mockRejectedValue(new Error('API Error'));

      await communityEngagement.engageWithTweets();
      // Should not throw error, just log it
    });
  });

  describe('runGiveaway', () => {
    it('should create and monitor a giveaway', async () => {
      const mockTweet = { data: { id: 'tweet1' } };
      const mockTweetMetrics = {
        data: {
          public_metrics: {
            like_count: 100,
            retweet_count: 50
          }
        }
      };

      mockOpenAI.chat.completions.create.mockResolvedValue({
        choices: [{ message: { content: 'Test giveaway tweet' } }]
      });
      mockTwitter.v2.tweet.mockResolvedValue(mockTweet);
      mockTwitter.v2.singleTweet.mockResolvedValue(mockTweetMetrics);

      await communityEngagement.runGiveaway();

      expect(mockTwitter.v2.tweet).toHaveBeenCalled();
      expect(mockTwitter.v2.singleTweet).toHaveBeenCalledWith('tweet1', expect.any(Object));
    });
  });
}); 