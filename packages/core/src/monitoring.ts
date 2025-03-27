import { CapybaraBot } from './index';
import { config } from 'dotenv';
import { writeFileSync } from 'fs';
import { join } from 'path';

// Load environment variables
config();

class BotMonitor {
  private bot: CapybaraBot;
  private metrics: {
    startTime: Date;
    uptime: number;
    errors: Array<{ timestamp: Date; error: string }>;
    performance: Array<{ timestamp: Date; duration: number }>;
  };

  constructor() {
    this.bot = new CapybaraBot();
    this.metrics = {
      startTime: new Date(),
      uptime: 0,
      errors: [],
      performance: []
    };
  }

  async start() {
    try {
      await this.bot.start();
      console.log('Bot started successfully');
      
      // Start monitoring
      this.startMonitoring();
    } catch (error) {
      console.error('Failed to start bot:', error);
      this.recordError(error as Error);
    }
  }

  private startMonitoring() {
    // Update uptime every minute
    setInterval(() => {
      this.metrics.uptime = Date.now() - this.metrics.startTime.getTime();
      this.saveMetrics();
    }, 60000);

    // Record performance metrics
    setInterval(() => {
      this.recordPerformance();
    }, 300000); // Every 5 minutes
  }

  private recordError(error: Error) {
    this.metrics.errors.push({
      timestamp: new Date(),
      error: error.message
    });
    this.saveMetrics();
  }

  private recordPerformance() {
    const start = Date.now();
    // Perform a simple operation to measure performance
    Promise.resolve().then(() => {
      const duration = Date.now() - start;
      this.metrics.performance.push({
        timestamp: new Date(),
        duration
      });
      this.saveMetrics();
    });
  }

  private saveMetrics() {
    const metricsPath = join(process.cwd(), 'metrics.json');
    writeFileSync(metricsPath, JSON.stringify(this.metrics, null, 2));
  }

  getMetrics() {
    return {
      ...this.metrics,
      currentUptime: Date.now() - this.metrics.startTime.getTime()
    };
  }
}

// Start monitoring if this file is run directly
if (require.main === module) {
  const monitor = new BotMonitor();
  monitor.start().catch(console.error);
}

export { BotMonitor }; 