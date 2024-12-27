import React, { useState, useEffect } from "react";
import { GroundStationList } from "./components/ground-station-list";
import MainLayout from "../../layouts/MainLayout";
import { fetchGroundStations } from "@/services/ground-station";
import { GroundStation } from "@/types/ground-station";

const GroundStationPage: React.FC = () => {
    const [groundStations, setGroundStations] = useState<GroundStation[]>([]);
    const [loading, setLoading] = useState(false);
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        const loadGroundStations = async () => {
            setLoading(true);
            try {
                const data = await fetchGroundStations();
                setGroundStations(data);
            } catch (error) {
                console.error("Failed to load ground stations:", error);
            } finally {
                setLoading(false);
            }
        };

        loadGroundStations();
    }, [refresh]);

    const handleRefresh = () => {
        setRefresh(prev => !prev);
    };

    return (
        <MainLayout
            title="Ground Stations"
            description="Manage ground station configurations and settings."
            keywords="Ground Stations, Configuration"
        >
            <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
                <div className="w-full max-w-[1400px]">
                    {loading ? (
                        <div className="flex items-center justify-center h-32">
                            <div className="text-muted-foreground">Loading ground stations...</div>
                        </div>
                    ) : (
                        <GroundStationList
                            groundStations={groundStations}
                            onRefresh={handleRefresh}
                        />
                    )}
                </div>
            </div>
        </MainLayout>
    );
};

export default GroundStationPage; 