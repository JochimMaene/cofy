import { FdsData } from "@/types/fds-data";

export const fetchFdsData = async (): Promise<FdsData[]> => {
    const response = await fetch("/update-data");
    if (!response.ok) throw new Error("Failed to fetch data.");
    return response.json();
};

export const updateFdsData = async (data: FdsData): Promise<void> => {
    const url = `/update-data/${data.id}`;
    const response = await fetch(url, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error("Failed to update data.");
};

export const deleteFdsData = async (id: string): Promise<void> => {
    const response = await fetch(`/update-data/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Failed to delete data.");
};
