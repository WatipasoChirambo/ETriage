// Interface for all response handlers
export interface ResponseHandler {
  run(userInput:string,sessionId:string, phoneNumber : string): any;
}
