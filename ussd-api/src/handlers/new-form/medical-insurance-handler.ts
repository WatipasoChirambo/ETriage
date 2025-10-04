import { StateService } from 'src/services/state.service';
import { ResponseHandler } from 'src/types/response-handler.interface';


export class MedicalInsuranceHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string,sessionId:string) {
    await this.stateService.setState(sessionId, 'medicalInsuranceExit');
    return 'CON Do you have medical insurance?\n1. Yes \n2. No';
  }
}
