import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { Config } from '../config/config';

export class ApiClient {
  private client: AxiosInstance;
  private requestQueue: Array<() => Promise<any>> = [];
  private isProcessing = false;
  private lastRequestTime = 0;
  private readonly minRequestInterval: number;

  constructor(
    private readonly config: {
      baseURL: string;
      apiKey: string;
      timeout: number;
      rateLimit?: {
        requestsPerMinute: number;
      };
    }
  ) {
    this.client = axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout,
      headers: {
        'x-cg-pro-api-key': config.apiKey,
      },
    });

    this.minRequestInterval = config.rateLimit
      ? (60 * 1000) / config.rateLimit.requestsPerMinute
      : 0;

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 429) {
          // Rate limit exceeded
          return this.handleRateLimit(error);
        }
        return Promise.reject(error);
      }
    );
  }

  private async handleRateLimit(error: any): Promise<AxiosResponse> {
    const retryAfter = error.response?.headers['retry-after'] || 60;
    await new Promise((resolve) => setTimeout(resolve, retryAfter * 1000));
    return this.client.request(error.config);
  }

  private async processQueue() {
    if (this.isProcessing || this.requestQueue.length === 0) {
      return;
    }

    this.isProcessing = true;
    const now = Date.now();
    const timeSinceLastRequest = now - this.lastRequestTime;

    if (timeSinceLastRequest < this.minRequestInterval) {
      await new Promise((resolve) =>
        setTimeout(resolve, this.minRequestInterval - timeSinceLastRequest)
      );
    }

    const request = this.requestQueue.shift();
    if (request) {
      try {
        await request();
        this.lastRequestTime = Date.now();
      } catch (error) {
        console.error('Request failed:', error);
      }
    }

    this.isProcessing = false;
    this.processQueue();
  }

  async request<T>(config: AxiosRequestConfig): Promise<T> {
    return new Promise((resolve, reject) => {
      this.requestQueue.push(async () => {
        try {
          const response = await this.client.request<T>(config);
          resolve(response.data);
        } catch (error) {
          reject(error);
        }
      });
      this.processQueue();
    });
  }

  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: 'GET', url });
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.request<T>({ ...config, method: 'POST', url, data });
  }
} 