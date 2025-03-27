import { CapybaraBot } from './index';

describe('CapybaraBot', () => {
  let bot: CapybaraBot;

  beforeEach(() => {
    bot = new CapybaraBot();
  });

  it('should initialize correctly', () => {
    expect(bot).toBeDefined();
  });
});

async function testBot() {
  try {
    console.log('Starting Capybara Sui Bot test...');
    
    const agent = new CapybaraBot();
    
    // Test initialization
    console.log('Testing initialization...');
    await agent.start();
    
    // Test DeFi monitoring
    console.log('Testing DeFi monitoring...');
    const defiStats = await agent.defiMonitor.getStats();
    console.log('DeFi stats:', defiStats);
    
    // Test price monitoring
    console.log('Testing price monitoring...');
    const price = await agent.priceMonitor.getPrice();
    console.log('SUI price:', price);
    
    // Test community monitoring
    console.log('Testing community monitoring...');
    const communityMetrics = await agent.communityManager.getMetrics();
    console.log('Community metrics:', communityMetrics);
    
    console.log('All tests completed successfully!');
    
    // Clean up
    agent.stop();
  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Run tests if this file is run directly
if (require.main === module) {
  testBot();
} 