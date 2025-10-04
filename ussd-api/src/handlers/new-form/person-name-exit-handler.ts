import { StateService } from 'src/services/state.service';
import { SubmitSymptomsRequest } from 'src/types/requests/submit-symptoms';
import { ResponseHandler } from 'src/types/response-handler.interface';



export class PersonNameExitHandler implements ResponseHandler {
  constructor(private stateService: StateService) {}
  async run(userInput: string, sessionId: string, phoneNumber : string) {
    const names = userInput.split(' ');
    if (names.length < 2) {
      return 'CON Please enter both first and last names separated by a space.';
    }
    const firstName = names[0];
    const lastName = names.slice(1).join(' ');
    const submitSymptomsRequest : SubmitSymptomsRequest = {
        hospital_id : 0, 
        first_name : firstName,
        last_name : lastName,
        phone_number : phoneNumber ,
        has_scheme : false,
        symptoms : [],
        severity : []
    }
    await this.stateService.setValue<SubmitSymptomsRequest>(`submit_symptoms_${sessionId}`,submitSymptomsRequest);
    await this.stateService.setState(sessionId, 'hospitalSelect');
    return this.stateService.runHandlerByKey('hospitalSelect', userInput, sessionId,phoneNumber); 
  }
}
