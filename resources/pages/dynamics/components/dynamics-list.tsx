import React, { useEffect, useState } from "react";
import { Dynamics } from "@/types/dynamics";
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
    DialogFooter,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import DynamicsForm from "./dynamics-form";
import { fetchDynamics, deleteDynamics } from "@/services/dynamics";


interface DynamicsListProps {
    refresh: boolean;
    onRefresh: () => void;
}

const DynamicsList: React.FC<DynamicsListProps> = ({ refresh, onRefresh }) => {
    const [dynamics, setDynamics] = useState<Dynamics[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [editingDynamics, setEditingDynamics] = useState<Dynamics | null>(null);
    const [deleteId, setDeleteId] = useState<string | null>(null);
    useEffect(() => {
        const loadDynamics = async () => {
            setLoading(true);
            try {
                const data = await fetchDynamics();
                setDynamics(data.items);
            } catch (error) {
                toast.error("Failed to load dynamics.");
            } finally {
                setLoading(false);
            }
        };
        loadDynamics();
    }, [refresh]);

    if (loading) {
        return <div>Loading dynamics...</div>;
    }

    if (dynamics.length === 0) {
        return <div>No dynamics available.</div>;
    }

    const handleEdit = (dyn: Dynamics) => {
        setEditingDynamics(dyn); // Set dynamics to be edited
    };

    const handleCreate = () => {
        setEditingDynamics(null); // Clear dynamics for creating a new one
    };

    const handleDelete = async (id: string) => {
        try {
            await deleteDynamics(id);
            toast.success("Dynamics deleted successfully.");
            onRefresh();
            setDeleteId(null);
        } catch {
            toast.error("Failed to delete dynamics.");
        }
    };

    return (
        <>


            {/* Dialog for Create/Update */}
            <Dialog>
                <DialogTrigger asChild>
                    <Button onClick={handleCreate} variant="default">
                        Create Dynamics
                    </Button>
                </DialogTrigger>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>
                            {editingDynamics ? "Update Dynamics" : "Create Dynamics"}
                        </DialogTitle>
                    </DialogHeader>
                    <DynamicsForm
                        initialData={editingDynamics ?? undefined}
                        onRefresh={onRefresh}
                        onClose={() => setEditingDynamics(null)} // Close the dialog
                    />
                </DialogContent>
            </Dialog>

            {/* Confirmation Dialog */}
            <Dialog open={!!deleteId} onOpenChange={(isOpen) => !isOpen && setDeleteId(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Confirm Deletion</DialogTitle>
                    </DialogHeader>
                    <p>Are you sure you want to delete this dynamics object? This action cannot be undone.</p>
                    <DialogFooter>
                        <Button variant="destructive" onClick={() => deleteId && handleDelete(deleteId)}>
                            Delete
                        </Button>
                        <Button variant="outline" onClick={() => setDeleteId(null)}>
                            Cancel
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Harmonics Degree</TableHead>
                        <TableHead>Harmonics Order</TableHead>
                        <TableHead>Solar Radiation Pressure</TableHead>
                        <TableHead>Drag</TableHead>
                        <TableHead>Solid Tides</TableHead>
                        <TableHead>Third Body Sun</TableHead>
                        <TableHead>Third Body Moon</TableHead>
                        <TableHead>Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {dynamics.map((dyn) => (
                        <TableRow key={dyn.id}>
                            <TableCell>{dyn.name}</TableCell>
                            <TableCell>{dyn.harmonicsDegree}</TableCell>
                            <TableCell>{dyn.harmonicsOrder}</TableCell>
                            <TableCell>{dyn.solarRadiationPressure ? "Yes" : "No"}</TableCell>
                            <TableCell>{dyn.drag ? "Yes" : "No"}</TableCell>
                            <TableCell>{dyn.solidTides ? "Yes" : "No"}</TableCell>
                            <TableCell>{dyn.thirdBodySun ? "Yes" : "No"}</TableCell>
                            <TableCell>{dyn.thirdBodyMoon ? "Yes" : "No"}</TableCell>
                            <TableCell>
                                <div className="flex space-x-2">
                                    <Dialog>
                                        <DialogTrigger asChild>
                                            <Button
                                                variant="outline"
                                                size="sm"
                                                onClick={() => handleEdit(dyn)}
                                            >
                                                Update
                                            </Button>
                                        </DialogTrigger>
                                        <DialogContent>
                                            <DialogHeader>
                                                <DialogTitle>Update Dynamics</DialogTitle>
                                            </DialogHeader>
                                            <DynamicsForm
                                                initialData={dyn}
                                                onRefresh={onRefresh}
                                                onClose={() => setEditingDynamics(null)} // Close dialog on save/cancel
                                            />
                                        </DialogContent>
                                    </Dialog>
                                    <Button variant="destructive" size="sm" onClick={() => setDeleteId(dyn.id)}>
                                        Delete
                                    </Button>
                                </div>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </>
    );
};


export default DynamicsList;
