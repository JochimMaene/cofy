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
import { convertFrame } from "@/services/frame-conversion";
import { FrameType } from "@/types/frame-conversion";

const frameTypes = ["ICRF", "ITRF", "MOD", "TOD", "EME2000"] as const;
const timeScales = ["UTC", "TT", "TAI", "GPS"] as const;

const stateLabels = [
  { name: "pos_x", label: "Position X (km)" },
  { name: "pos_y", label: "Position Y (km)" },
  { name: "pos_z", label: "Position Z (km)" },
  { name: "vel_x", label: "Velocity X (km/s)" },
  { name: "vel_y", label: "Velocity Y (km/s)" },
  { name: "vel_z", label: "Velocity Z (km/s)" },
];

const formSchema = z.object({
  fromFrame: z.enum(frameTypes),
  toFrame: z.enum(frameTypes),
  state: z.array(z.number()).length(6),
  epoch: z.object({
    datetime: z.string(),
    timeScale: z.enum(timeScales),
  }),
});

export function FrameConversionForm() {
  const [result, setResult] = useState<number[] | null>(null);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      fromFrame: "ICRF" as FrameType,
      toFrame: "ITRF" as FrameType,
      state: [0, 0, 0, 0, 0, 0],
      epoch: {
        datetime: new Date().toISOString().replace('Z', ''),
        timeScale: "UTC",
      },
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    try {
      const result = await convertFrame(data);
      if (!result.state || result.state.some(value => !Number.isFinite(value))) {
        throw new Error("Invalid conversion result: received invalid values");
      }
      setResult(result.state);
      toast.success("Frame converted successfully");
    } catch (error) {
      console.error("Conversion error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to convert frame");
      setResult(null); // Reset result on error
    }
  };

  return (
    <div className="space-y-8">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="fromFrame"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>From Frame</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select input frame" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {frameTypes.map((frame) => (
                        <SelectItem key={frame} value={frame}>
                          {frame}
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
              name="toFrame"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>To Frame</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select output frame" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {frameTypes.map((frame) => (
                        <SelectItem key={frame} value={frame}>
                          {frame}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">Position (km)</label>
              <div className="grid grid-cols-3 gap-4">
                {stateLabels.slice(0, 3).map((field, index) => (
                  <FormField
                    key={field.name}
                    control={form.control}
                    name={`state.${index}`}
                    render={({ field: formField }) => (
                      <FormItem>
                        <FormLabel className="text-xs">{field.label.split(' ')[1]}</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            step="any"
                            {...formField}
                            onChange={(e) => formField.onChange(parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                ))}
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium">Velocity (km/s)</label>
              <div className="grid grid-cols-3 gap-4">
                {stateLabels.slice(3, 6).map((field, index) => (
                  <FormField
                    key={field.name}
                    control={form.control}
                    name={`state.${index + 3}`}
                    render={({ field: formField }) => (
                      <FormItem>
                        <FormLabel className="text-xs">{field.label.split(' ')[1]}</FormLabel>
                        <FormControl>
                          <Input
                            type="number"
                            step="any"
                            {...formField}
                            onChange={(e) => formField.onChange(parseFloat(e.target.value))}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={form.control}
              name="epoch.datetime"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Epoch (ISO format)</FormLabel>
                  <FormControl>
                    <Input 
                      type="text" 
                      placeholder="YYYY-MM-DDTHH:mm:ss.SSSSSS"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="epoch.timeScale"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Time Scale</FormLabel>
                  <Select onValueChange={field.onChange} defaultValue={field.value}>
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select time scale" />
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

          <Button type="submit">Convert Frame</Button>
        </form>
      </Form>

      {result && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Conversion Result</h3>
          <div className="grid gap-4">
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Position (km)</label>
                <div className="grid grid-cols-3 gap-4">
                  {stateLabels.slice(0, 3).map((field, index) => (
                    <div key={field.name} className="space-y-1">
                      <label className="text-xs font-medium">{field.label.split(' ')[1]}</label>
                      <div className="text-sm font-mono bg-muted p-2 rounded-md">
                        {result[index].toString()}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Velocity (km/s)</label>
                <div className="grid grid-cols-3 gap-4">
                  {stateLabels.slice(3, 6).map((field, index) => (
                    <div key={field.name} className="space-y-1">
                      <label className="text-xs font-medium">{field.label.split(' ')[1]}</label>
                      <div className="text-sm font-mono bg-muted p-2 rounded-md">
                        {result[index + 3].toString()}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <Button 
              variant="outline" 
              onClick={() => {
                const text = `[${result.map(v => v.toString()).join(", ")}]`;
                navigator.clipboard.writeText(text);
                toast.success("Copied to clipboard");
              }}
            >
              Copy Output To Clipboard
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}