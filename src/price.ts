import { SuiClient } from '@mysten/sui.js/client';
import axios from 'axios';

export class PriceMonitor {
  private provider: SuiClient;
  private priceEndpoint: string;
  private price: number = 0;
  private interval?: NodeJS.Timeout;

  constructor() {
    this.provider = new SuiClient({
      url: process.env.SUI_RPC_URL || 'https://fullnode.mainnet.sui.io:443'
    });
    this.priceEndpoint = 'https://api.coingecko.com/api/v3/simple/price?ids=sui&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true';
  }

  async getSuiPrice(): Promise<number> {
    try {
      const response = await axios.get(this.priceEndpoint);
      return response.data.sui.usd;
    } catch (error) {
      console.error('Error fetching SUI price:', error);
      throw error;
    }
  }

  async getPrice(): Promise<number> {
    try {
      return await this.getSuiPrice();
    } catch (error) {
      console.error('Error fetching price:', error);
      throw error;
    }
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