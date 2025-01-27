import { TimeScale } from "./time-conversion";

export type FrameType = "ICRF" | "ITRF" | "MOD" | "TOD" | "EME2000";

export interface EpochInput {
  datetime: string;
  timeScale: TimeScale;
}

export interface FrameConversionInput {
  fromFrame: FrameType;
  toFrame: FrameType;
  state: number[];
  epoch: EpochInput;
}

export interface FrameConversionOutput {
  state: number[];
} 