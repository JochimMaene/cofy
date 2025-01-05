import { Satellite } from "./satellite";

export interface IpfOrbit {
    id: string;
    fileName: string;
    start: string;
    end: string;
    satelliteId: string;
    satellite: Satellite;
    createdAt: string;
    updatedAt: string;
} 