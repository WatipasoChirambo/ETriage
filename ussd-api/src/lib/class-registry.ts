import { ResponseHandler } from '../types/response-handler.interface';
// Registry to map string keys to handler factory functions
export class ClassRegistry {
  private static registry: Map<string, (...args: any[]) => ResponseHandler> = new Map();

  static register(key: string, factory: (...args: any[]) => ResponseHandler) {
    this.registry.set(key, factory);
  }

  // Bulk register handlers from an object: { key: factory }
  static registerMany(handlers: Record<string, (...args: any[]) => ResponseHandler>) {
    for (const [key, factory] of Object.entries(handlers)) {
      this.register(key, factory);
    }
  }

  static get(key: string, ...args: any[]): ResponseHandler | undefined {
    const factory = this.registry.get(key);
    if (!factory) return undefined;
    return factory(...args);
  }
}
