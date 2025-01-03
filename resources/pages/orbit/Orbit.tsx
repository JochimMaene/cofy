import React, { useState, useEffect } from "react";
import MainLayout from "../../layouts/MainLayout";
import { OrbitList } from "./components/orbit-list";
import { IpfOrbit } from "@/types/orbit";
import { fetchOrbits } from "@/services/orbit";
import { toast } from "sonner";

const OrbitPage: React.FC = () => {
    const [orbits, setOrbits] = useState<IpfOrbit[]>([]);
    const [loading, setLoading] = useState(false);
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        const loadOrbits = async () => {
            setLoading(true);
            try {
                const data = await fetchOrbits();
                console.log("Fetched orbits:", data);
                setOrbits(data);
            } catch (error) {
                console.error("Failed to load orbits:", error);
                toast.error("Failed to load orbits");
            } finally {
                setLoading(false);
            }
        };

        loadOrbits();
    }, [refresh]);

    const handleRefresh = () => {
        setRefresh(prev => !prev);
    };

    return (
        <MainLayout
            title="Orbit Files"
            description="View and manage orbit files"
            keywords="Orbits, IPF, Files"
        >
            <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
                <div className="w-full max-w-[1400px]">
                    {loading ? (
                        <div className="flex items-center justify-center h-32">
                            <div className="text-muted-foreground">Loading orbit files...</div>
                        </div>
                    ) : (
                        <OrbitList
                            orbits={orbits}
                            onRefresh={handleRefresh}
                        />
                    )}
                </div>
            </div>
        </MainLayout>
    );
}

export default OrbitPage; 