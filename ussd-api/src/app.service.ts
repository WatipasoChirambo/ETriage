import { Injectable, Inject } from '@nestjs/common';

import { CACHE_MANAGER, Cache } from '@nestjs/cache-manager';
@Injectable()
export class AppService {
  constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}
  getHello(): string {
    return 'Hello World!';
  }
}
