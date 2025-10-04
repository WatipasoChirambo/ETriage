import { StateService } from 'src/services/state.service';
import { ResponseHandler } from '../types/response-handler.interface';


export class HomeHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string,sessionId:string) {
    await this.stateService.setState(sessionId, 'homeExit');
    return 'CON Welcome to ETriage\n1. Start New Form\n2. Exit';
  }
}
