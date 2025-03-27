import { Plugin, PluginContext } from '@elizaos/core';
import { SuiClient } from '@mysten/sui.js/client';
import type { ValidatorsApy } from '@mysten/sui.js/client';

export class SuiPlugin implements Plugin {
  private provider: SuiClient;
  private context: PluginContext;

  constructor(context: PluginContext) {
    this.context = context;
    this.provider = new SuiClient({
      url: context.config.networks.sui.rpcUrl
    });
  }

  async initialize(): Promise<void> {
    // Initialize plugin
    await this.provider.getCheckpoint();
  }

  async getLatestTransactions(): Promise<any[]> {
    const latestCheckpoint = await this.provider.getCheckpoint();
    const transactions = await this.provider.queryTransactionBlocks({
      filter: { Checkpoint: latestCheckpoint.digest }
    });
    return transactions.data;
  }

  async getAccountBalance(address: string): Promise<string> {
    const balance = await this.provider.getBalance({
      owner: address,
      coinType: '0x2::sui::SUI'
    });
    return balance.totalBalance;
  }

  async getNetworkStats(): Promise<any> {
    const latestCheckpoint = await this.provider.getCheckpoint();
    const networkStats = {
      totalTransactions: latestCheckpoint.networkTotalTransactions,
      totalGasUsed: latestCheckpoint.networkTotalGasUsed,
      epoch: latestCheckpoint.epoch
    };
    return networkStats;
  }

  async getValidators(): Promise<ValidatorsApy> {
    const validators = await this.provider.getValidatorsApy();
    return validators;
  }

  async getDeFiStats(): Promise<any> {
    // Implement DeFi stats collection
    return {
      totalValueLocked: '0',
      activePools: 0,
      dailyVolume: '0'
    };
  }
}

export default SuiPlugin; 