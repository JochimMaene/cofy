export type TimeScale = "UTC" | "TT" | "TAI" | "GPS";

export interface TimeScaleConversionInput {
  fromTimeScale: TimeScale;
  toTimeScale: TimeScale;
  datetime: string;
}

export interface TimeScaleConversionOutput {
  datetime: string;
} 