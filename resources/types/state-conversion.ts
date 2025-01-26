export type StateType = "Cart" | "Kep" | "Circ";

export interface StateConversionInput {
  fromState: StateType;
  toState: StateType;
  state: number[];
}

export interface StateConversionOutput {
  state: number[];
} 