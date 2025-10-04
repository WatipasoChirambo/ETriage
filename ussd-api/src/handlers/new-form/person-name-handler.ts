import { StateService } from 'src/services/state.service';
import { ResponseHandler } from 'src/types/response-handler.interface';

export class PersonNameHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string, sessionId: string) {
    await this.stateService.setState(sessionId, 'personNameExit');
    return 'CON Please enter your full name for example John Doe:';
  }
}
