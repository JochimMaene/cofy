import { useState } from "react";
import { GroundStation } from "@/types/ground-station";
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
    DialogContent,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Edit2, Trash2, PlusCircle } from "lucide-react";
import { GroundStationForm } from "./ground-station-form";
import { createGroundStation, updateGroundStation, deleteGroundStation } from "@/services/ground-station";
// import { useUser } from "@/hooks/useUser";

interface GroundStationListProps {
    groundStations: GroundStation[];
    onRefresh: () => void;
}

export function GroundStationList({ groundStations, onRefresh }: GroundStationListProps) {
    const [selectedStation, setSelectedStation] = useState<GroundStation | null>(null);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    // const { isSuperuser } = useUser();

    const handleCreate = async (data: GroundStation) => {
        try {
            await createGroundStation(data);
            setIsDialogOpen(false);
            onRefresh();
            toast.success("Ground station created successfully");
        } catch (error) {
            toast.error("Failed to create ground station");
        }
    };

    const handleUpdate = async (data: GroundStation) => {
        try {
            if (selectedStation) {
                await updateGroundStation({ ...data, id: selectedStation.id });
                setSelectedStation(null);
                onRefresh();
                toast.success("Ground station updated successfully");
            }
        } catch (error) {
            toast.error("Failed to update ground station");
        }
    };

    const handleDelete = async (station: GroundStation) => {
        if (confirm("Are you sure you want to delete this ground station?")) {
            try {
                await deleteGroundStation(station.id);
                onRefresh();
                toast.success("Ground station deleted successfully");
            } catch (error) {
                toast.error("Failed to delete ground station");
            }
        }
    };

    return (
        <Card className="w-full">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <div>
                    <CardTitle>Ground Stations</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                        Manage ground station configurations
                    </p>
                </div>
                {(
                    <Button onClick={() => setIsDialogOpen(true)}>
                        <PlusCircle className="mr-2 h-4 w-4" />
                        Add Station
                    </Button>
                )}
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead>Name</TableHead>
                            <TableHead>Group</TableHead>
                            <TableHead>Longitude</TableHead>
                            <TableHead>Latitude</TableHead>
                            <TableHead>Altitude</TableHead>
                            <TableHead>Mask Points</TableHead>
                            <TableHead className="text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {groundStations.map((station) => (
                            <TableRow key={station.id}>
                                <TableCell>{station.name}</TableCell>
                                <TableCell>{station.group || "-"}</TableCell>
                                <TableCell>{station.longitude.toFixed(6)}°</TableCell>
                                <TableCell>{station.latitude.toFixed(6)}°</TableCell>
                                <TableCell>{station.altitude.toFixed(1)} m</TableCell>
                                <TableCell>{station.elevation_mask?.length || 0}</TableCell>
                                <TableCell className="text-right">
                                    {(
                                        <div className="flex justify-end space-x-2">
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => setSelectedStation(station)}
                                            >
                                                <Edit2 className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => handleDelete(station)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    )}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </CardContent>

            <Dialog
                open={isDialogOpen || !!selectedStation}
                onOpenChange={(open) => {
                    setIsDialogOpen(open);
                    if (!open) setSelectedStation(null);
                }}
            >
                <DialogContent className="max-w-2xl">
                    <DialogHeader>
                        <DialogTitle>
                            {selectedStation ? "Edit Ground Station" : "Add Ground Station"}
                        </DialogTitle>
                    </DialogHeader>
                    <GroundStationForm
                        initialData={selectedStation || undefined}
                        onSubmit={selectedStation ? handleUpdate : handleCreate}
                        onCancel={() => {
                            setIsDialogOpen(false);
                            setSelectedStation(null);
                        }}
                    />
                </DialogContent>
            </Dialog>
        </Card>
    );
} 