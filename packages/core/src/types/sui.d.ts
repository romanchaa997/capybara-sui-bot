export interface SuiClient {
  getBalance(address: string): Promise<number>;
  getLatestCheckpoint(): Promise<string>;
}

export class JsonRpcProvider implements SuiClient {
  constructor(endpoint?: string);
  getBalance(address: string): Promise<number>;
  getLatestCheckpoint(): Promise<string>;
} 