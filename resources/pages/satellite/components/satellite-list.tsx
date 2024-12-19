import React, { useEffect, useState } from "react";
import { Satellite } from "@/types/satellite";
import { Eye, Pencil, Trash2, PlusCircle, Search, Rocket } from "lucide-react";
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
import SatelliteForm from "./satellite-form";
import SatelliteDetails from "./satellite-details";
import { fetchSatellites, deleteSatellite } from "@/services/satellite";

interface SatelliteListProps {
    refresh: boolean;
    onRefresh: () => void;
}

const SatelliteList: React.FC<SatelliteListProps> = ({ refresh, onRefresh }) => {
    const [satellites, setSatellites] = useState<Satellite[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [editingSatellite, setEditingSatellite] = useState<Satellite | null>(null);
    const [inspectingSatellite, setInspectingSatellite] = useState<Satellite | null>(null);
    const [deleteId, setDeleteId] = useState<string | null>(null);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        const loadSatellites = async () => {
            setLoading(true);
            try {
                const data = await fetchSatellites();
                setSatellites(data.items);
            } catch (error) {
                toast.error("Failed to load satellites.");
            } finally {
                setLoading(false);
            }
        };
        loadSatellites();
    }, [refresh]);

    const filteredSatellites = satellites.filter(sat =>
        sat.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        sat.group?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        sat.tleConfig.noradId.toString().includes(searchTerm)
    );

    if (loading) {
        return (
            <Card className="w-full">
                <CardContent className="flex items-center justify-center h-32">
                    <div className="text-muted-foreground">Loading satellites...</div>
                </CardContent>
            </Card>
        );
    }

    const handleEdit = (satellite: Satellite) => {
        setEditingSatellite(satellite);
    };

    const handleInspect = (satellite: Satellite) => {
        setInspectingSatellite(satellite);
    };

    const handleDelete = async (id: string) => {
        try {
            await deleteSatellite(id);
            toast.success("Satellite deleted successfully.");
            onRefresh();
            setDeleteId(null);
        } catch {
            toast.error("Failed to delete satellite.");
        }
    };

    return (
        <Card className="w-full">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <div>
                    <CardTitle>Satellite Configuration</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                        Manage and monitor your satellite configurations
                    </p>
                </div>
                <Dialog>
                    <DialogTrigger asChild>
                        <Button variant="default" className="flex items-center gap-2">
                            <PlusCircle className="h-4 w-4" />
                            Add Satellite
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[600px]">
                        <DialogHeader>
                            <DialogTitle>Create Satellite</DialogTitle>
                        </DialogHeader>
                        <SatelliteForm
                            onRefresh={onRefresh}
                            onClose={() => setEditingSatellite(null)}
                        />
                    </DialogContent>
                </Dialog>
            </CardHeader>
            <CardContent>
                <div className="flex items-center gap-4 mb-4">
                    <div className="relative flex-1 max-w-sm">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search by name, group, or NORAD ID..."
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
                                <TableHead>Group</TableHead>
                                <TableHead>NORAD ID</TableHead>
                                <TableHead>Propulsion</TableHead>
                                <TableHead>Mass (kg)</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredSatellites.map((satellite) => (
                                <TableRow key={satellite.id}>
                                    <TableCell className="font-medium">{satellite.name}</TableCell>
                                    <TableCell>
                                        {satellite.group ? (
                                            <span className="inline-flex items-center rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-700/10">
                                                {satellite.group}
                                            </span>
                                        ) : '-'}
                                    </TableCell>
                                    <TableCell>{satellite.tleConfig.noradId}</TableCell>
                                    <TableCell>
                                        <div className="flex items-center gap-2">
                                            <Rocket className="h-4 w-4 text-muted-foreground" />
                                            <span>{satellite.propulsion.name}</span>
                                        </div>
                                    </TableCell>
                                    <TableCell>{satellite.dryMass}</TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end space-x-2">
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8"
                                                onClick={() => handleInspect(satellite)}
                                                title="Inspect"
                                            >
                                                <Eye className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8"
                                                onClick={() => handleEdit(satellite)}
                                                title="Edit"
                                            >
                                                <Pencil className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8 text-destructive hover:text-destructive"
                                                onClick={() => setDeleteId(satellite.id)}
                                                title="Delete"
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

            {/* Edit Dialog */}
            <Dialog
                open={editingSatellite !== null}
                onOpenChange={(open) => !open && setEditingSatellite(null)}
            >
                <DialogContent className="sm:max-w-[600px]">
                    <DialogHeader>
                        <DialogTitle>Update Satellite</DialogTitle>
                    </DialogHeader>
                    {editingSatellite && (
                        <SatelliteForm
                            initialData={editingSatellite}
                            onRefresh={onRefresh}
                            onClose={() => setEditingSatellite(null)}
                        />
                    )}
                </DialogContent>
            </Dialog>

            {/* Inspect Dialog */}
            <Dialog
                open={inspectingSatellite !== null}
                onOpenChange={(open) => !open && setInspectingSatellite(null)}
            >
                <DialogContent className="sm:max-w-[800px]">
                    <DialogHeader>
                        <DialogTitle>
                            Satellite Details: {inspectingSatellite?.name}
                        </DialogTitle>
                    </DialogHeader>
                    {inspectingSatellite && <SatelliteDetails satellite={inspectingSatellite} />}
                </DialogContent>
            </Dialog>

            {/* Delete Confirmation Dialog */}
            <Dialog open={!!deleteId} onOpenChange={(isOpen) => !isOpen && setDeleteId(null)}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Confirm Deletion</DialogTitle>
                    </DialogHeader>
                    <p>Are you sure you want to delete this satellite? This action cannot be undone.</p>
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

export default SatelliteList;