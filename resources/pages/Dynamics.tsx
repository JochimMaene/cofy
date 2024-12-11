import React, { useState } from "react";
import DynamicsList from "@/components/DynamicsList";
import MainLayout from "@/layouts/MainLayout";

const DynamicsPage: React.FC = () => {
    const [refresh, setRefresh] = useState(false);

    const handleRefresh = () => {
        setRefresh((prev) => !prev); // Toggle refresh state
    };

    return (
        <MainLayout
            title="Litestar Application - Dynamics"
            description="Manage Dynamics settings and configurations."
            keywords="Dynamics, Settings"
        >
            <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
                <h1 className="text-2xl font-semibold text-gray-800">Manage Dynamics</h1>

                {/* List Section */}
                <div className="w-full max-w-4xl">
                    <DynamicsList refresh={refresh} onRefresh={handleRefresh} />
                </div>
            </div>
        </MainLayout>
    );
};

export default DynamicsPage;
