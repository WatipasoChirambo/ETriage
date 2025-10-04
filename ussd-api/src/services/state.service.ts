import { Injectable, Inject } from '@nestjs/common';

import { CACHE_MANAGER, Cache } from '@nestjs/cache-manager';
import { ClassRegistry } from '../lib/class-registry';
import { ResponseHandler } from '../types/response-handler.interface';
@Injectable()
export class StateService {
  constructor(@Inject(CACHE_MANAGER) private cacheManager: Cache) {}

  async getState(sessionId: string): Promise<string> {
    return await this.cacheManager.get<string>(`session_state_${sessionId}`) || "";
  }
  
  async setState(sessionId: string, state: string): Promise<void> {
    await this.cacheManager.set(`session_state_${sessionId}`, state);
  }

  async clearState(sessionId: string): Promise<boolean> {
    return await this.cacheManager.del(`session_state_${sessionId}`);
  }

  async setValue<T>(key:string,value : T,ttl?:number){
    let result : T | undefined;
    if(ttl){
      result = await this.cacheManager.set(key,value,ttl);
    }
    else{
      result = await this.cacheManager.set(key,value);
    }
    return result
  }

  async clearValue(key:string){
    return await this.cacheManager.del(key);
  }


  async  getValue<T>(key:string){
    return await this.cacheManager.get<T>(key);
  }

  runHandlerByKey(key: string, userInput: string, sessionId: string, phoneNumber : string): any {
    // Pass this StateService instance to the handler factory
    const handler: ResponseHandler | undefined = ClassRegistry.get(key, this);
    if (handler) {
      return handler.run(userInput, sessionId,phoneNumber);
    }
    return undefined;
  }
}
