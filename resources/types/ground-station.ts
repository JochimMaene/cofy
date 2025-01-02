export interface ElevationMaskPoint {
    azimuth: number;
    elevation: number;
}

export interface GroundStation {
    id: string;
    name: string;
    group?: string;
    longitude: number;
    latitude: number;
    altitude: number;
    elevationMask: ElevationMaskPoint[];
} 