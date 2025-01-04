

export interface SeparateAudioPayload {
  audio: File;
  separateType: string;
}

export interface SeparateAudioResponse {
  data?: any;
  message?: string;
}