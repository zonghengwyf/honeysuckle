export interface SeparateAudioListPayload {

}

export interface SeparateTracksListPayload {

}

export interface SeparateAudioPayload {
  file: File;
  separateType: string;
}

export interface OperateResponse {
  message?: string;
}

export interface SeparateAudioResponse {
  data?: any;
  message?: string;
}

export interface SeparateTracksResponse {
  data?: any;
  message?: string;
}