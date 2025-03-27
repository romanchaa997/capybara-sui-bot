import { CapybaraBot } from '../index';
import { config } from 'dotenv';

// Load environment variables
config();

describe('CapybaraBot Integration', () => {
  let bot: CapybaraBot;

  beforeAll(() => {
    bot = new CapybaraBot();
  });

  describe('Initialization', () => {
    it('should initialize all components successfully', async () => {
      await expect(bot.start()).resolves.not.toThrow();
    });
  });

  describe('DeFi Monitoring', () => {
    it('should fetch DeFi stats', async () => {
      const stats = await bot.defiMonitor.getStats();
      expect(stats).toHaveProperty('tvl');
      expect(stats).toHaveProperty('pools');
      expect(stats).toHaveProperty('volume24h');
      expect(stats).toHaveProperty('topPools');
    });
  });

  describe('Price Monitoring', () => {
    it('should fetch price data', async () => {
      const price = await bot.priceMonitor.getPrice();
      expect(typeof price).toBe('number');
      expect(price).toBeGreaterThan(0);
    });
  });

  describe('Community Engagement', () => {
    it('should fetch community metrics', async () => {
      const metrics = await bot.communityEngagement.getMetrics();
      expect(metrics).toHaveProperty('followers');
      expect(metrics).toHaveProperty('engagement');
      expect(metrics).toHaveProperty('totalEngagement');
    });
  });

  describe('Scheduled Tasks', () => {
    it('should execute scheduled tasks', async () => {
      // Wait for at least one scheduled task to execute
      await new Promise(resolve => setTimeout(resolve, 60000));
      
      // Verify that tasks have been executed
      // This will depend on your specific implementation
    });
  });
}); 