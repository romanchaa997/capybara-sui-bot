import { config } from 'dotenv';
import { JsonRpcProvider } from '@mysten/sui';
import { TwitterApi } from 'twitter-api-v2';
import { OpenAI } from 'openai';
import { Client as DiscordClient } from 'discord.js';
import TelegramBot from 'node-telegram-bot-api';

// Load test environment variables
config({ path: '.env.test' });

// Mock external services
jest.mock('@mysten/sui');
jest.mock('twitter-api-v2');
jest.mock('openai');
jest.mock('discord.js');
jest.mock('node-telegram-bot-api');

// Global test configuration
beforeAll(() => {
  // Set up test environment
  process.env.NODE_ENV = 'test';
});

afterAll(() => {
  // Clean up test environment
  jest.clearAllMocks();
}); 