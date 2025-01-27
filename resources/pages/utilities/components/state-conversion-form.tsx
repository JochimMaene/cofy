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
import { convertState } from "@/services/state-conversion";
import { StateType } from "@/types/state-conversion";

const stateTypes = ["Cart", "Kep", "Circ"] as const;

const stateFields = {
  Cart: [
    { name: "pos_x", label: "Position X (km)" },
    { name: "pos_y", label: "Position Y (km)" },
    { name: "pos_z", label: "Position Z (km)" },
    { name: "vel_x", label: "Velocity X (km/s)" },
    { name: "vel_y", label: "Velocity Y (km/s)" },
    { name: "vel_z", label: "Velocity Z (km/s)" },
  ],
  Kep: [
    { name: "sma", label: "Semi-major Axis (km)" },
    { name: "ecc", label: "Eccentricity" },
    { name: "inc", label: "Inclination (deg)" },
    { name: "ran", label: "RAAN (deg)" },
    { name: "aop", label: "Argument of Periapsis (deg)" },
    { name: "tan", label: "True Anomaly (deg)" },
  ],
  Circ: [
    { name: "sma", label: "Semi-major Axis (km)" },
    { name: "ecx", label: "Eccentricity X Component" },
    { name: "ecy", label: "Eccentricity Y Component" },
    { name: "inc", label: "Inclination (deg)" },
    { name: "ran", label: "RAAN (deg)" },
    { name: "aol", label: "Argument of Latitude (deg)" },
  ],
};

const formSchema = z.object({
  fromState: z.enum(stateTypes),
  toState: z.enum(stateTypes),
  stateValues: z.array(z.number()).length(6),
});

export function StateConversionForm() {
  const [result, setResult] = useState<number[] | null>(null);
  const [selectedFromType, setSelectedFromType] = useState<StateType>("Cart");
  const [selectedToType, setSelectedToType] = useState<StateType>("Kep");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      fromState: "Cart",
      toState: "Kep",
      stateValues: [0, 0, 0, 0, 0, 0],
    },
  });

  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    try {
      const result = await convertState({
        fromState: data.fromState,
        toState: data.toState,
        state: data.stateValues,
      });
      if (!result.state || result.state.some(value => value === null || !Number.isFinite(value))) {
        throw new Error("Invalid conversion result: received invalid values");
      }
      setResult(result.state);
      toast.success("State converted successfully");
    } catch (error) {
      console.error("Conversion error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to convert state");
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
              name="fromState"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>From State Type</FormLabel>
                  <Select
                    onValueChange={(value: StateType) => {
                      field.onChange(value);
                      setSelectedFromType(value);
                    }}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select input state type" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {stateTypes.map((type) => (
                        <SelectItem key={type} value={type}>
                          {type}
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
              name="toState"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>To State Type</FormLabel>
                  <Select
                    onValueChange={(value: StateType) => {
                      field.onChange(value);
                      setSelectedToType(value);
                    }}
                    defaultValue={field.value}
                  >
                    <FormControl>
                      <SelectTrigger>
                        <SelectValue placeholder="Select output state type" />
                      </SelectTrigger>
                    </FormControl>
                    <SelectContent>
                      {stateTypes.map((type) => (
                        <SelectItem key={type} value={type}>
                          {type}
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
              <label className="text-sm font-medium">ICRF Position (km)</label>
              <div className="grid grid-cols-3 gap-4">
                {stateFields[selectedFromType].slice(0, 3).map((field, index) => (
                  <FormField
                    key={field.name}
                    control={form.control}
                    name={`stateValues.${index}`}
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
              <label className="text-sm font-medium">ICRF Velocity (km/s)</label>
              <div className="grid grid-cols-3 gap-4">
                {stateFields[selectedFromType].slice(3, 6).map((field, index) => (
                  <FormField
                    key={field.name}
                    control={form.control}
                    name={`stateValues.${index + 3}`}
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

          <Button type="submit">Convert State</Button>
        </form>
      </Form>

      {result && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Conversion Result</h3>
          <div className="grid gap-4">
            <div className="grid grid-cols-2 gap-4">
              {stateFields[selectedToType].map((field, index) => (
                <div key={field.name} className="space-y-1">
                  <label className="text-sm font-medium">{field.label}</label>
                  <div className="text-sm font-mono bg-muted p-2 rounded-md">
                    {result[index].toString()}
                  </div>
                </div>
              ))}
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