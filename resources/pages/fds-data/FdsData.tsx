import React, { useState } from "react";
import FdsDataList from "./components/fds-data-list";
import MainLayout from "../../layouts/MainLayout";

const FdsDataPage: React.FC = () => {


    const [refresh, setRefresh] = useState(false);

    const handleRefresh = () => {
        setRefresh((prev) => !prev); // Toggle refresh state
    };

    return (
        <MainLayout
            title="FDS Data"
            description="Manage FDS data configurations and settings."
            keywords="FDS Data, Configuration"
        >
            <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
                <div className="w-full max-w-[1400px]">
                    <FdsDataList refresh={refresh} onRefresh={handleRefresh} />
                </div>
            </div>
        </MainLayout>
    );
};

export default FdsDataPage;