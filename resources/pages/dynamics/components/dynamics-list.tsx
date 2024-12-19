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
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { PlusCircle, Search, Edit2, Trash2, Check, X } from "lucide-react";
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
    const [searchTerm, setSearchTerm] = useState("");

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

    const filteredDynamics = dynamics.filter(dyn =>
        dyn.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <Card className="w-full">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <CardTitle>Dynamics Configuration</CardTitle>
                <Dialog>
                    <DialogTrigger asChild>
                        <Button onClick={handleCreate} variant="default" className="flex items-center gap-2">
                            <PlusCircle className="h-4 w-4" />
                            Add New
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[600px]">
                        <DialogHeader>
                            <DialogTitle>
                                {editingDynamics ? "Update Dynamics" : "Create Dynamics"}
                            </DialogTitle>
                        </DialogHeader>
                        <DynamicsForm
                            initialData={editingDynamics ?? undefined}
                            onRefresh={onRefresh}
                            onClose={() => setEditingDynamics(null)}
                        />
                    </DialogContent>
                </Dialog>
            </CardHeader>
            <CardContent>
                <div className="flex items-center gap-4 mb-4">
                    <div className="relative flex-1 max-w-sm">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search dynamics..."
                            className="pl-8"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                </div>

                <div className="rounded-md border">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Harmonics Degree</TableHead>
                                <TableHead>Harmonics Order</TableHead>
                                <TableHead className="text-center">Other perturbations</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredDynamics.map((dyn) => (
                                <TableRow key={dyn.id}>
                                    <TableCell className="font-medium">{dyn.name}</TableCell>
                                    <TableCell>{dyn.harmonicsDegree}</TableCell>
                                    <TableCell>{dyn.harmonicsOrder}</TableCell>
                                    <TableCell>
                                        <div className="flex flex-wrap gap-2 justify-center">
                                            {dyn.solarRadiationPressure && (
                                                <span className="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
                                                    SRP
                                                </span>
                                            )}
                                            {dyn.drag && (
                                                <span className="inline-flex items-center rounded-full bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-700/10">
                                                    Drag
                                                </span>
                                            )}
                                            {dyn.solidTides && (
                                                <span className="inline-flex items-center rounded-full bg-purple-50 px-2 py-1 text-xs font-medium text-purple-700 ring-1 ring-inset ring-purple-700/10">
                                                    Solid Tides
                                                </span>
                                            )}
                                            {dyn.thirdBodySun && (
                                                <span className="inline-flex items-center rounded-full bg-yellow-50 px-2 py-1 text-xs font-medium text-yellow-700 ring-1 ring-inset ring-yellow-700/10">
                                                    Sun
                                                </span>
                                            )}
                                            {dyn.thirdBodyMoon && (
                                                <span className="inline-flex items-center rounded-full bg-gray-50 px-2 py-1 text-xs font-medium text-gray-700 ring-1 ring-inset ring-gray-700/10">
                                                    Moon
                                                </span>
                                            )}
                                        </div>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end space-x-2">
                                            <Dialog>
                                                <DialogTrigger asChild>
                                                    <Button
                                                        variant="ghost"
                                                        size="icon"
                                                        onClick={() => handleEdit(dyn)}
                                                        className="h-8 w-8"
                                                    >
                                                        <Edit2 className="h-4 w-4" />
                                                    </Button>
                                                </DialogTrigger>
                                                <DialogContent>
                                                    <DialogHeader>
                                                        <DialogTitle>Update Dynamics</DialogTitle>
                                                    </DialogHeader>
                                                    <DynamicsForm
                                                        initialData={dyn}
                                                        onRefresh={onRefresh}
                                                        onClose={() => setEditingDynamics(null)}
                                                    />
                                                </DialogContent>
                                            </Dialog>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 text-destructive hover:text-destructive"
                                                onClick={() => setDeleteId(dyn.id)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </div>
            </CardContent>

            {/* Delete Confirmation Dialog */}
            <Dialog open={!!deleteId} onOpenChange={(isOpen) => !isOpen && setDeleteId(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Confirm Deletion</DialogTitle>
                    </DialogHeader>
                    <p>Are you sure you want to delete this dynamics object? This action cannot be undone.</p>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setDeleteId(null)}>
                            Cancel
                        </Button>
                        <Button variant="destructive" onClick={() => deleteId && handleDelete(deleteId)}>
                            Delete
                        </Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </Card>
    );
};

export default DynamicsList;
