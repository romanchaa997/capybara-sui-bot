import { PriceMonitor } from '../price';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('PriceMonitor', () => {
  let priceMonitor: PriceMonitor;
  const mockApiKey = 'test-api-key';

  beforeEach(() => {
    priceMonitor = new PriceMonitor(mockApiKey);
    jest.clearAllMocks();
  });

  describe('getStats', () => {
    it('should return cached data if available and not expired', async () => {
      const mockData = {
        price: 1.23,
        change24h: 5.67,
        volume24h: 1000000,
        marketCap: 50000000
      };

      // @ts-ignore - accessing private property for testing
      priceMonitor.cache.set('price_stats', {
        data: mockData,
        timestamp: Date.now()
      });

      const result = await priceMonitor.getStats();
      expect(result).toEqual(mockData);
      expect(mockedAxios.get).not.toHaveBeenCalled();
    });

    it('should fetch fresh data if cache is expired', async () => {
      const mockResponse = {
        data: {
          sui: {
            usd: 1.23,
            usd_24h_change: 5.67,
            usd_24h_vol: 1000000,
            usd_market_cap: 50000000
          }
        }
      };

      mockedAxios.get.mockResolvedValueOnce(mockResponse);

      // @ts-ignore - accessing private property for testing
      priceMonitor.cache.set('price_stats', {
        data: {},
        timestamp: Date.now() - 6 * 60 * 1000 // 6 minutes old
      });

      const result = await priceMonitor.getStats();
      expect(result).toEqual({
        price: 1.23,
        change24h: 5.67,
        volume24h: 1000000,
        marketCap: 50000000
      });
      expect(mockedAxios.get).toHaveBeenCalledWith(
        expect.stringContaining('api.coingecko.com'),
        expect.objectContaining({
          headers: {
            'x-cg-pro-api-key': mockApiKey
          }
        })
      );
    });

    it('should handle API errors gracefully', async () => {
      mockedAxios.get.mockRejectedValueOnce(new Error('API Error'));

      await expect(priceMonitor.getStats()).rejects.toThrow('Error fetching price stats');
    });
  });

  describe('getPrice', () => {
    it('should return current price', async () => {
      const mockStats = {
        price: 1.23,
        change24h: 5.67,
        volume24h: 1000000,
        marketCap: 50000000
      };

      jest.spyOn(priceMonitor, 'getStats').mockResolvedValue(mockStats);

      const result = await priceMonitor.getPrice();
      expect(result).toBe(1.23);
    });
  });

  describe('getPriceChange24h', () => {
    it('should return 24h price change', async () => {
      const mockStats = {
        price: 1.23,
        change24h: 5.67,
        volume24h: 1000000,
        marketCap: 50000000
      };

      jest.spyOn(priceMonitor, 'getStats').mockResolvedValue(mockStats);

      const result = await priceMonitor.getPriceChange24h();
      expect(result).toBe(5.67);
    });
  });

  describe('getMarketCap', () => {
    it('should return market cap', async () => {
      const mockStats = {
        price: 1.23,
        change24h: 5.67,
        volume24h: 1000000,
        marketCap: 50000000
      };

      jest.spyOn(priceMonitor, 'getStats').mockResolvedValue(mockStats);

      const result = await priceMonitor.getMarketCap();
      expect(result).toBe(50000000);
    });
  });
}); 