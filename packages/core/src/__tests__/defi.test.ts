import { DeFiMonitor } from '../defi';
import { JsonRpcProvider } from '@mysten/sui';

describe('DeFiMonitor', () => {
  let defiMonitor: DeFiMonitor;
  let mockSui: jest.Mocked<JsonRpcProvider>;

  beforeEach(() => {
    mockSui = new JsonRpcProvider() as jest.Mocked<JsonRpcProvider>;
    defiMonitor = new DeFiMonitor(mockSui);
  });

  describe('getStats', () => {
    it('should return cached data if available and not expired', async () => {
      const mockStats = {
        tvl: 1000000,
        pools: 10,
        volume24h: 500000,
        topPools: [
          { protocol: 'Test Protocol', pool: 'Pool 1', volume: '100000' }
        ]
      };

      // @ts-ignore - accessing private property for testing
      defiMonitor.cache.set('defi_stats', {
        data: mockStats,
        timestamp: Date.now()
      });

      const result = await defiMonitor.getStats();
      expect(result).toEqual(mockStats);
    });

    it('should fetch fresh data if cache is expired', async () => {
      const mockStats = {
        tvl: 1000000,
        pools: 10,
        volume24h: 500000,
        topPools: [
          { protocol: 'Test Protocol', pool: 'Pool 1', volume: '100000' }
        ]
      };

      // @ts-ignore - accessing private property for testing
      defiMonitor.cache.set('defi_stats', {
        data: mockStats,
        timestamp: Date.now() - 6 * 60 * 1000 // 6 minutes old
      });

      // Mock the private methods
      jest.spyOn(defiMonitor as any, 'getTotalValueLocked').mockResolvedValue(1000000);
      jest.spyOn(defiMonitor as any, 'getActivePools').mockResolvedValue(10);
      jest.spyOn(defiMonitor as any, 'get24hVolume').mockResolvedValue(500000);
      jest.spyOn(defiMonitor as any, 'getTopPools').mockResolvedValue([
        { protocol: 'Test Protocol', pool: 'Pool 1', volume: '100000' }
      ]);

      const result = await defiMonitor.getStats();
      expect(result).toEqual(mockStats);
    });

    it('should handle errors gracefully', async () => {
      // Mock error in one of the methods
      jest.spyOn(defiMonitor as any, 'getTotalValueLocked').mockRejectedValue(new Error('API Error'));

      await expect(defiMonitor.getStats()).rejects.toThrow('Error fetching DeFi stats');
    });
  });
}); 