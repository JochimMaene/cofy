import React, { useState, useMemo } from "react";
import { IpfOrbit } from "@/types/orbit";
import { Search, Download, Trash2, Copy } from "lucide-react";
import {
    Table,
    TableHeader,
    TableBody,
    TableRow,
    TableHead,
    TableCell,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { format } from "date-fns";
import { deleteOrbit, downloadOrbit } from "@/services/orbit";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";

interface OrbitListProps {
    orbits: IpfOrbit[];
    onRefresh: () => void;
}

export function OrbitList({ orbits = [], onRefresh }: OrbitListProps) {
    const [searchTerm, setSearchTerm] = useState("");
    const [startDate, setStartDate] = useState<string>("");
    const [endDate, setEndDate] = useState<string>("");

    console.log("Received orbits:", orbits);

    const filteredOrbits = useMemo(() => {
        console.log("Filtering orbits:", orbits);
        if (!Array.isArray(orbits)) {
            console.log("Orbits is not an array");
            return [];
        }

        return orbits.filter((orbit) => {
            const matchesSearch =
                orbit.fileName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                orbit.satellite.name.toLowerCase().includes(searchTerm.toLowerCase());

            const matchesDateRange =
                (!startDate || new Date(orbit.start) >= new Date(startDate)) &&
                (!endDate || new Date(orbit.end) <= new Date(endDate));

            return matchesSearch && matchesDateRange;
        });
    }, [orbits, searchTerm, startDate, endDate]);

    console.log("Filtered orbits:", filteredOrbits);

    const handleDownload = async (orbit: IpfOrbit) => {
        try {
            const blob = await downloadOrbit(orbit.id);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = orbit.fileName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            toast.error("Failed to download orbit file");
        }
    };

    const handleDelete = async (orbit: IpfOrbit) => {
        try {
            await deleteOrbit(orbit.id);
            toast.success("Orbit file deleted successfully");
            onRefresh();
        } catch (error) {
            toast.error("Failed to delete orbit file");
        }
    };

    return (
        <Card className="w-full max-w-[1000px] mx-auto">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <div>
                    <CardTitle>Orbit Files</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                        Manage orbit files and configurations
                    </p>
                </div>
            </CardHeader>
            <CardContent>
                <div className="flex items-center gap-4 mb-4">
                    <div className="relative flex-1">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                        <Input
                            placeholder="Search by filename or satellite..."
                            className="pl-8"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex gap-2">
                        <Input
                            type="datetime-local"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            className="w-auto"
                        />
                        <Input
                            type="datetime-local"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            className="w-auto"
                        />
                    </div>
                </div>

                <div className="rounded-md border">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Satellite</TableHead>
                                <TableHead>Filename</TableHead>
                                <TableHead>Start Time</TableHead>
                                <TableHead>End Time</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredOrbits.map((orbit) => (
                                <TableRow key={orbit.id}>
                                    <TableCell className="font-medium">
                                        {orbit.satellite.name}
                                    </TableCell>
                                    <TableCell>{orbit.fileName}</TableCell>
                                    <TableCell>
                                        {format(new Date(orbit.start), "PPpp")}
                                    </TableCell>
                                    <TableCell>
                                        {format(new Date(orbit.end), "PPpp")}
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end space-x-2">
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => {
                                                    navigator.clipboard.writeText(orbit.id);
                                                    toast.success("ID copied to clipboard");
                                                }}
                                                title="Copy ID"
                                            >
                                                <Copy className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => handleDownload(orbit)}
                                                title="Download"
                                            >
                                                <Download className="h-4 w-4" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => handleDelete(orbit)}
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
        </Card>
    );
} 