import { StateService } from 'src/services/state.service';
import { ResponseHandler } from 'src/types/response-handler.interface';



export class  CloseFormHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string,sessionId:string, phoneNumber : string) {
    await this.stateService.clearState(sessionId)
    return "END Thank you for using our service.";
  }
}
