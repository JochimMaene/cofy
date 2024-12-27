import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Plus, Trash2 } from "lucide-react";
import { useState } from "react";

interface ElevationPoint {
    azimuth: number;
    elevation: number;
}

interface ElevationMaskEditorProps {
    value: ElevationPoint[];
    onChange: (value: ElevationPoint[]) => void;
}

export function ElevationMaskEditor({ value, onChange }: ElevationMaskEditorProps) {
    const [newPoint, setNewPoint] = useState<ElevationPoint>({ azimuth: 0, elevation: 0 });

    const addPoint = () => {
        const sortedPoints = [...value, newPoint].sort((a, b) => a.azimuth - b.azimuth);
        onChange(sortedPoints);
        setNewPoint({ azimuth: 0, elevation: 0 });
    };

    const removePoint = (index: number) => {
        const newPoints = value.filter((_, i) => i !== index);
        onChange(newPoints);
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center">
                <div className="font-medium">Elevation Mask</div>
            </div>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Azimuth (°)</TableHead>
                        <TableHead>Elevation (°)</TableHead>
                        <TableHead className="w-[100px]">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {value.map((point, index) => (
                        <TableRow key={index}>
                            <TableCell>{point.azimuth.toFixed(1)}</TableCell>
                            <TableCell>{point.elevation.toFixed(1)}</TableCell>
                            <TableCell>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    onClick={() => removePoint(index)}
                                >
                                    <Trash2 className="h-4 w-4" />
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                    <TableRow>
                        <TableCell>
                            <Input
                                type="number"
                                min={0}
                                max={360}
                                step={0.1}
                                value={newPoint.azimuth}
                                onChange={(e) => setNewPoint({ ...newPoint, azimuth: parseFloat(e.target.value) })}
                                placeholder="Azimuth"
                            />
                        </TableCell>
                        <TableCell>
                            <Input
                                type="number"
                                min={0}
                                max={90}
                                step={0.1}
                                value={newPoint.elevation}
                                onChange={(e) => setNewPoint({ ...newPoint, elevation: parseFloat(e.target.value) })}
                                placeholder="Elevation"
                            />
                        </TableCell>
                        <TableCell>
                            <Button
                                variant="ghost"
                                size="icon"
                                onClick={addPoint}
                            >
                                <Plus className="h-4 w-4" />
                            </Button>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        </div>
    );
}

export default ElevationMaskEditor; 