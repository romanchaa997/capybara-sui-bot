import { PriceMonitor } from '../price';
import { Config } from '../config/config';

describe('PriceMonitor Integration', () => {
  let priceMonitor: PriceMonitor;

  beforeAll(() => {
    priceMonitor = new PriceMonitor();
  });

  it('should fetch SUI price data', async () => {
    const stats = await priceMonitor.getStats();
    
    expect(stats).toHaveProperty('price');
    expect(stats).toHaveProperty('change24h');
    expect(stats).toHaveProperty('volume24h');
    expect(stats).toHaveProperty('marketCap');
    
    // Verify data types
    expect(typeof stats.price).toBe('number');
    expect(typeof stats.change24h).toBe('number');
    expect(typeof stats.volume24h).toBe('number');
    expect(typeof stats.marketCap).toBe('number');
    
    // Verify values are reasonable
    expect(stats.price).toBeGreaterThan(0);
    expect(stats.volume24h).toBeGreaterThan(0);
    expect(stats.marketCap).toBeGreaterThan(0);
  });

  it('should handle API rate limits gracefully', async () => {
    // Make multiple requests in quick succession
    const requests = Array(10).fill(null).map(() => priceMonitor.getStats());
    const results = await Promise.allSettled(requests);
    
    // Some requests might fail due to rate limiting
    const successful = results.filter(r => r.status === 'fulfilled').length;
    expect(successful).toBeGreaterThan(0);
  });

  it('should cache responses', async () => {
    const startTime = Date.now();
    const stats1 = await priceMonitor.getStats();
    const stats2 = await priceMonitor.getStats();
    const endTime = Date.now();

    // Verify both responses are identical
    expect(stats1).toEqual(stats2);
    
    // Verify the second request was served from cache (should be much faster)
    expect(endTime - startTime).toBeLessThan(Config.cache.ttl);
  });
}); 