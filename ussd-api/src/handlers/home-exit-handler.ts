import { StateService } from 'src/services/state.service';
import { ResponseHandler } from '../types/response-handler.interface';


export class HomeExitHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string, sessionId: string, phoneNumber : string) {
    switch (userInput) {
      case '1':
        await this.stateService.setState(sessionId, 'personName');
        return this.stateService.runHandlerByKey('personName', userInput, sessionId,phoneNumber);
      case '2':
        await this.stateService.setState(sessionId, 'closeForm');
        return this.stateService.runHandlerByKey('closeForm', userInput, sessionId,phoneNumber);
      default:
        return 'END Invalid input. Please try again.';
    }
  }
}
