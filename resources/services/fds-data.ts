import { FdsData } from "@/types/fds-data";
import { api } from "@/lib/axios";

export const fetchFdsData = async (): Promise<FdsData[]> => {
    const response = await api.get("/api/data-status");
    return response.data;
};

export const updateFdsData = async (data: FdsData): Promise<void> => {
    await api.patch(`/api/data-status/${data.id}`, data);
};

export const refreshFdsData = async (id: number): Promise<void> => {
    await api.post(`/api/data-update/${id}`);
};