import React, { useState } from "react";
import SatelliteList from "./components/satellite-list";
import MainLayout from "@/layouts/MainLayout";

const SatellitesPage: React.FC = () => {
    const [refresh, setRefresh] = useState(false);

    const handleRefresh = () => {
        setRefresh((prev) => !prev);
    };

    return (
        <MainLayout
            title="Satellites"
            description="Manage satellite configurations and settings."
            keywords="Satellites, Configuration"
        >
            <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
                <div className="w-full max-w-6xl">
                    <SatelliteList refresh={refresh} onRefresh={handleRefresh} />
                </div>
            </div>
        </MainLayout>
    );
};

export default SatellitesPage;