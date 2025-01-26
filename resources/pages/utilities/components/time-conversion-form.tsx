import { useState } from "react";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { TimeScale } from "@/types/time-conversion";
import { convertTimeScale } from "@/services/time-conversion";

const timeScales: TimeScale[] = ["UTC", "TT", "TAI", "GPS"];

const formSchema = z.object({
  fromTimeScale: z.enum(["UTC", "TT", "TAI", "GPS"] as const),
  toTimeScale: z.enum(["UTC", "TT", "TAI", "GPS"] as const),
  datetime: z.string(),
});

export function TimeConversionForm() {
  const [result, setResult] = useState<string | null>(null);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      fromTimeScale: "UTC",
      toTimeScale: "TT",
      datetime: new Date().toISOString().split('.')[0], // Current time in YYYY-MM-DDTHH:mm:ss format
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    try {
      const result = await convertTimeScale({
        fromTimeScale: data.fromTimeScale,
        toTimeScale: data.toTimeScale,
        datetime: data.datetime,
      });
      setResult(result.datetime);
      toast.success("Time converted successfully");
    } catch (error) {
      console.error("Conversion error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to convert time");
    }
  };

  return (
    <div className="space-y-8">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="fromTimeScale"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>From Time Scale</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select input time scale" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {timeScales.map((scale) => (
                        <SelectItem key={scale} value={scale}>
                          {scale}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="toTimeScale"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>To Time Scale</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select output time scale" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {timeScales.map((scale) => (
                        <SelectItem key={scale} value={scale}>
                          {scale}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={form.control}
            name="datetime"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Date and Time (ISO format)</FormLabel>
                <FormControl>
                  <Input 
                    type="text" 
                    placeholder="YYYY-MM-DDTHH:mm:ss.SSSSSS"
                    {...field}
                    defaultValue={new Date().toISOString().replace('Z', '')}
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button type="submit">Convert Time</Button>
        </form>
      </Form>

      {result && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Conversion Result</h3>
          <div className="text-sm">{result}</div>
        </div>
      )}
    </div>
  );
} 