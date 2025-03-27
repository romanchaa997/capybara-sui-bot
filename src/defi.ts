import { SuiClient } from '@mysten/sui.js/client';
import { TransactionBlock } from '@mysten/sui.js/transactions';
import type { SuiEvent } from '@mysten/sui.js/client';

export class DeFiMonitor {
  private provider: SuiClient;
  private unsubscribe?: () => void;

  constructor(provider: SuiClient) {
    this.provider = provider;
  }

  async monitorTransactions() {
    try {
      // Subscribe to new transactions
      this.unsubscribe = await this.provider.subscribeEvent({
        filter: {
          MoveModule: {
            package: process.env.DEFI_PACKAGE_ID || '',
            module: 'defi'
          }
        },
        onMessage: this.handleTransaction.bind(this)
      });
    } catch (error) {
      console.error('Error monitoring transactions:', error);
      throw error;
    }
  }

  private async handleTransaction(event: SuiEvent) {
    try {
      // Process transaction based on type
      console.log('New DeFi transaction:', event);
    } catch (error) {
      console.error('Error handling transaction:', error);
    }
  }

  async stop() {
    if (this.unsubscribe) {
      this.unsubscribe();
      this.unsubscribe = undefined;
    }
  }
} 