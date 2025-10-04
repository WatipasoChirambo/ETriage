import { StateService } from 'src/services/state.service';
import { ResponseHandler } from 'src/types/response-handler.interface';



export class  HospitalSelectHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string,sessionId:string, phoneNumber : string) {
    await this.stateService.setState(sessionId, 'hospitalSelectExit');
    return 'CON Please select your hospital:\n1. Central Hospital\n2. Community Hospital';
  }
}
