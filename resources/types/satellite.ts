export interface TleConfig {

    noradId: number;
    classification: "U" | "C";
    launchYear: number;
    launchNumber: number;
    pieceOfLaunch: string;
}

export interface PropulsionSystem {
    name: string;
    direction: string;
    isp: number;
    thrustLevel: number;
    minBurnDuration: number;
    maxBurnDuration: number;
}

export interface GnssSensor {
    name: string;
    posXStd: number;
    posYStd: number;
    posZStd: number;
    velStd: number;
}

export interface Aocs {
    name: string;
    maximumAngVel: number;
}

export interface Satellite {
    id: string;
    name: string;
    group?: string;
    dryMass: number;
    dragArea: number;
    dragCoefficient: number;
    srpArea: number;
    srpCoefficient: number;
    tleConfig: TleConfig;
    propulsion: PropulsionSystem;
    aocs: Aocs;
    gnss: GnssSensor;
    dynamicsId: string;
}

export interface PaginationResponse<T> {
    items: T[];
    total: number;
}