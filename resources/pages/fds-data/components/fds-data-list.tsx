import React, { useEffect, useState } from "react";
import { FdsData } from "@/types/fds-data";
import {
    Clock,
    Edit2,
    AlertCircle,
    Calendar,
    Copy,
    RotateCw,
    CheckCircle2
} from "lucide-react";
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
import FdsDataForm from "./fds-data-form";
import { fetchFdsData, refreshFdsData } from "@/services/fds-data";
// import { useUser } from "@/hooks/useUser";

interface FdsDataListProps {
    refresh: boolean;
    onRefresh: () => void;
}

const FdsDataList: React.FC<FdsDataListProps> = ({ refresh, onRefresh }) => {
    // const { isSuperuser } = useUser();
    const [fdsData, setFdsData] = useState<FdsData[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [editingFdsData, setEditingFdsData] = useState<FdsData | null>(null);
    const [refreshing, setRefreshing] = useState<number | null>(null);

    useEffect(() => {
        const loadFdsData = async () => {
            setLoading(true);
            try {
                const data = await fetchFdsData();
                setFdsData(data);
            } catch (error) {
                toast.error("Failed to load FDS data status.");
            } finally {
                setLoading(false);
            }
        };
        loadFdsData();
    }, [refresh]);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "updated":
                return <CheckCircle2 className="h-5 w-5 text-green-500" />;
            case "out_of_date":
                return <AlertCircle className="h-5 w-5 text-red-500" />;
            default:
                return null;
        }
    };

    const handleCopyUrl = (url: string) => {
        navigator.clipboard.writeText(url);
        toast.success("URL copied to clipboard");
    };

    const handleManualRefresh = async (id: number) => {
        setRefreshing(id);
        try {
            await refreshFdsData(id);
            toast.success("Environment file updated.");
            onRefresh();
        } catch (error) {
            toast.error("Failed to update environment file.");
        } finally {
            setRefreshing(null);
        }
    };

    if (loading) {
        return (
            <Card className="w-full">
                <CardContent className="flex items-center justify-center h-32">
                    <div className="text-muted-foreground">Loading FDS data status...</div>
                </CardContent>
            </Card>
        );
    }

    return (
        <Card className="w-full">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
                <div>
                    <CardTitle>FDS Data Status</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                        Monitor and manage FDS data update configurations
                    </p>
                </div>
            </CardHeader>
            <CardContent>
                <div className="rounded-md border">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Last Update</TableHead>
                                <TableHead>Next Update</TableHead>
                                <TableHead>Schedule</TableHead>
                                <TableHead>URL</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {fdsData.map((data) => (
                                <TableRow key={data.id}>
                                    <TableCell className="font-medium">{data.name}</TableCell>
                                    <TableCell>
                                        <div
                                            className="flex items-center justify-center"
                                            title={data.status}
                                        >
                                            {getStatusIcon(data.status)}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex items-center gap-2">
                                            <Clock className="h-4 w-4 text-muted-foreground" />
                                            {data.lastUpdate}
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex items-center gap-2">
                                            <Calendar className="h-4 w-4 text-muted-foreground" />
                                            {data.nextUpdate}
                                        </div>
                                    </TableCell>
                                    <TableCell className="whitespace-nowrap">
                                        {data.cron}
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex items-center gap-2">
                                            <span className="truncate max-w-[200px]">{data.URL}</span>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-6 w-6"
                                                onClick={() => handleCopyUrl(data.URL)}
                                                title="Copy URL"
                                            >
                                                <Copy className="h-3 w-3" />
                                            </Button>
                                        </div>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <div className="flex justify-end space-x-2">
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8"
                                                title="Refresh Data"
                                                onClick={() => handleManualRefresh(data.id)}
                                                disabled={refreshing === data.id}
                                            >
                                                <RotateCw className={`h-4 w-4 ${refreshing === data.id ? 'animate-spin' : ''}`} />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="h-8 w-8"
                                                onClick={() => setEditingFdsData(data)}
                                                title="Edit"
                                            >
                                                <Edit2 className="h-4 w-4" />
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
                open={editingFdsData !== null}
                onOpenChange={(open) => !open && setEditingFdsData(null)}
            >
                <DialogContent className="sm:max-w-[600px]">
                    <DialogHeader>
                        <DialogTitle>Edit FDS Data Update Settings</DialogTitle>
                    </DialogHeader>
                    {editingFdsData && (
                        <FdsDataForm
                            initialData={editingFdsData}
                            onRefresh={onRefresh}
                            onClose={() => setEditingFdsData(null)}
                        />
                    )}
                </DialogContent>
            </Dialog>
        </Card>
    );
};

export default FdsDataList;
