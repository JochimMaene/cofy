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
import React from "react";

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
  const [selectedFromType, setSelectedFromType] = useState<keyof typeof stateFields>("Cart");
  const [selectedToType, setSelectedToType] = useState<keyof typeof stateFields>("Kep");

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
      const response = await fetch("/api/util/state-convert", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          fromState: data.fromState,
          toState: data.toState,
          state: data.stateValues,
        }),
      });

      if (!response.ok) {
        throw new Error("Conversion failed");
      }

      const result = await response.json();
      setResult(result.state);
      toast.success("State converted successfully");
    } catch (error) {
      toast.error("Failed to convert state");
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
                    onValueChange={(value: keyof typeof stateFields) => {
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
                    onValueChange={(value: keyof typeof stateFields) => {
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

          <div className="grid grid-cols-2 gap-4">
            {stateFields[selectedFromType].map((field, index) => (
              <FormField
                key={field.name}
                control={form.control}
                name={`stateValues.${index}`}
                render={({ field: formField }) => (
                  <FormItem>
                    <FormLabel>{field.label}</FormLabel>
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

          <Button type="submit">Convert State</Button>
        </form>
      </Form>

      {result && (
        <div className="space-y-4">
          <h3 className="text-lg font-medium">Conversion Result</h3>
          <div className="grid grid-cols-2 gap-4">
            {stateFields[selectedToType].map((field, index) => (
              <div key={field.name} className="space-y-1">
                <label className="text-sm font-medium">{field.label}</label>
                <div className="text-sm">{result[index].toFixed(6)}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 