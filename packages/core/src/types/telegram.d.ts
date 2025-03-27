declare module 'node-telegram-bot-api' {
  interface TelegramBotOptions {
    polling?: boolean;
    filepath?: boolean;
  }

  interface Chat {
    id: number;
    type: string;
    title?: string;
    member_count?: number;
  }

  interface Message {
    message_id: number;
    text?: string;
  }

  export default class TelegramBot {
    constructor(token: string, options?: TelegramBotOptions);
    sendMessage(chatId: string | number, text: string): Promise<Message>;
    getChat(chatId: string | number): Promise<Chat>;
    getMessages(chatId: string | number, options?: { limit?: number }): Promise<Message[]>;
  }
} 