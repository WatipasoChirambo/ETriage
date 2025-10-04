import { Body, Controller, Get, Inject, Post } from '@nestjs/common';
import { AppService } from './app.service';
import { StateService } from './services/state.service';

type UssdRequestBody = {
  sessionId: string;
  serviceCode: string;
  phoneNumber: string;
  text: string;
}

@Controller()
export class AppController {
  constructor(private readonly appService: AppService, private readonly stateService: StateService) {}

  @Post("/callback")
  async callback(@Body() requestBody :UssdRequestBody ): Promise<string> {
    console.log(requestBody)
    const currentState = await this.stateService.getState(requestBody.sessionId)
    if(currentState == ""){
      this.stateService.setState(requestBody.sessionId, "home")
      return this.stateService.runHandlerByKey("home",requestBody.text,requestBody.sessionId,requestBody.phoneNumber) || "END An error occurred"
    }
    else{
      return this.stateService.runHandlerByKey(currentState,requestBody.text,requestBody.sessionId,requestBody.phoneNumber) || "END An error occurred"
    }
    
  }
}
