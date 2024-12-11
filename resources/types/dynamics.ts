export interface Dynamics {
    id: string;
    name: string;
    harmonicsDegree: number;
    harmonicsOrder: number;
    solarRadiationPressure: boolean;
    drag: boolean;
    solidTides: boolean;
    thirdBodySun: boolean;
    thirdBodyMoon: boolean;
}

export interface PaginationResponse<T> {
    items: T[];
    total: number;
}
