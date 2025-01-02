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

    const addPoint = (e: React.MouseEvent) => {
        e.preventDefault(); // Prevent form submission
        e.stopPropagation(); // Prevent event bubbling
        const sortedPoints = [...value, newPoint].sort((a, b) => a.azimuth - b.azimuth);
        onChange(sortedPoints);
        setNewPoint({ azimuth: 0, elevation: 0 });
    };

    const removePoint = (index: number, e: React.MouseEvent) => {
        e.preventDefault(); // Prevent form submission
        e.stopPropagation(); // Prevent event bubbling
        const newPoints = value.filter((_, i) => i !== index);
        onChange(newPoints);
    };

    return (
        <div className="space-y-4">
            <div className="flex justify-between items-center">
                <div className="font-medium">Elevation Mask</div>
                <div className="text-sm text-muted-foreground">
                    {value.length} points
                </div>
            </div>
            <div className="border rounded-md max-h-[300px] overflow-y-auto">
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead className="w-[33%]">Azimuth (°)</TableHead>
                            <TableHead className="w-[33%]">Elevation (°)</TableHead>
                            <TableHead className="w-[100px] text-right">Actions</TableHead>
                        </TableRow>
                    </TableHeader>
                    <TableBody>
                        {value.map((point, index) => (
                            <TableRow key={index}>
                                <TableCell className="w-[33%]">{point.azimuth.toFixed(1)}</TableCell>
                                <TableCell className="w-[33%]">{point.elevation.toFixed(1)}</TableCell>
                                <TableCell className="w-[100px] text-right">
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="icon"
                                        onClick={(e) => removePoint(index, e)}
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </div>

            <div className="grid grid-cols-[1fr_1fr_auto] items-center gap-4">
                <Input
                    type="number"
                    min={0}
                    max={360}
                    step={0.1}
                    value={newPoint.azimuth}
                    onChange={(e) => setNewPoint({ ...newPoint, azimuth: parseFloat(e.target.value) })}
                    placeholder="Azimuth"
                />
                <Input
                    type="number"
                    min={0}
                    max={90}
                    step={0.1}
                    value={newPoint.elevation}
                    onChange={(e) => setNewPoint({ ...newPoint, elevation: parseFloat(e.target.value) })}
                    placeholder="Elevation"
                />
                <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={addPoint}
                >
                    <Plus className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}

export default ElevationMaskEditor; 