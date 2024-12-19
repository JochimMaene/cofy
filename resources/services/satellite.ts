import { Satellite, PaginationResponse } from "@/types/satellite";

export const fetchSatellites = async (): Promise<PaginationResponse<Satellite>> => {
    const response = await fetch("/api/satellites");
    if (!response.ok) throw new Error("Failed to fetch satellites.");
    return response.json();
};

export const createOrUpdateSatellite = async (satellite: Satellite): Promise<void> => {
    const url = satellite.id ? `/api/satellites/${satellite.id}` : "/api/satellites";
    const method = satellite.id ? "PATCH" : "POST";
    const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(satellite),
    });
    if (!response.ok) throw new Error("Failed to save satellite.");
};

export const deleteSatellite = async (id: string): Promise<void> => {
    const response = await fetch(`/api/satellites/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Failed to delete satellite.");
};
