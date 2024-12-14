import { Dynamics, PaginationResponse } from "@/types/dynamics";

export const fetchDynamics = async (): Promise<PaginationResponse<Dynamics>> => {
    const response = await fetch("/api/dynamics");
    if (!response.ok) throw new Error("Failed to fetch dynamics.");
    return response.json();
};

export const createOrUpdateDynamics = async (dynamics: Dynamics): Promise<void> => {
    const url = dynamics.id ? `/api/dynamics/${dynamics.id}` : "/api/dynamics";
    const method = dynamics.id ? "PATCH" : "POST";
    const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dynamics),
    });
    if (!response.ok) throw new Error("Failed to save dynamics.");
};

export const deleteDynamics = async (id: string): Promise<void> => {
    const response = await fetch(`/api/dynamics/${id}`, { method: "DELETE" });
    if (!response.ok) throw new Error("Failed to delete dynamics.");
};
