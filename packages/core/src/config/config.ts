import { config } from 'dotenv';
import { z } from 'zod';

// Load environment variables
config();

// Define environment variable schema
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  COINGECKO_API_KEY: z.string().min(1),
  OPENAI_API_KEY: z.string().min(1),
  TELEGRAM_BOT_TOKEN: z.string(),
  TELEGRAM_CHAT_ID: z.string(),
  DISCORD_BOT_TOKEN: z.string(),
  DISCORD_CHANNEL_ID: z.string(),
  TWITTER_APP_KEY: z.string(),
  TWITTER_APP_SECRET: z.string(),
  TWITTER_ACCESS_TOKEN: z.string(),
  TWITTER_ACCESS_SECRET: z.string(),
});

// Validate environment variables
export function loadConfig() {
  const result = envSchema.safeParse(process.env);
  
  if (!result.success) {
    const missingVars = result.error.errors.map(err => err.path.join('.')).join(', ');
    throw new Error(`Missing required environment variables: ${missingVars}`);
  }
  
  return result.data;
}

// Create configuration object
const env = loadConfig();

export const Config = {
  env: env.NODE_ENV,
  api: {
    coingecko: {
      key: env.COINGECKO_API_KEY,
      baseUrl: 'https://api.coingecko.com/api/v3',
      timeout: 10000, // 10 seconds
    },
    openai: {
      key: env.OPENAI_API_KEY,
      model: 'gpt-4',
      maxTokens: 1000,
      temperature: 0.7,
    },
  },
  cache: {
    ttl: 5 * 60 * 1000, // 5 minutes
    maxSize: 100, // Maximum number of items to cache
  },
  monitoring: {
    enabled: true,
    logLevel: env.NODE_ENV === 'production' ? 'info' : 'debug',
    metricsInterval: 5 * 60 * 1000, // 5 minutes
  },
} as const;

// Type for the configuration
export type Config = typeof Config; 