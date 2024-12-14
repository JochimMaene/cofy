import React, { useEffect, useState } from "react";
import { FdsData } from "@/types/fds-data";
import {
    Table,
    TableHeader,
    TableBody,
    TableRow,
    TableHead,
    TableCell,
} from "@/components/ui/table";
import {
    Dialog,
    DialogTrigger,
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import FdsDataForm from "./fds-data-form";
import { fetchFdsData } from "@/services/fds-data";


interface FdsDataListProps {
    refresh: boolean;
    onRefresh: () => void;
}

const FdsDataList: React.FC<FdsDataListProps> = ({ refresh, onRefresh }) => {
    const [fdsData, setFdsData] = useState<FdsData[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [editingFdsData, setEditingFdsData] = useState<FdsData | null>(null);
    useEffect(() => {
        const loadFdsData = async () => {
            setLoading(true);
            try {
                const data = await fetchFdsData();
                setFdsData(data);
            } catch (error) {
                toast.error("Failed to load environment data status.");
            } finally {
                setLoading(false);
            }
        };
        loadFdsData();
    }, [refresh]);

    if (loading) {
        return <div>Loading fds data status...</div>;
    }

    if (fdsData.length === 0) {
        return <div>No fds data status available.</div>;
    }

    const handleEdit = (dyn: FdsData) => {
        setEditingFdsData(dyn);
    };

    const getStatusStyle = (status: string) => {
        switch (status) {
            case "out_of_date":
                return "bg-red-500 text-white px-2 py-1 rounded-full";
            case "updated":
                return "bg-green-500 text-white px-2 py-1 rounded-full";
            default:
                return "bg-gray-200 text-black px-2 py-1 rounded-full";
        }
    };

    return (
        <>

            {/* Dialog for Create/Update */}
            <Dialog open={editingFdsData !== null} onOpenChange={(open) => !open && setEditingFdsData(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Edit FDS Data Update settings</DialogTitle>
                    </DialogHeader>
                    <FdsDataForm
                        initialData={editingFdsData!}  // Since editingFdsData is not null when dialog is open
                        onRefresh={onRefresh}
                        onClose={() => setEditingFdsData(null)} // Close dialog after save/cancel
                    />
                </DialogContent>
            </Dialog>

            {/* Confirmation Dialog */}
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>URL</TableHead>
                        <TableHead>Last update</TableHead>
                        <TableHead>Next update</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Cron</TableHead>

                    </TableRow>
                </TableHeader>
                <TableBody>
                    {fdsData.map((data) => (
                        <TableRow key={data.id}>
                            <TableCell>{data.name}</TableCell>
                            <TableCell>{data.URL}</TableCell>
                            <TableCell>{data.lastUpdate}</TableCell>
                            <TableCell>{data.nextUpdate}</TableCell>
                            <TableCell><span className={getStatusStyle(data.status)}>
                                {data.status}
                            </span></TableCell>
                            <TableCell>{data.cron}</TableCell>
                            <TableCell>
                                <Button
                                    variant="outline"
                                    size="sm"
                                    onClick={() => handleEdit(data)}  // Set the data to be edited
                                >
                                    Edit
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </>
    );
};


export default FdsDataList;
