import { z } from "zod";
import { convertState } from "@/services/state-conversion";
import { StateType } from "@/types/state-conversion";

const formSchema = z.object({
  fromState: z.enum(["Cart", "Kep", "Circ"] as const),
  toState: z.enum(["Cart", "Kep", "Circ"] as const),
  stateValues: z.array(z.number()).length(6),
});

const StateConversionForm = () => {
  const onSubmit = async (data: z.infer<typeof formSchema>) => {
    try {
      const result = await convertState({
        fromState: data.fromState,
        toState: data.toState,
        state: data.stateValues,
      });
      setResult(result.state);
      toast.success("State converted successfully");
    } catch (error) {
      console.error("Conversion error:", error);
      toast.error(error instanceof Error ? error.message : "Failed to convert state");
    }
  };

  return (
    // ... rest of the component ...
  );
};

export default StateConversionForm;