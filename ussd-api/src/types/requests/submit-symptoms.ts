export interface SubmitSymptomsRequest {
    phone_number: string;
    first_name?: string;
    last_name?: string;
    hospital_id: number;
    has_scheme: boolean;
    medical_scheme_id?: number;
    member_number?: string;
    symptoms: number[];
    severity: number[];
}