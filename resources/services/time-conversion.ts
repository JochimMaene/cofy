import { TimeScaleConversionInput, TimeScaleConversionOutput } from "@/types/time-conversion";
import { api } from "@/lib/axios";

export async function convertTimeScale(data: TimeScaleConversionInput): Promise<TimeScaleConversionOutput> {
  const response = await api.post<TimeScaleConversionOutput>("/api/util/time-scale-convert", {
    from_time_scale: data.fromTimeScale,
    to_time_scale: data.toTimeScale,
    datetime: data.datetime,
  });
  
  return response.data;
} 