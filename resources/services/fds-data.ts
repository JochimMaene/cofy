import { FdsData } from "@/types/fds-data";

export const fetchFdsData = async (): Promise<FdsData[]> => {
    const response = await fetch("/api/data-status");
    if (!response.ok) throw new Error("Failed to fetch data.");
    return response.json();
};

export const updateFdsData = async (data: FdsData): Promise<void> => {
    const url = `/api/data-status/${data.id}`;
    const response = await fetch(url, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update data.");
};