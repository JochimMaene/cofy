import React, { useState } from "react";
import DynamicsList from "./components/dynamics-list";
import MainLayout from "@/layouts/MainLayout";
const DynamicsPage: React.FC = () => {


    const [refresh, setRefresh] = useState(false);

    const handleRefresh = () => {
        setRefresh((prev) => !prev); // Toggle refresh state
    };

    return (
        <MainLayout
            title="Dynamics"
            description="Manage Dynamics settings and configurations."
            keywords="Dynamics, Settings"
        >
            <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
                <div className="w-full max-w-4xl">
                    <DynamicsList refresh={refresh} onRefresh={handleRefresh} />
                </div>
            </div>
        </MainLayout>
    );
};

export default DynamicsPage;