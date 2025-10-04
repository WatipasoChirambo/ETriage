import { StateService } from 'src/services/state.service';
import { SubmitSymptomsRequest } from 'src/types/requests/submit-symptoms';
import { ResponseHandler } from 'src/types/response-handler.interface';



export class HospitalSelectExitHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string, sessionId: string, phoneNumber : string) {
    const body = await this.stateService.getValue<SubmitSymptomsRequest>(`submit_symptoms_${sessionId}`);
    if (!body) {
        await this.stateService.setState(sessionId, 'personName');
        return this.stateService.runHandlerByKey('personName', userInput, sessionId,phoneNumber); 
    }
    body.hospital_id = parseInt(userInput, 10);
    await this.stateService.setValue<SubmitSymptomsRequest>(`submit_symptoms_${sessionId}`,body);
    await this.stateService.setState(sessionId, 'medicalInsurance');
    return this.stateService.runHandlerByKey('medicalInsurance', userInput, sessionId,phoneNumber); 
  }
}
