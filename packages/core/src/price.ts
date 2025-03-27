import { Config } from './config/config';
import { ApiClient } from './utils/api-client';

interface PriceStats {
  price: number;
  change24h: number;
  volume24h: number;
  marketCap: number;
}

export class PriceMonitor {
  private apiClient: ApiClient;
  private cache: Map<string, { data: PriceStats; timestamp: number }> = new Map();
  private price: number = 0;
  private interval?: NodeJS.Timeout;

  constructor() {
    this.apiClient = new ApiClient({
      baseURL: Config.api.coingecko.baseUrl,
      apiKey: Config.api.coingecko.key,
      timeout: Config.api.coingecko.timeout,
      rateLimit: {
        requestsPerMinute: 50, // CoinGecko Pro API limit
      },
    });
  }

  async getStats(): Promise<PriceStats> {
    const cacheKey = 'price_stats';
    const cached = this.cache.get(cacheKey);
    const now = Date.now();

    if (cached && now - cached.timestamp < Config.cache.ttl) {
      return cached.data;
    }

    try {
      const response = await this.apiClient.get<{
        sui: {
          usd: number;
          usd_24h_change: number;
          usd_24h_vol: number;
          usd_market_cap: number;
        };
      }>('/simple/price', {
        params: {
          ids: 'sui',
          vs_currencies: 'usd',
          include_24hr_change: true,
          include_24hr_vol: true,
          include_market_cap: true,
        },
      });

      const stats: PriceStats = {
        price: response.sui.usd,
        change24h: response.sui.usd_24h_change,
        volume24h: response.sui.usd_24h_vol,
        marketCap: response.sui.usd_market_cap,
      };

      this.cache.set(cacheKey, {
        data: stats,
        timestamp: now,
      });

      return stats;
    } catch (error) {
      console.error('Error fetching price stats:', error);
      throw new Error('Failed to fetch price statistics');
    }
  }

  async getPrice(): Promise<number> {
    try {
      // TODO: Implement price fetching from an API
      return this.price;
    } catch (error) {
      console.error('Error fetching price:', error);
      throw error;
    }
  }

  async getPriceChange24h(): Promise<number> {
    const stats = await this.getStats();
    return stats.change24h;
  }

  async getMarketCap(): Promise<number> {
    const stats = await this.getStats();
    return stats.marketCap;
  }

  async start() {
    // Update price every minute
    this.interval = setInterval(async () => {
      try {
        this.price = await this.getPrice();
      } catch (error) {
        console.error('Error updating price:', error);
      }
    }, 60000);

    // Initial price update
    try {
      this.price = await this.getPrice();
    } catch (error) {
      console.error('Error getting initial price:', error);
    }
  }

  async stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = undefined;
    }
  }
} 