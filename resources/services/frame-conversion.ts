import { api } from "@/lib/axios";
import { FrameConversionInput, FrameConversionOutput } from "@/types/frame-conversion";

export async function convertFrame(data: FrameConversionInput): Promise<FrameConversionOutput> {
  const response = await api.post<FrameConversionOutput>("/api/util/frame-convert", {
    from_frame: data.fromFrame,
    to_frame: data.toFrame,
    state: data.state,
    epoch: {
      datetime: data.epoch.datetime,
      time_scale: data.epoch.timeScale,
    },
  });
  
  if (!response.data.state || response.data.state.some(value => value === null)) {
    throw new Error("Invalid conversion result: received null values");
  }
  
  return response.data;
} 