import React, { useState } from "react";
import FdsDataList from "./components/fds-data-list";

const FdsDataPage: React.FC = () => {


    const [refresh, setRefresh] = useState(false);

    const handleRefresh = () => {
        setRefresh((prev) => !prev); // Toggle refresh state
    };

    return (
        // <MainLayout
        //     title="Litestar Application - FdsData"
        //     description="Manage FdsData settings and configurations."
        //     keywords="FdsData, Settings"
        // >
        <div className="w-full h-full flex flex-col items-center px-4 md:px-8 py-8 space-y-8">
            {/* List Section */}
            <div className="w-full max-w-4xl">
                <FdsDataList refresh={refresh} onRefresh={handleRefresh} />
            </div>
        </div>
        // </MainLayout>
    );
};

export default FdsDataPage;