import { api } from "@/lib/axios";
import { StateConversionInput, StateConversionOutput, StateType } from "@/types/state-conversion";

const DEG_TO_RAD = Math.PI / 180;
const RAD_TO_DEG = 180 / Math.PI;

// Fields that need degree to radian conversion for each state type
const angleFields: Record<StateType, number[]> = {
  Cart: [], // Cartesian has no angles
  Kep: [2, 3, 4, 5], // inc, ran, aop, tan are in degrees
  Circ: [3, 4, 5], // inc, ran, aol are in degrees
} as const;

function convertToRadians(stateType: StateConversionInput["fromState"], values: number[]): number[] {
  return values.map((value, index) => 
    angleFields[stateType].includes(index) ? value * DEG_TO_RAD : value
  );
}

function convertToDegrees(stateType: StateConversionInput["toState"], values: number[]): number[] {
  return values.map((value, index) => 
    angleFields[stateType].includes(index) ? value * RAD_TO_DEG : value
  );
}

export async function convertState(data: StateConversionInput): Promise<StateConversionOutput> {
  // Convert angles from degrees to radians before sending to API
  const radiansState = convertToRadians(data.fromState, data.state);

  const response = await api.post<StateConversionOutput>("/api/util/state-convert", {
    from_state: data.fromState,
    to_state: data.toState,
    state: radiansState,
  });
  
  if (!response.data.state || response.data.state.some(value => value === null || !Number.isFinite(value))) {
    throw new Error("Invalid conversion result: received invalid or null values");
  }
  
  // Convert angles back to degrees for display
  return {
    state: convertToDegrees(data.toState, response.data.state)
  };
} 