import { IpfOrbit } from "@/types/orbit";
import { api } from "@/lib/axios";

export async function fetchOrbits(): Promise<IpfOrbit[]> {
    const response = await api.get("/api/orbits");
    console.log("API response:", response.data);
    return response.data.items || [];
}

export async function deleteOrbit(id: string): Promise<void> {
    await api.delete(`/api/orbits/${id}`);
}

export async function downloadOrbit(id: string): Promise<Blob> {
    const response = await api.get(`/api/orbits/${id}/download`, {
        responseType: 'blob'
    });
    return response.data;
} 