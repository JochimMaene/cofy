import { GroundStation } from "@/types/ground-station";
import { api } from "@/lib/axios";

export const fetchGroundStations = async (): Promise<GroundStation[]> => {
    const response = await api.get("/api/ground-stations");
    return response.data.items || [];
};

export const createGroundStation = async (data: Omit<GroundStation, "id">): Promise<GroundStation> => {
    const response = await api.post("/api/ground-stations", data);
    return response.data;
};

export const updateGroundStation = async (data: GroundStation): Promise<GroundStation> => {
    const response = await api.patch(`/api/ground-stations/${data.id}`, data);
    return response.data;
};

export const deleteGroundStation = async (id: string): Promise<void> => {
    await api.delete(`/api/ground-stations/${id}`);
}; 